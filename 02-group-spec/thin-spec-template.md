# Thin SPEC — AI IN ACTION Copilot

## 1. Track, product/app và user

**Track:** A · Learning OS (Vin AI Thực Chiến)  
**Product/app thật:** LMS khoá học + Discord lớp Batch 02  
**User cụ thể:** Học viên Batch 02 đang làm lab hoặc hackathon, cần tra nhanh khái niệm/framework từ nội dung khoá học  
**Nhóm có phải user thật không?** Có — tất cả thành viên đều là học viên Batch 02 đang dùng chính LMS và Discord này

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Cùng câu hỏi lặp ≥3 lần trong 30 phút hackathon | Discord #day05-batch02 (observation) | Học viên biết câu trả lời tồn tại trong slide nhưng không tìm ra nhanh | Build slice phải giải quyết "tra nhanh", không phải "học thêm" |
| Tra slide thủ công mất 3–5 phút, dùng sai từ khoá thì không ra | Self-use Day 3 lab | Slide không có semantic search; PDF không hỗ trợ tìm theo ý nghĩa | RAG là đúng tool — không phải full-text search |
| GitHub Copilot Chat: answer + source file:line là baseline tối thiểu | Competitor analysis | User không tin answer không có source | Response phải kèm source (Day X, section Y) |

## 3. Pain statement

```text
Học viên AI Thực Chiến đang làm lab hoặc hackathon (40 phút có áp lực)
gặp khó khi cần tra lại khái niệm/framework đã học,
vì ~300 trang slide (6 ngày) không có semantic search và Discord không tra được theo ngữ nghĩa,
dẫn tới mất 3–5 phút tra thủ công hoặc hỏi lặp lại trong Discord — làm gián đoạn flow làm việc.
Bằng chứng chính là Discord observation (≥3 câu hỏi trùng/buổi) và self-use timing.
```

## 4. Build slice

```text
Cho học viên Batch 02 đang làm lab và cần tra khái niệm từ nội dung khoá học,
prototype dùng RAG (ChromaDB + sentence-transformers) để tìm chunk liên quan nhất trong 6 ngày slide,
tạo ra answer + source reference (Day X, section Y) + gợi ý next action (đọc thêm / thử lab),
và xử lý câu hỏi ngoài scope khoá học bằng fallback rõ ràng ("không tìm thấy trong tài liệu khoá học")
thay vì hallucinate câu trả lời tự tin sai.
```

## 5. Auto/Aug decision

- [x] **Augmentation:** AI gợi ý answer + source, user tự verify và quyết định dùng hay không.
- [ ] Conditional automation
- [ ] Automation

**Lý do chọn:** Nội dung khoá học có thể thay đổi giữa các batch; học viên cần tự kiểm tra source để học. Sai trong context học tập ít hậu quả hơn sai trong production, nhưng vẫn cần source để user không phụ thuộc mù quáng vào AI.

**Human role:** Reviewer — AI draft answer, user đọc source để verify trước khi dùng vào bài nộp.

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | Câu hỏi rõ trong scope → trả answer có nguồn (Day X, section Y) + next action trong < 3 giây |
| Low-confidence | Câu hỏi mơ hồ hoặc score thấp → hiện "Tôi tìm được đoạn này, nhưng không chắc đủ liên quan — bạn xem thử?" kèm source để user tự phán |
| Failure | Câu hỏi ngoài scope hoàn toàn (hỏi về tin tức, kỹ thuật ngoài khoá) → "Không tìm thấy trong tài liệu khoá học AI Thực Chiến. Thử hỏi lại với từ khoá khác hoặc xem slide Day X." |
| Correction | User report "câu trả lời sai" → log câu hỏi + answer + source vào file correction_log.jsonl để Người 4 review |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user hỏi câu ngoài scope khoá học (ví dụ: "lãi suất ngân hàng hiện tại là bao nhiêu?"),
AI có thể hallucinate câu trả lời tự tin dựa trên training data,
hậu quả là user tin và dùng thông tin sai trong bài nộp.
Prototype sẽ xử lý bằng: kiểm tra similarity score — nếu top chunk score < threshold, trả fallback message thay vì generate answer.
Owner kiểm thử path này là Người 4 (QA).
```

## 8. Owner plan cho sáng Day 06

| Thành viên | MSSV | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|---|
| Vũ Quốc Bảo | 2A202600541 | Build ChromaDB từ 6 file day1–6.txt, chạy retriever test | `data/processed/chunks.jsonl`, `manifest.json`, retriever search demo |
| Vũ Văn Huy | 2A202600750 | Implement `ask_copilot(question)` → answer + source + next action | `src/retriever.py`, test chạy được từ terminal |
| Nguyễn Trung Kiên | 2A202600969 | Streamlit UI: input box, response area, source display | App chạy được tại localhost |
| Lê Đình Sỹ | 2A202600770 | Viết bộ 10 test cases (happy + low-confidence + failure), chạy và log kết quả | `prompt-tests-or-failure-log.md`, screenshot demo |
| Phạm Hoàng Anh Kiệt | 2A202600797 | README, evidence pack, thin spec, demo script 3 phút | README.md, file spec này, demo script nháp |
