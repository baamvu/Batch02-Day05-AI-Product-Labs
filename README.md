# Day 05 Lab — AI IN ACTION Copilot

> Track A · Learning OS (Vin AI Thực Chiến) · Batch 02

RAG chatbot trả lời câu hỏi nội dung khoá học AI Thực Chiến, trả về answer + source + next action.

## Nhóm và phân công

| Tên | MSSV | Vai trò | Deliverable |
|---|---|---|---|
| Vũ Quốc Bảo | 2A202600541 | Data / Knowledge Base | chunks.jsonl, manifest.json, ChromaDB/vectorstore, retriever test chạy được |
| Vũ Văn Huy | 2A202600750 | Backend RAG + API | `ask_copilot(question)` → answer + source + next action |
| Nguyễn Trung Kiên | 2A202600969 | Frontend Streamlit UI | Giao diện chat demo chạy được |
| Lê Đình Sỹ | 2A202600770 | QA / Evaluation / Demo Test | Bộ câu hỏi test, test fallback, test accuracy, screenshot demo |
| Phạm Hoàng Anh Kiệt | 2A202600797 | README / Evidence / Thin SPEC / Presentation | README, evidence pack, thin spec, demo script |

## Tài liệu trong folder này

| Folder / File | Nội dung |
|---|---|
| `01-invidual-workshop/app-teardown.md` | Mổ app V-AI: vẽ flow, tìm path yếu, viết finding thành product decision. |
| `02-group-spec/evidence-pack-template.md` | Evidence pack: self-use + review + competitor, insight, opportunity. |
| `02-group-spec/synthesis-decide-toolkit.md` | Gom evidence → insight → opportunity → câu chốt build slice. |
| `02-group-spec/thin-spec-template.md` | Thin SPEC cuối Day 05: build slice, 4 paths, failure mode, owner plan. |

## Build slice

```text
Cho học viên AI Thực Chiến đang làm lab cần tra nhanh khái niệm/framework trong slide,
prototype dùng RAG để lấy đoạn liên quan từ ChromaDB và trả lời kèm nguồn (day + section),
tạo ra answer + source reference + gợi ý next action,
và xử lý câu ngoài scope bằng fallback rõ ràng thay vì hallucinate.
```

## Cấu trúc repo nộp bài Day 06

Mỗi học viên nộp **một repo cá nhân**:

```text
Day06-MãHọcViên-HọVàTên/
├── 01-invidual-workshop/
│   └── reflection.md
└── 02-group-spec/
    ├── spec-final.md
    ├── prototype-readme.md
    ├── demo-slides.pdf
    └── prompt-tests-or-failure-log.md
```

- `01-invidual-workshop/`: reflection cá nhân — vai trò, việc đã làm, phần AI hỗ trợ, bài học sau demo.
- `02-group-spec/`: bản làm chung của nhóm. Mỗi học viên copy bản cuối vào repo cá nhân.
