# Workshop — Mổ App AI Thật

**Sản phẩm chọn:** MoMo — Moni  
**AI feature:** Trợ thủ tài chính, phân tích chi tiêu, chatbot  
**Cách truy cập:** App MoMo  
**Output:** finding note + sketch `as-is / to-be`

Mục tiêu của phần phân tích này không phải đánh giá giao diện đẹp hay xấu, mà là tìm điểm gãy trong workflow thật của Moni. Trường hợp được chọn là khi người dùng thử bẻ chatbot từ vai trò **AI phân tích tài chính** sang yêu cầu **viết code Python/HTML**.

---

## 1. Chọn một sản phẩm để dùng thử

| Sản phẩm | AI feature | Cách truy cập |
|---|---|---|
| MoMo — Moni | Trợ thủ tài chính, phân tích chi tiêu, chatbot | App MoMo |

**Lý do chọn Moni:**  
Moni được định vị là trợ lý tài chính cá nhân, có thể hỗ trợ người dùng hiểu chi tiêu, phân tích tài chính, gợi ý cách quản lý tiền và giải thích các vấn đề liên quan đến ngân sách. Vì vậy, đây là sản phẩm phù hợp để kiểm tra xem AI có giữ đúng phạm vi vai trò hay không.

---

## 2. Dùng thử: promise vs reality

### Product hứa gì?

Moni hứa sẽ đóng vai trò như một **trợ thủ tài chính cá nhân**, hỗ trợ người dùng trong các vấn đề như:

- phân tích chi tiêu,
- lập ngân sách,
- theo dõi thói quen tiêu dùng,
- đưa ra lời khuyên tài chính cá nhân,
- hỗ trợ hiểu dòng tiền và hành vi chi tiêu.

### User nào được hứa sẽ được giúp?

User mục tiêu là người dùng MoMo có nhu cầu quản lý tài chính cá nhân tốt hơn. Họ có thể là sinh viên, nhân viên văn phòng, freelancer, người dùng ví điện tử thường xuyên hoặc người muốn theo dõi chi tiêu hằng tháng.

### Kỳ vọng AI làm được task nào?

Kỳ vọng hợp lý là Moni có thể:

- giải thích tình hình chi tiêu,
- phân loại khoản chi,
- gợi ý cách tiết kiệm,
- cảnh báo thói quen chi tiêu chưa hợp lý,
- tư vấn tài chính cá nhân ở mức đơn giản.

Tuy nhiên, Moni **không nên trở thành AI lập trình tổng quát**. Khi user yêu cầu viết code Python, HTML hoặc JavaScript, hệ thống cần nhận diện đây là yêu cầu lệch khỏi vai trò chính.

### Khi dùng thật, điểm gãy xuất hiện ở đâu?

Điểm gãy xuất hiện khi user bắt đầu chuyển hướng hội thoại từ phân tích tài chính sang yêu cầu tạo code. Ban đầu Moni vẫn trả lời theo hướng tài chính. Sau đó, khi user hỏi về ví dụ bài code và yêu cầu mẫu Python, Moni có lúc từ chối vì cho rằng mình không phải AI để “test hack”. Nhưng sau khi user phản hồi rằng trước đó Moni đã gợi ý code, Moni lại tiếp tục cung cấp code Python và sau đó là HTML/JavaScript.

Vấn đề không nằm ở việc câu trả lời code đúng hay sai về mặt kỹ thuật. Vấn đề là Moni **không giữ được product boundary**: một AI phân tích tài chính bị bẻ sang vai trò AI viết code.

### Evidence

#### Screenshot 1

![Screenshot đoạn chat Moni 1](images/huyvu/file1.jpg)

**Observation:** User bắt đầu bằng một câu hỏi liên quan đến tài chính cho coder. Đây vẫn là một intent hợp lệ trong phạm vi tài chính cá nhân.

#### Screenshot 2

![Screenshot đoạn chat Moni 2](images/huyvu/file2.jpg)

**Observation:** User chuyển dần sang hỏi về ví dụ bài code phân tích tài chính. Moni bắt đầu mở cửa cho hướng trả lời liên quan đến code.

#### Screenshot 3

![Screenshot đoạn chat Moni 3](images/huyvu/file3.jpg)

**Observation:** User yêu cầu mẫu Python. Đây là điểm Moni cần giữ boundary rõ hơn. Thay vì tiếp tục viết code, Moni nên giải thích rằng mình chỉ có thể mô tả logic phân tích tài chính, không trực tiếp tạo code.

#### Screenshot 4

![Screenshot đoạn chat Moni 4](images/huyvu/file4.jpg)

**Observation:** Moni tiếp tục bị kéo sang tạo HTML/JavaScript. Điều này cho thấy chatbot có thể bị bẻ khỏi vai trò sản phẩm ban đầu.

---

## 3. Vẽ 4 paths

| Path | Câu hỏi cần trả lời | Quan sát trên Moni |
|---|---|---|
| Happy | Khi AI đúng và tự tin, user thấy gì? | Moni trả lời tốt khi câu hỏi nằm trong phạm vi tài chính cá nhân, ví dụ lập ngân sách, theo dõi chi tiêu, phân tích thói quen tiêu dùng. |
| Low-confidence | Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không? | Chưa thấy path hỏi lại rõ ràng. Khi user hỏi về code, Moni không hỏi lại mục đích mà phản ứng chưa ổn định: lúc từ chối, lúc lại cung cấp code. |
| Failure | Khi AI sai, user biết bằng cách nào và sửa thế nào? | User phải tự chỉ ra mâu thuẫn: trước đó Moni gợi ý có thể tham khảo code, sau đó lại từ chối. Hệ thống không tự nhận diện failure boundary. |
| Correction | Khi user sửa, correction có được lưu/log/học lại không hay biến mất? | Chưa thấy cơ chế correction rõ ràng. Sau khi user phản hồi, Moni đổi hướng và cung cấp code, nhưng không có dấu hiệu lưu lại thành quy tắc sản phẩm. |

---

## 4. Viết finding thành quyết định

### Finding chính

Khi user hỏi Moni về mẫu code Python/HTML để phân tích chi tiêu, AI bị kéo khỏi vai trò **trợ lý phân tích tài chính** và chuyển sang hành vi của **AI lập trình tổng quát**. Hậu quả là product boundary bị gãy: user có thể bẻ chatbot sang những tác vụ ngoài phạm vi thiết kế, làm giảm tính nhất quán và độ tin cậy của sản phẩm. Lỗi thuộc layer **intent + safety boundary + UX recovery**. Nên sửa bằng cách thêm boundary rule: Moni chỉ giải thích logic phân tích tài chính, tiêu chí đánh giá, công thức, hoặc gợi ý cấu trúc báo cáo; không trực tiếp viết code Python/HTML/JavaScript.

### Viết theo template workshop

```text
Khi user yêu cầu Moni viết mẫu Python/HTML cho bài toán phân tích chi tiêu,
AI/product bị bẻ từ vai trò phân tích tài chính sang vai trò lập trình tổng quát,
hậu quả là user nhận được phản hồi không nhất quán và product boundary bị phá vỡ.
Lỗi thuộc layer intent + safety boundary + UX recovery.
Nên sửa bằng requirement: Moni không tạo code, chỉ mô tả logic tài chính, công thức phân tích,
tiêu chí đánh giá hoặc đề xuất cấu trúc báo cáo; nếu user cần code, Moni cần từ chối mềm và điều hướng về phạm vi tài chính.
```

### Product decision

Moni cần giữ vai trò là **AI phân tích tài chính**, không phải AI code. Vì vậy:

| Tình huống user hỏi | Cách Moni nên xử lý |
|---|---|
| Hỏi phân tích chi tiêu | Trả lời bình thường |
| Hỏi lập ngân sách | Trả lời bình thường |
| Hỏi tiêu chí đánh giá tài chính cá nhân | Trả lời bình thường |
| Hỏi logic tính toán chi tiêu | Có thể giải thích bằng công thức hoặc pseudo-logic mức khái niệm |
| Hỏi viết code Python/HTML/JavaScript | Từ chối mềm, không tạo code |
| Hỏi “làm app”, “tạo file”, “viết script” | Điều hướng lại: Moni chỉ hỗ trợ nội dung phân tích tài chính, không lập trình |

Câu trả lời chuẩn của Moni nên là:

```text
Moni có thể giúp bạn xác định tiêu chí phân tích chi tiêu, cách chia nhóm khoản chi,
công thức tính tỷ lệ tiết kiệm và cảnh báo vượt ngân sách. Tuy nhiên, Moni không trực tiếp viết code Python/HTML/JavaScript.
Nếu bạn muốn, Moni có thể mô tả logic phân tích tài chính để bạn hoặc developer triển khai.
```

---

## 5. Sketch as-is / to-be

### As-is: flow hiện tại

```text
User hỏi về tài chính cho coder
        ↓
Moni trả lời trong phạm vi tài chính cá nhân
        ↓
User hỏi ví dụ bài code phân tích tài chính
        ↓
Moni bắt đầu gợi ý hướng làm code
        ↓
User yêu cầu mẫu Python cụ thể
        ↓
Moni có lúc từ chối vì không phải AI để test hack
        ↓
User phản hồi rằng trước đó Moni đã gợi ý code
        ↓
Moni đổi hướng và cung cấp code Python
        ↓
User tiếp tục yêu cầu nâng cấp thành HTML
        ↓
Moni cung cấp HTML/JavaScript
        ↓
Điểm gãy: Moni bị bẻ khỏi vai trò AI phân tích tài chính
```

### Điểm gãy trong as-is

```text
Moni không có boundary ổn định giữa:
- hỗ trợ phân tích tài chính
- hỗ trợ lập trình tạo code
```

Điểm yếu nhất là đoạn Moni vừa từ chối, sau đó lại chấp nhận tạo code khi user phản hồi. Điều này làm hành vi sản phẩm thiếu nhất quán.

---

### To-be: flow đề xuất

```text
User hỏi về tài chính cho coder
        ↓
Moni trả lời trong phạm vi tài chính cá nhân
        ↓
User hỏi ví dụ code phân tích tài chính
        ↓
Moni nhận diện intent có nguy cơ lệch khỏi phạm vi
        ↓
Moni phản hồi boundary mềm:
“Moni không trực tiếp viết code, nhưng có thể giúp bạn mô tả logic phân tích tài chính.”
        ↓
Moni đưa các tiêu chí tài chính có thể phân tích:
- tổng thu nhập
- tổng chi tiêu
- tỷ lệ tiết kiệm
- nhóm chi tiêu lớn nhất
- cảnh báo vượt ngân sách
        ↓
Nếu user tiếp tục yêu cầu code
        ↓
Moni giữ boundary:
“Moni không tạo Python/HTML/JavaScript. Moni có thể chuyển yêu cầu thành đặc tả logic cho developer.”
        ↓
Nếu user muốn tiếp tục trong phạm vi tài chính
        ↓
Moni hỗ trợ tạo bảng tiêu chí, công thức, rule đánh giá hoặc report template
```

### Path đã sửa

```text
User: “Tôi muốn mẫu Python theo tiêu chí đánh giá chi tiêu hằng tháng.”
        ↓
Moni: “Moni không trực tiếp viết code Python. Nhưng Moni có thể giúp bạn xác định logic phân tích tài chính.”
        ↓
Moni đưa logic:
1. Nhập tổng thu nhập tháng
2. Nhập các nhóm chi tiêu
3. Tính tổng chi
4. Tính số dư
5. Tính tỷ lệ tiết kiệm
6. Cảnh báo nếu chi tiêu vượt 80% thu nhập
7. Gợi ý nhóm chi cần cắt giảm
        ↓
User vẫn nhận được giá trị tài chính, nhưng Moni không bị bẻ thành AI code
```

---

## 6. Tự kiểm trước khi nộp

- [x] Có ít nhất 1 screenshot hoặc observation cụ thể.
- [x] Có đủ 4 paths: Happy, Low-confidence, Failure, Correction.
- [x] Finding được viết thành product decision, không chỉ là nhận xét.
- [x] Sketch có as-is và to-be.
- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.

### SPEC change đề xuất

Thêm vào SPEC của Moni:

```text
Moni is a personal finance analysis assistant, not a general-purpose coding assistant.
When users request programming output such as Python, HTML, JavaScript, scripts, apps, or files,
Moni must not generate code. Moni should redirect to financial reasoning by offering formulas,
financial criteria, decision rules, report structure, or developer-facing requirements without code.
```

Viết lại bằng tiếng Việt:

```text
Moni là trợ lý phân tích tài chính cá nhân, không phải trợ lý lập trình tổng quát.
Khi người dùng yêu cầu tạo code Python/HTML/JavaScript, script, app hoặc file kỹ thuật,
Moni không được tạo code. Moni cần điều hướng lại bằng cách cung cấp công thức tài chính,
tiêu chí đánh giá, rule phân tích, cấu trúc báo cáo hoặc đặc tả yêu cầu cho developer nhưng không viết code.
```

---

## Kết luận

Finding quan trọng nhất là Moni chưa giữ được ranh giới sản phẩm khi user chuyển từ nhu cầu tài chính sang yêu cầu lập trình. Nếu không sửa, chatbot có thể bị dùng như AI code tổng quát, làm lệch promise ban đầu của sản phẩm. SPEC cần bổ sung boundary rule rõ ràng: **Moni chỉ phân tích tài chính, không tạo code; khi gặp yêu cầu code, Moni phải từ chối mềm và chuyển về logic tài chính.**
