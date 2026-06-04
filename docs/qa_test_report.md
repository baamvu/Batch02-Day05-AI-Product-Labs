# QA / Evaluation Report - AI IN ACTION Copilot

**Nguoi phu trach:** Lê Sỹ - Người 4    QA / Evaluation / Demo Test  
**Ngay chay test:** 2026-06-04  
**File log:** `C:\Users\Asus\AI_Labs\Day06-C401-Vinflow\codebase\data\logs\test_results_20260604_112552.csv`  
**Bo test:** `data/test_cases.csv`

## 1. Muc tieu test

Kiem tra AI Copilot tren bo cau hoi `test_cases.csv` de danh gia:

- Kha nang tra loi cau hoi fact-based dua tren tai lieu Day 1-5.
- Kha nang suy luan / so sanh dua tren framework trong bai hoc.
- Kha nang fallback khi cau hoi ngoai pham vi, thieu du lieu hoac mo ho.
- Chatbot co tra loi kem source va next action hay khong.
- Do tre cua tung cau tra loi khi chay demo.

## 2. Ket qua tong quan

| Chi so | Ket qua |
|---|---:|
| Tong so test cases | 20 |
| PASS | 17 |
| FAIL | 3 |
| PARTIAL | 0 |
| Accuracy so bo | 85% |
| Latency trung binh | ~21s |
| Case cham nhat | Test #3 - ~133s |

Nhan dinh nhanh: He thong dang du tot de demo prototype. Da so cau hoi fact-based va reasoning tra loi dung y chinh, co source. Cac loi con lai tap trung vao retrieval miss va fallback voi cau hoi mo ho.

## 3. Cac case FAIL can xem xet

### Test #4 - Retrieval miss

**Loai:** Fact-based (Day 2)  
**Cau hoi:** Ba muc giai phap he thong AI duoc de cap trong Day 2 la gi?  
**Ground truth:** Rule / Script, LLM Feature, va Agent.  
**Ket qua thuc te:** Bot noi context khong co thong tin nay va lay nham sang cac doan ve `Model + Context + Planning + Tools` va ly do doanh nghiep dau tu AI.

**Danh gia:** Loi retrieval that. Cau hoi ro rang, ground truth dung, nhung retriever khong dua dung chunk Day 2 slide 28 vao context.

**Huong xu ly:**

- Kiem tra chunk Day 2 slide 28 co nam trong `chunks.jsonl` khong.
- Tang `top_k` khi goi `ask_copilot`, vi hien tai dang dung `top_k=3`.
- Neu cau hoi co nhac `Day 2`, dam bao filter theo `day2` hoat dong dung.
- Co the them keyword vao chunk hoac cai thien chunking de cum "Rule / Script, LLM Feature, Agent" de tim hon.

### Test #16 - Ground truth can chinh lai

**Loai:** Edge Case (Thieu du lieu)  
**Cau hoi:** Ai la giang vien phu trach dung lop Day 3?  
**Ground truth hien tai:** Yeu cau fallback, noi chi co ten Pham Manh va khong co profile/lien he.  
**Ket qua thuc te:** Bot tra loi giang vien Day 3 la Pham Manh, den tu VinUniversity.

**Danh gia:** Bot khong sai nghiem trong. Tai lieu Day 3 co ghi giang vien la Pham Manh va don vi VinUniversity. Loi chinh nam o cach viet ground truth: cau hoi hoi "ai la giang vien", nen bot co the tra loi ten.

**Huong xu ly:**

- Neu muon test cau hoi fact-based, doi expected thanh:

```text
Giang vien phu trach Day 3 la Pham Manh. Tai lieu chi ghi them don vi VinUniversity, khong co profile hoac thong tin lien he chi tiet.
```

- Neu muon test thieu du lieu, doi cau hoi thanh:

```text
Profile hoac thong tin lien he cua giang vien Pham Manh la gi?
```

### Test #17 - Cau hoi mo ho / fallback chua tot

**Loai:** Edge Case (Mo ho)  
**Cau hoi:** Ngay mai phai nop bai tap thuc hanh nhu the nao?  
**Ground truth:** Bot nen hoi lai dang hoi bai tap cua Day nao.  
**Ket qua thuc te:** Bot noi context khong co format nop bai cu the, nhung sau do suy luan sang Day 6 va tra loi dai dua tren Day 5.

**Danh gia:** Day la loi ambiguity handling. Bot co dau hieu fallback mot phan, nhung van doan tiep qua nhieu.

**Huong xu ly:**

- Them rule vao system prompt: voi cau hoi dung thoi gian tuong doi nhu "hom nay", "ngay mai", "bai nay", neu khong co Day cu the thi hoi lai.
- Han che bot suy luan lich hoc neu context khong noi ro ngay hien tai cua nguoi dung.
- Giu case nay trong bo test de chung minh product co kiem tra low-confidence path.

## 4. Van de latency

Top case cham nhat:

| Test | Loai | Latency |
|---:|---|---:|
| #3 | Fact-based (Day 2) | ~133s |
| #11 | Reasoning | ~75s |
| #1 | Fact-based (Day 1) | ~34s |
| #10 | Fact-based (Day 5) | ~25s |
| #13 | Reasoning | ~21s |

Nhan xet: Latency trung binh bi keo cao boi mot vai case rat cham. Co the do lan dau load retriever / vectorstore, API LLM cham, hoac prompt context qua dai.

Huong xu ly:

- Khi demo, chay warm-up truoc bang 1 cau hoi don gian.
- Dung san 3 cau hoi demo da test PASS de tranh bat ngo.
- Neu can toi uu, giam context hoac gioi han chunk ngan hon.
- Ghi trong demo script rang day la prototype local/API nen latency co the dao dong.

## 5. Case nen dung de demo

Nen chon 3 case dai dien:

1. **Fact-based PASS:** Mot cau hoi Day 1/3/5 co answer dung va source ro.
2. **Reasoning PASS:** Cau hoi ve Agent loop, Automation vs Augmentation, hoac False Positive/False Negative.
3. **Fallback / Edge:** Cau hoi ngoai pham vi de chung minh bot khong bia.

Khong nen dung Test #4, #16, #17 trong demo chinh neu chua chinh lai, vi day la cac case dang can xu ly.

## 6. De xuat cai thien tiep theo

Uu tien theo thu tu:

1. **Sua ground truth Test #16** de ket qua QA cong bang hon.
2. **Sua retrieval cho Test #4** vi day la loi that anh huong cau hoi fact-based.
3. **Them rule fallback cho cau hoi mo ho** nhu "ngay mai", "hom nay", "bai nay".
4. **Chay lai bo test sau khi sua** va tao log moi de so sanh truoc / sau.
5. **Chup screenshot demo** cho 3 case: fact-based, reasoning, fallback.

## 7. Ket luan QA

He thong hien dat **17/20 PASS, accuracy so bo 85%**, phu hop de demo o muc prototype. Chatbot tra loi tot voi phan lon cau hoi trong pham vi tai lieu Day 1-5 va co source. Cac diem can cai thien truoc khi nop/demo la retrieval cua mot cau Day 2, chinh lai mot ground truth chua cong bang, va lam fallback chat hon cho cau hoi mo ho.

**Trang thai de xuat:** Demo-ready sau khi chon case demo an toan va ghi ro cac known issues.
