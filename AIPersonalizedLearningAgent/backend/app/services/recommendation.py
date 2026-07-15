import numpy as np
from app.core.exceptions import PredictionError
from app.services.model_loader import ModelLoader
from app.schemas.predict import RecommendationResponse, RecommendationItem
from app.config.logging_config import get_logger

logger = get_logger("recommendation_service")

class RecommendationService:
    @classmethod
    def predict(cls, student_id: int, k: int = 5) -> RecommendationResponse:
        """Generates Top-K resource recommendations for a student using Item-Based Collaborative Filtering."""
        logger.info(f"Generating recommendations for student {student_id} (k={k})...")
        
        try:
            # 1. Retrieve recommendation package and R matrix
            package = ModelLoader.get_recommendation_package()
            R = ModelLoader.get_recommendation_matrix_R()
            
            if package is None:
                raise PredictionError("Recommendation model package is not loaded in memory.")
                
            S = package["S"]
            student_to_idx = package["student_to_idx"]
            site_to_idx = package["site_to_idx"]
            idx_to_site = package["idx_to_site"]
            
            recs = []
            
            # 2. Check if student has interaction history or is cold start
            if R is None or student_id not in student_to_idx:
                logger.info(f"Student {student_id} is cold-start or R matrix is empty. Falling back to popularity recommendation.")
                if R is not None:
                    popularity = np.array(R.sum(axis=0)).flatten()
                    top_popular_indices = np.argsort(popularity)[::-1][:k]
                    
                    max_pop = popularity.max() if popularity.max() > 0 else 1.0
                    for rank, idx in enumerate(top_popular_indices):
                        recs.append(
                            RecommendationItem(
                                rank=rank + 1,
                                id_site=int(idx_to_site[idx]),
                                score=float(round(popularity[idx] / max_pop, 4)),
                                type="Popularity (Fallback)"
                            )
                        )
            else:
                # Collaborative Filtering recommendation
                u_idx = student_to_idx[student_id]
                r_u = R[u_idx].toarray().flatten()  # shape (num_sites,)
                
                if r_u.sum() == 0:
                    logger.info(f"Student {student_id} has zero click history in R. Falling back to popularity.")
                    popularity = np.array(R.sum(axis=0)).flatten()
                    top_popular_indices = np.argsort(popularity)[::-1][:k]
                    max_pop = popularity.max() if popularity.max() > 0 else 1.0
                    for rank, idx in enumerate(top_popular_indices):
                        recs.append(
                            RecommendationItem(
                                rank=rank + 1,
                                id_site=int(idx_to_site[idx]),
                                score=float(round(popularity[idx] / max_pop, 4)),
                                type="Popularity (Fallback)"
                            )
                        )
                else:
                    # scores = S * r_u
                    scores = S.dot(r_u)
                    
                    # Mask already interacted resources
                    interacted_mask = r_u > 0
                    scores[interacted_mask] = -np.inf
                    
                    # Get top k
                    top_indices = np.argsort(scores)[::-1][:k]
                    max_score = scores[top_indices[0]] if scores[top_indices[0]] > 0 else 1.0
                    
                    for rank, idx in enumerate(top_indices):
                        score = scores[idx]
                        if score == -np.inf:
                            score = 0.0
                        normalized_score = float(round(score / max_score, 4)) if max_score > 0 else 0.0
                        recs.append(
                            RecommendationItem(
                                rank=rank + 1,
                                id_site=int(idx_to_site[idx]),
                                score=normalized_score,
                                type="Collaborative Filtering"
                            )
                        )
                        
            logger.info(f"Generated {len(recs)} recommendations for student {student_id}")
            return RecommendationResponse(
                student_id=student_id,
                recommendations=recs
            )
            
        except Exception as e:
            logger.error(f"Error generating recommendations for student {student_id}: {str(e)}", exc_info=True)
            raise PredictionError(f"Recommendation generation failed: {str(e)}")
