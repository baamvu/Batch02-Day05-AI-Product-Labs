"""
Prompt template for the AI IN ACTION Copilot RAG flow.

This module only turns retrieved chunks into chat messages.
It does not call the retriever or the LLM.
"""

from typing import Any, Dict, List


SYSTEM_PROMPT = (
    "Bạn là AI Copilot hỗ trợ chương trình 'AI Thực Chiến' (Batch 02, VinUniversity).\n"
    "Nhiệm vụ: trả lời câu hỏi dựa trên nội dung được cung cấp bên dưới.\n\n"
    "QUY TẮC:\n"
    "- Chỉ trả lời dựa trên context được cung cấp. Không bịa thông tin.\n"
    "- Trả lời bằng tiếng Việt, rõ ràng, ngắn gọn.\n"
    "- Nếu context không đủ để trả lời, nói rõ rằng thông tin chưa có trong knowledge base.\n\n"
    "OUTPUT FORMAT (JSON):\n"
    "{{\n"
    '  "answer": "Câu trả lời chi tiết bằng tiếng Việt",\n'
    '  "sources": ["Nguồn 1: mô tả ngắn", "Nguồn 2: mô tả ngắn"],\n'
    '  "next_action": "Gợi ý hành động tiếp theo cho người hỏi"\n'
    "}}\n\n"
    "Chỉ trả về JSON, không thêm markdown hay text khác."
)


def build_context(chunks: List[Dict[str, Any]]) -> str:
    """Format retrieved chunks into grounded context for the LLM."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source_file", "unknown")
        day = chunk.get("day", "unknown")
        section = chunk.get("section", "unknown")
        content = chunk.get("content", "")
        context_parts.append(f"[Nguồn {i}] ({source} | {day} | {section})\n{content}")

    return "\n\n---\n\n".join(context_parts)


def build_prompt_messages(question: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Build OpenAI-compatible chat messages for a grounded RAG answer."""
    context = build_context(chunks)
    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
