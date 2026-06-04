# QA / Evaluation Report - AI IN ACTION Copilot

**Người phụ trách:** Lê Sỹ - Người 4    QA / Evaluation / Demo Test  
**Ngày chạy test:** 2026-06-04  
**File log:** `C:\Users\Asus\AI_Labs\Day06-C401-Vinflow\codebase\data\logs\test_results_20260604_112552.csv`  
**Bộ test:** `data/test_cases.csv`

## 1. Mục tiêu test

Kiểm tra AI Copilot trên bộ câu hỏi `test_cases.csv` để đánh giá:

- Khả năng trả lời câu hỏi fact-based dựa trên tài liệu Day 1-5.
- Khả năng suy luận / so sánh dựa trên framework trong bài học.
- Khả năng fallback khi câu hỏi ngoài phạm vi, thiếu dữ liệu hoặc mơ hồ.
- Chatbot có trả lời kèm source và next action hay không.
- Độ trễ của từng câu trả lời khi chạy demo.

## 2. Kết quả tổng quan

| Chỉ số | Kết quả |
|---|---:|
| Tổng số test cases | 20 |
| PASS | 17 |
| FAIL | 3 |
| PARTIAL | 0 |
| Accuracy sơ bộ | 85% |
| Latency trung bình | ~21s |
| Case chậm nhất | Test #3 - ~133s |

Nhận định nhanh: Hệ thống đang đủ tốt để demo prototype. Đa số câu hỏi fact-based và reasoning trả lời đúng ý chính, có source. Các lỗi còn lại tập trung vào retrieval miss và fallback với câu hỏi mơ hồ.

## 3. Các case FAIL cần xem xét

### Test #4 - Retrieval miss

**Loại:** Fact-based (Day 2)  
**Câu hỏi:** Ba mức giải pháp hệ thống AI được đề cập trong Day 2 là gì?  
**Ground truth:** Rule / Script, LLM Feature, và Agent.  
**Kết quả thực tế:** Bot nói context không có thông tin này và lấy nhầm sang các đoạn về `Model + Context + Planning + Tools` và lý do doanh nghiệp đầu tư AI.

**Đánh giá:** Lỗi retrieval thật. Câu hỏi rõ ràng, ground truth đúng, nhưng retriever không đưa đúng chunk Day 2 slide 28 vào context.

**Hướng xử lý:**

- Kiểm tra chunk Day 2 slide 28 có nằm trong `chunks.jsonl` không.
- Tăng `top_k` khi gọi `ask_copilot`, vì hiện tại đang dùng `top_k=3`.
- Nếu câu hỏi có nhắc `Day 2`, đảm bảo filter theo `day2` hoạt động đúng.
- Có thể thêm keyword vào chunk hoặc cải thiện chunking để cụm "Rule / Script, LLM Feature, Agent" dễ tìm hơn.

### Test #16 - Ground truth cần chỉnh lại

**Loại:** Edge Case (Thiếu dữ liệu)  
**Câu hỏi:** Ai là giảng viên phụ trách đứng lớp Day 3?  
**Ground truth hiện tại:** Yêu cầu fallback, nói chỉ có tên Phạm Mạnh và không có profile/liên hệ.  
**Kết quả thực tế:** Bot trả lời giảng viên Day 3 là Phạm Mạnh, đến từ VinUniversity.

**Đánh giá:** Bot không sai nghiêm trọng. Tài liệu Day 3 có ghi giảng viên là Phạm Mạnh và đơn vị VinUniversity. Lỗi chính nằm ở cách viết ground truth: câu hỏi hỏi "ai là giảng viên", nên bot có thể trả lời tên.

**Hướng xử lý:**

- Nếu muốn test câu hỏi fact-based, đổi expected thành:

```text
Giảng viên phụ trách Day 3 là Phạm Mạnh. Tài liệu chỉ ghi thêm đơn vị VinUniversity, không có profile hoặc thông tin liên hệ chi tiết.
```

- Nếu muốn test thiếu dữ liệu, đổi câu hỏi thành:

```text
Profile hoặc thông tin liên hệ của giảng viên Phạm Mạnh là gì?
```

### Test #17 - Câu hỏi mơ hồ / fallback chưa tốt

**Loại:** Edge Case (Mơ hồ)  
**Câu hỏi:** Ngày mai phải nộp bài tập thực hành như thế nào?  
**Ground truth:** Bot nên hỏi lại đang hỏi bài tập của Day nào.  
**Kết quả thực tế:** Bot nói context không có format nộp bài cụ thể, nhưng sau đó suy luận sang Day 6 và trả lời dài dựa trên Day 5.

**Đánh giá:** Đây là lỗi ambiguity handling. Bot có dấu hiệu fallback một phần, nhưng vẫn đoán tiếp quá nhiều.

**Hướng xử lý:**

- Thêm rule vào system prompt: với câu hỏi dùng thời gian tương đối như "hôm nay", "ngày mai", "bài này", nếu không có Day cụ thể thì hỏi lại.
- Hạn chế bot suy luận lịch học nếu context không nói rõ ngày hiện tại của người dùng.
- Giữ case này trong bộ test để chứng minh product có kiểm tra low-confidence path.

## 4. Vấn đề latency

Top case chậm nhất:

| Test | Loại | Latency |
|---:|---|---:|
| #3 | Fact-based (Day 2) | ~133s |
| #11 | Reasoning | ~75s |
| #1 | Fact-based (Day 1) | ~34s |
| #10 | Fact-based (Day 5) | ~25s |
| #13 | Reasoning | ~21s |

Nhận xét: Latency trung bình bị kéo cao bởi một vài case rất chậm. Có thể do lần đầu load retriever / vectorstore, API LLM chậm, hoặc prompt context quá dài.

Hướng xử lý:

- Khi demo, chạy warm-up trước bằng 1 câu hỏi đơn giản.
- Dùng sẵn 3 câu hỏi demo đã test PASS để tránh bất ngờ.
- Nếu cần tối ưu, giảm context hoặc giới hạn chunk ngắn hơn.
- Ghi trong demo script rằng đây là prototype local/API nên latency có thể dao động.

## 5. Case nên dùng để demo

Nên chọn 3 case đại diện:

1. **Fact-based PASS:** Một câu hỏi Day 1/3/5 có answer đúng và source rõ.
2. **Reasoning PASS:** Câu hỏi về Agent loop, Automation vs Augmentation, hoặc False Positive/False Negative.
3. **Fallback / Edge:** Câu hỏi ngoài phạm vi để chứng minh bot không bịa.

Không nên dùng Test #4, #16, #17 trong demo chính nếu chưa chỉnh lại, vì đây là các case đang cần xử lý.

## 6. Đề xuất cải thiện tiếp theo

Ưu tiên theo thứ tự:

1. **Sửa ground truth Test #16** để kết quả QA công bằng hơn.
2. **Sửa retrieval cho Test #4** vì đây là lỗi thật ảnh hưởng câu hỏi fact-based.
3. **Thêm rule fallback cho câu hỏi mơ hồ** như "ngày mai", "hôm nay", "bài này".
4. **Chạy lại bộ test sau khi sửa** và tạo log mới để so sánh trước / sau.
5. **Chụp screenshot demo** cho 3 case: fact-based, reasoning, fallback.

## 7. Kết luận QA

Hệ thống hiện đạt **17/20 PASS, accuracy sơ bộ 85%**, phù hợp để demo ở mức prototype. Chatbot trả lời tốt với phần lớn câu hỏi trong phạm vi tài liệu Day 1-5 và có source. Các điểm cần cải thiện trước khi nộp/demo là retrieval của một câu Day 2, chỉnh lại một ground truth chưa công bằng, và làm fallback chặt hơn cho câu hỏi mơ hồ.

**Trạng thái đề xuất:** Demo-ready sau khi chọn case demo an toàn và ghi rõ các known issues.
