"""
RAG Copilot module.

Usage:
    from src.copilot import ask_copilot
    result = ask_copilot("Day 5 cần nộp gì?")
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from src.retriever import CourseRetriever
from src.llm.client import get_llm_client

_retriever_instance: Optional[CourseRetriever] = None


def _get_retriever() -> CourseRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = CourseRetriever()
    return _retriever_instance


def _build_prompt(question: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source_file", "unknown")
        day = chunk.get("day", "unknown")
        section = chunk.get("section", "unknown")
        content = chunk.get("content", "")
        context_parts.append(
            f"[Nguồn {i}] ({source} | {day} | {section})\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "Bạn là AI Copilot hỗ trợ chương trình 'AI Thực Chiến' (Batch 02, VinUniversity).\n"
        "Nhiệm vụ: trả lời câu hỏi dựa trên nội dung được cung cấp bên dưới.\n\n"
        "QUY TẮC:\n"
        "- Chỉ trả lời dựa trên context được cung cấp. Không bịa thông tin.\n"
        "- Trả lời bằng tiếng Việt, rõ ràng, ngắn gọn.\n"
        "- Nếu context không đủ để trả lời, nói rõ rằng thông tin chưa có trong knowledge base.\n\n"
        "OUTPUT FORMAT (JSON):\n"
        '{{\n'
        '  "answer": "Câu trả lời chi tiết bằng tiếng Việt",\n'
        '  "sources": ["Nguồn 1: mô tả ngắn", "Nguồn 2: mô tả ngắn"],\n'
        '  "next_action": "Gợi ý hành động tiếp theo cho người hỏi"\n'
        '}}\n\n'
        "Chỉ trả về JSON, không thêm markdown hay text khác."
    )

    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _call_mimo(prompt_messages: List[Dict[str, str]], timeout: int = 60) -> str:
    client = get_llm_client()
    return client.chat(
        messages=prompt_messages,
        temperature=0.3,
        max_tokens=1024,
    )


def _parse_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    return json.loads(text)


def _format_source(chunk: Dict[str, Any]) -> str:
    source = chunk.get("source_file", "unknown")
    day = chunk.get("day", "unknown")
    section = chunk.get("section", "unknown")
    return f"{source} | {day} | {section}"


def ask_copilot(
    question: str,
    top_k: int = 4,
    retriever: Optional[CourseRetriever] = None,
) -> Dict[str, Any]:
    """
    Ask the RAG backend and return answer + sources + next action.

    Args:
        question: User question string
        top_k: Number of chunks to retrieve
        retriever: Optional CourseRetriever instance (created if not provided)

    Returns:
        Dict with keys:
            - question: Original question
            - answer: LLM-generated answer
            - sources: List of source descriptions
            - next_action: Suggested next step
            - retrieved_chunks: Raw chunks from retriever (for debug/frontend)
    """
    if not question or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    if retriever is None:
        retriever = _get_retriever()

    retrieved_chunks = retriever.search(question, top_k=top_k)

    if not retrieved_chunks:
        return {
            "question": question,
            "answer": "Không tìm thấy thông tin phù hợp trong knowledge base.",
            "sources": [],
            "next_action": "Kiểm tra lại câu hỏi hoặc cập nhật thêm nội dung vào knowledge base.",
            "retrieved_chunks": [],
        }

    prompt = _build_prompt(question, retrieved_chunks)

    try:
        model_output = _call_mimo(prompt)
    except Exception as e:
        return {
            "question": question,
            "answer": f"Lỗi khi gọi LLM: {e}",
            "sources": [_format_source(c) for c in retrieved_chunks],
            "next_action": "Thử lại sau hoặc kiểm tra API key trong .env.",
            "retrieved_chunks": retrieved_chunks,
        }

    try:
        parsed = _parse_json(model_output)
    except (ValueError, json.JSONDecodeError):
        parsed = {
            "answer": model_output,
            "sources": [_format_source(c) for c in retrieved_chunks],
            "next_action": "Xem lại các nguồn tham chiếu hoặc hỏi lại cụ thể hơn.",
        }

    sources = parsed.get("sources")
    if isinstance(sources, str):
        sources = [sources]
    if not sources:
        sources = [_format_source(c) for c in retrieved_chunks]

    return {
        "question": question,
        "answer": parsed.get("answer", ""),
        "sources": sources,
        "next_action": parsed.get("next_action", "Thử đặt câu hỏi tiếp theo."),
        "retrieved_chunks": retrieved_chunks,
    }
