# Workshop — Mổ App AI Thật

**Sản phẩm được chọn: MoMo — Moni**
* **Người thực hiện:** Nguyễn Trung Kiên - 2A202600969


---

## 1. Chọn một sản phẩm để dùng thử

| Sản phẩm | AI feature | Cách truy cập |
| :--- | :--- | :--- |
| **MoMo — Moni** | **Trợ thủ tài chính, phân tích chi tiêu, chatbot** | **App MoMo** |
| Vietnam Airlines — NEO | Chatbot hỗ trợ vé, hành lý, khiếu nại | Website/Zalo VNA |
| V-App — V-AI | Trợ lý voice/text, gợi ý theo ngữ cảnh | App V-App |

**Lý do chọn:** Moni được định vị là một "Trợ thủ tài chính cá nhân thông minh". Kỳ vọng cốt lõi của người dùng là Moni có thể hiểu dữ liệu chi tiêu thật, giúp phân tích dòng tiền, quản lý ngân sách và đưa ra các đề xuất tích lũy thông minh dựa trên hệ sinh thái sẵn có của MoMo (Túi Thần Tài, Chứng chỉ quỹ, Quản lý chi tiêu).

## 2. Dùng thử: promise vs reality

### 2.1. Product hứa gì?
* Tự động phân tích, phân loại các khoản chi tiêu hàng tháng qua ví.
* Tương tác bằng hội thoại tự nhiên để giải đáp các thắc mắc về tài chính cá nhân.
* Đưa ra lời khuyên, gợi ý quản lý tài chính thông minh gắn liền với ngữ cảnh người dùng.

### 2.2. User nào được hứa sẽ được giúp?
* Người dùng ví điện tử MoMo có nhu cầu quản lý dòng tiền và theo dõi thói quen chi tiêu.
* Sinh viên, người đi làm muốn tìm kiếm giải pháp tích lũy hiệu quả từ số vốn nhỏ.

### 2.3. Kỳ vọng AI làm được task nào?
1. **Phân tích và tối ưu hóa ngân sách:** Đọc hiểu lịch sử giao dịch thật, chỉ ra khoản chi vượt mức dựa trên dữ liệu thực tế.
2. **Định hướng giải pháp tài chính thực tế:** Khéo léo kết nối với các công cụ tài chính nội bộ trong app MoMo (Túi Thần Tài, Chứng chỉ quỹ) khi user phát sinh nhu cầu tăng tài sản.
3. **Giữ đúng phạm vi (Guardrails):** Tập trung hoàn toàn vào các bài toán tài chính, không đi lệch sang các chủ đề lan man khác.

### 2.4. Prompt/input đã thử thực tế
> **Query 1:** "tôi muốn kiếm nhiều tiền như elon mu"
> **Query 2:** "thế banh giúp tôi tạo 1 roadmap ngon như ô đấy đi"
> **Query 3:** "mới thôi từ đầu đi"

### 2.5. Hành vi quan sát được (Observations)
* **Observation 1 — Lỗi Tràn phạm vi (Scope Creep):** Khi user hỏi câu mang tính vĩ mô về cách làm giàu như Elon Musk, Moni thiếu bộ lọc Guardrails để kéo user về lại chức năng ví. AI bị cuốn theo câu chuyện ngoài lề, đưa ra lời khuyên chung chung mang tính triết lý giáo điều thay vì liên kết đến sản phẩm đầu tư/tích lũy nội bộ.
* **Observation 2 — Biến thành Chatbot đa năng phân cấp thấp:** Khi user đòi xin roadmap, Moni đánh mất hoàn toàn nhận thức ngữ cảnh (Context-awareness). AI lại đi khạc ra một bài giảng về lập trình và tự sinh các đoạn code ví dụ bằng Python (tính tổng từ 1 đến n) ngay trên giao diện chat.
* **Observation 3 — Trải nghiệm đứt gãy nặng nề (Technical Overflow):** Tại query cuối, Moni hiển thị nguyên một khối mã nguồn dài dằng dặc bao gồm HTML, CSS, và JavaScript mô phỏng giao diện ví. Việc nhìn thấy các thẻ code hệ thống là một trải nghiệm cực kỳ tệ, rối mắt và vô dụng đối với một người dùng ví điện tử mobile.

## 3. Vẽ 4 paths

| Path | Câu hỏi cần trả lời | Quan sát trên MoMo Moni |
| :--- | :--- | :--- |
| **Happy** | Khi AI đúng và tự tin, user thấy gì? | AI hiển thị code block và văn bản rất nhanh. Tuy nhiên, nó lại "đúng" ở tác vụ viết code hộ chứ không phải tài chính. |
| **Low-confidence** | Khi AI không chắc, hệ thống có hỏi lại không? | Chưa có bộ lọc Out-of-Scope. AI tự ý chém gió lan man, bị cuốn theo user thay vì từ chối khéo léo. |
| **Failure** | Khi AI sai, user sửa bằng cách nào? | AI khạc ra mớ code phá vỡ UI chat. User hoàn toàn bất lực, không biết bấm vào đâu để quay lại luồng chính. |
| **Correction** | Khi user sửa, correction có được lưu không? | Không có nút hiệu chỉnh, câu lệnh sửa lỗi của user ("mới thôi từ đầu đi") chỉ làm AI lún sâu hơn vào việc giải thích code. |

## 4. Finding thành quyết định product

**Finding 1 — AI tự tin trả lời sai phạm vi chức năng (Scope Creep):**
> Khi user nhập các câu hỏi vĩ mô hoặc trêu đùa về tài chính ("muốn giàu như Elon Musk"), AI vẫn cố gắng đóng vai bách khoa toàn thư để trả lời lan man và tự động sinh code lập trình không liên quan, hậu quả là phá vỡ lời hứa sản phẩm, gây nhiễu giao diện mobile và mất mục tiêu chuyển đổi khách hàng. Lỗi thuộc layer Intent Classification + Guardrail + UX Recovery. Nên sửa bằng requirement: Kích hoạt bộ lọc Out-of-Scope. AI phải từ chối ngắn gọn và hiển thị các nút định hướng hành động tài chính thực tế.

* **Product decision:** Cần ưu tiên thiết lập cơ chế **strict scope restriction (giới hạn phạm vi nghiêm ngặt)**. Tuyệt đối cấm render các đoạn mã nguồn dài dòng, bắt buộc phải quy đổi mọi thắc mắc của user về các hành động tài chính tương thích trong app.

**Finding 2 — Thiếu hụt cơ chế Chuyển giao ngữ cảnh (Context Handoff):**
> Khi user hỏi về cách tích lũy, đầu tư hay roadmap làm giàu, AI trả lời thuần túy bằng văn bản chung chung giống hệt chatbot nguồn mở, không gọi bất kỳ công cụ nội bộ nào, hậu quả là sản phẩm không tạo ra chuyển đổi kinh doanh (Conversion Rate) cho các dịch vụ tài chính của MoMo. Lỗi thuộc layer Data-tool + Business Logic. Nên sửa bằng bộ liên kết Deep-link hoặc Nút hành động dẫn trực tiếp tới sản phẩm tương ứng trong app.

* **Product decision:** Moni phải hoạt động như một **business-driven assistant**. Mọi câu trả lời liên quan đến tiền bạc đều phải được cấu trúc để handoff mượt mà về các tính năng lõi (Túi Thần Tài, Chứng chỉ quỹ).

## 5. Sketch as-is / to-be (Luồng xử lý câu hỏi ngoài phạm vi)

| Luồng Hiện tại (As-is Flow) | Luồng Đề xuất (To-be Flow) |
| :--- | :--- |
| 1. User hỏi: Muốn giàu như Elon Musk, xin roadmap | 1. User hỏi: Muốn giàu như Elon Musk, xin roadmap |
| 2. Moni nhận diện sai intent / Cho phép chat tự do (Fail) | 2. Kích hoạt bộ kiểm tra phạm vi (Guardrail Check) (Success) |
| 3. Moni bị cuốn theo câu chuyện dạy lập trình, học code | 3. Moni kích hoạt Out-of-Scope Path (Từ chối viết code) |
| 4. Tràn ngập code HTML/JS... | 4. AI phản hồi ngắn gọn: "Để giàu như Elon, hãy bắt đầu tích lũy từ 10.000đ ngay hôm nay" |
| 5. User bị ngợp, rối mắt và kẹt hoàn toàn trong khung chat (Fail) | 5. Hiển thị các Nút hành động: [Mở Túi Thần Tài] / [Quản lý Chi tiêu] (Success) |

## 6. SPEC change đề xuất

* **Requirement 1 — Out-of-Scope Guardrail Control:** Hệ thống bắt buộc phải chặn mọi query không liên quan đến tài chính cá nhân, ngân sách, hoặc dịch vụ của MoMo. AI phải từ chối viết code hoặc làm bài tập hộ.
* **Requirement 2 — Output Format Restriction:** Moni tuyệt đối không được render mã nguồn thô (Python, HTML, JS) lên màn hình chat mobile dưới bất kỳ hình thức nào.
* **Requirement 3 — Hệ thống Nút hành động bắt buộc (Mandatory Contextual Handoff):**

| Từ khóa hệ thống nhận diện | Nút bấm hành động (Deep-link Button) tương ứng |
| :--- | :--- |
| "Kiếm tiền", "Tích lũy", "Giàu" | **[Mở Túi Thần Tài]** |
| "Đầu tư", "Sinh lời" | **[Mở Chứng Chỉ Quỹ]** |
| "Roadmap", "Học quản lý" | **[Mở Quản Lý Chi Tiêu MoMo]** |