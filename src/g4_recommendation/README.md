# 🎯 Group 4: Recommendation & Evaluation (Tầng Scoring & Metrics)

Nhiệm vụ cốt lõi: **Thuật toán chấm điểm Match giữa CV - Job -> Xếp hạng Top K -> Đo lường độ chính xác (Metrics) bằng Ground Truth.**

## 🗺️ 1. Luồng dữ liệu (Data Workflow)

1. **Scoring Engine (`scoring.py`)**: Lấy danh sách skill của CV -> So sánh với danh sách skill của hàng ngàn Jobs -> Tính điểm (0-1).
2. **Top-K Ranking**: Sắp xếp điểm giảm dần -> Lấy K jobs cao nhất -> Trả kết quả chuẩn JSON.
3. **Evaluation (`evaluation.py`)**: Chạy vòng lặp tính điểm cho tập Test (Ground Truth) -> Tính chỉ số Recall@K, Precision@K, Pass@K.

---

## 📋 2. Đặc tả công việc chi tiết (Tasks)

### Module 4.1: Thuật toán Chấm điểm (Scoring Engine)
*   **Vị trí code:** `src/g4_recommendation/scoring.py`
*   **Input:** `candidate_skills` (G3) và `job_skills` (G2).
*   **Output:** Điểm số Final Score (float).
*   **Hướng dẫn thuật toán:**
    *   **Base model:** Dùng **Jaccard Similarity** trên tập `skill_id`.
    *   **Advanced model:** Tính **Weighted Jaccard** hoặc **TF-IDF**. Skill hiếm (như CUDA) trùng nhau thì cộng nhiều điểm hơn skill phổ thông (như Git, Word).
    *   **Ưu tiên tuyệt đối:** Các skill bên bảng ứng viên có `user_confirmed = True` phải được giữ nguyên weight = 1.0 khi tính toán.

### Module 4.2: Đánh giá Model (Evaluation)
*   **Vị trí code:** `src/g4_recommendation/evaluation.py`
*   **Input:** Bảng `evaluation_ground_truth` (Do team tự gán nhãn tay).
*   **Output:** In ra Console các chỉ số đo lường.
*   **Metrics cần tính:**
    *   **Recall@10:** Trong các Job thực sự phù hợp với CV này (nhãn >= 2), thuật toán đưa được bao nhiêu % vào Top 10?
    *   **Precision@10:** Trong 10 Job thuật toán gợi ý, có bao nhiêu Job thực sự phù hợp?
    *   **Pass@10 (Hit Rate):** Trong Top 10 trả về, có *ít nhất 1 Job* phù hợp không? (0 hoặc 1).

---

## 🔒 3. Data Contract (Hợp đồng Dữ liệu)

Kết quả trả về cho Frontend (hoặc API) **bắt buộc** phải tuân theo schema `RecommendationResult`. Không trả về DataFrame hay Array trần trụi.

```python
from src.shared.schemas import RecommendationResult, RecommendationExplanation

def get_recommendations(candidate_id: str, top_k: int = 5) -> list[RecommendationResult]:
    # 1. [Logic gọi DB lấy CV skills và toàn bộ Job skills]
    # 2. [Logic tính final_score]
    
    results = []
    # Loop qua các jobs đã chấm điểm và được sắp xếp giảm dần:
    for rank, (job_id, final_score, matched, missing) in enumerate(top_jobs[:top_k]):
        
        # 3. Tạo lời giải thích
        explanation = RecommendationExplanation(
            reason=f"CV khớp {len(matched)} kỹ năng quan trọng của Job.",
            matched_score=round(final_score, 2)
        )
        
        # 4. Map vào Pydantic Contract
        rec = RecommendationResult(
            candidate_id=candidate_id,
            job_id=job_id,
            rank=rank + 1,
            score=round(final_score, 4),
            matched_skills=matched, # List skill_id
            missing_skills=missing, # List skill_id
            role_affinity=1.0,
            level_fit=1.0,
            explanation=explanation
        )
        results.append(rec)
        
    return results
```

---

## 🚀 4. To-do List
1. [ ] Đọc file `src/shared/schemas/evaluation.py` để hiểu format output.
2. [ ] Viết hàm tính **Jaccard Index** giữa 2 set `skill_id`.
3. [ ] Nâng cấp hàm chấm điểm bằng cách nhân thêm IDF (Inverse Document Frequency).
4. [ ] Lập file script nhỏ, lôi 50 CV và 50 Job ra ngồi gán nhãn thủ công (1-3) ném vào bảng `evaluation_ground_truth`.
5. [ ] Viết hàm tính Recall@K, Precision@K từ kết quả của thuật toán đối chiếu với bộ test chuẩn.