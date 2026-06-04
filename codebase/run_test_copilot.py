import csv
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Thêm đường dẫn project để import được src
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.rag_chain import ask_copilot

GROUND_TRUTH_COLUMN = "Câu trả lời mong đợi (Ground Truth)"
LOG_COLUMNS = [
    "timestamp",
    "test_id",
    "question_type",
    "question",
    "expected_answer",
    "actual_answer",
    "sources",
    "next_action",
    "pass_fail",
    "score",
    "error_type",
    "note",
    "latency_ms",
]


def normalize_text(text):
    text = (text or "").lower()
    text = re.sub(r"[^\w\sÀ-ỹ]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def evaluate_answer(expected, actual, sources):
    """
    Heuristic chấm nhanh để QA có điểm khởi đầu.
    Người 4 vẫn nên review thủ công các case PARTIAL/FAIL.
    """
    expected_norm = normalize_text(expected)
    actual_norm = normalize_text(actual)

    if not actual_norm:
        return "FAIL", 0.0, "empty_answer", "Không có câu trả lời từ AI."

    fallback_expected = "(fallback)" in expected.lower()
    fallback_signals = [
        "không có trong",
        "chưa có trong",
        "không tìm thấy",
        "không thể",
        "ngoài phạm vi",
        "không được đề cập",
        "bạn có thể nói rõ",
    ]

    if fallback_expected:
        if any(signal in actual.lower() for signal in fallback_signals):
            return "PASS", 1.0, "", "Fallback đúng hướng, không bịa thông tin ngoài tài liệu."
        return "FAIL", 0.0, "missing_fallback", "Case yêu cầu fallback nhưng AI có vẻ trả lời như có thông tin."

    expected_tokens = set(expected_norm.split())
    actual_tokens = set(actual_norm.split())
    if not expected_tokens:
        return "PARTIAL", 0.5, "missing_ground_truth", "Ground truth rỗng hoặc không đọc được."

    overlap = len(expected_tokens & actual_tokens) / len(expected_tokens)

    if overlap >= 0.45 and sources:
        return "PASS", round(overlap, 2), "", "Đúng nhiều ý chính và có nguồn."
    if overlap >= 0.45 and not sources:
        return "PARTIAL", round(overlap, 2), "missing_source", "Đúng nhiều ý chính nhưng thiếu nguồn."
    if overlap >= 0.25:
        return "PARTIAL", round(overlap, 2), "incomplete_answer", "Có một phần ý đúng, cần QA kiểm tra thêm."
    return "FAIL", round(overlap, 2), "low_overlap", "Câu trả lời khác xa ground truth, cần kiểm tra retrieval hoặc prompt."


def open_log_writer(project_root):
    log_dir = project_root / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"test_results_{run_id}.csv"
    log_file = open(log_path, mode="w", encoding="utf-8-sig", newline="")
    writer = csv.DictWriter(log_file, fieldnames=LOG_COLUMNS)
    writer.writeheader()
    return log_path, log_file, writer


def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 Đang khởi tạo AI Copilot (Sẽ kết nối với MIMO LLM API)...")

    csv_path = project_root / "data" / "test_cases.csv"
    if not csv_path.exists():
        print(f"❌ Không tìm thấy file {csv_path}")
        return

    print(f"Đang đọc danh sách câu hỏi từ {csv_path.name}...\n")
    log_path, log_file, log_writer = open_log_writer(project_root)
    print(f"🧾 Kết quả test sẽ được ghi vào: {log_path}\n")

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for idx, row in enumerate(reader, 1):
                category = row.get("Loại câu hỏi", "Unknown")
                question = row.get("Câu hỏi", "")
                expected = row.get(GROUND_TRUTH_COLUMN, "")

                if not question:
                    continue

                print("=" * 80)
                print(f"📝 TEST CASE #{idx} [{category}]")
                print(f"❓ Hỏi: {question}")
                print(f"🎯 Trả lời mong đợi: {expected}")
                print("-" * 40)

                print("⏳ AI đang suy nghĩ và tổng hợp câu trả lời...")
                started_at = time.perf_counter()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                answer = ""
                next_action = ""
                sources = []
                pass_fail = "FAIL"
                score = 0.0
                error_type = ""
                note = ""

                try:
                    # Gọi thẳng hàm ask_copilot của Backend
                    result = ask_copilot(question, top_k=3)
                    answer = result.get('answer', '')
                    next_action = result.get('next_action', '')
                    sources = result.get('sources', [])
                    pass_fail, score, error_type, note = evaluate_answer(expected, answer, sources)

                    print(f"🤖 AI Trả lời: {answer}")
                    print(f"💡 Gợi ý tiếp theo: {next_action}")
                    print(f"🧪 Đánh giá sơ bộ: {pass_fail} | score={score} | {note}")
                    print("📚 Nguồn trích dẫn:")
                    if sources:
                        for src in sources:
                            print(f"  - {src}")
                    else:
                        print("  (Không có nguồn)")
                except Exception as e:
                    error_type = "runtime_error"
                    note = str(e)
                    print(f"❌ Lỗi khi gọi AI: {e}")

                latency_ms = round((time.perf_counter() - started_at) * 1000)
                log_writer.writerow({
                    "timestamp": timestamp,
                    "test_id": idx,
                    "question_type": category,
                    "question": question,
                    "expected_answer": expected,
                    "actual_answer": answer,
                    "sources": " | ".join(sources),
                    "next_action": next_action,
                    "pass_fail": pass_fail,
                    "score": score,
                    "error_type": error_type,
                    "note": note,
                    "latency_ms": latency_ms,
                })
                log_file.flush()

                print("=" * 80 + "\n")

                # Tạm dừng để dễ theo dõi
                if idx % 2 == 0:
                    cont = input("💡 Nhấn Enter để test 2 câu tiếp theo, hoặc gõ 'q' để thoát: ")
                    if cont.strip().lower() == 'q':
                        break
    finally:
        log_file.close()

    print("✅ Đã hoàn thành bài test AI Copilot!")
    print(f"📄 File log: {log_path}")

if __name__ == "__main__":
    main()
