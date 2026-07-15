import numpy as np
import pandas as pd
import math

def calculate_ndcg_at_k(recommended_items, test_items, k):
    """
    Computes Normalized Discounted Cumulative Gain at K (NDCG@K).
    """
    dcg = 0.0
    for idx, item in enumerate(recommended_items[:k]):
        if item in test_items:
            dcg += 1.0 / math.log2(idx + 2)
            
    idcg = 0.0
    num_hits = min(k, len(test_items))
    for idx in range(num_hits):
        idcg += 1.0 / math.log2(idx + 2)
        
    if idcg == 0.0:
        return 0.0
    return dcg / idcg

def evaluate_recommender(R_train, df_test, S, student_to_idx, site_to_idx, idx_to_site, k_list=[5, 10]):
    """
    Evaluates the collaborative filtering recommendation engine on the test set.
    """
    print("Evaluating recommender on test set...")
    
    # 1. Group test set by student
    test_targets = df_test.groupby('id_student')['id_site'].apply(set).to_dict()
    test_students = list(test_targets.keys())
    print(f"  Total test students to evaluate: {len(test_students)}")
    
    max_k = max(k_list)
    
    # Initialize metrics dictionary
    metrics = {k: {"precision": [], "recall": [], "ndcg": [], "hit_rate": []} for k in k_list}
    
    # Import recommendation function here to avoid circular imports
    from PersonalizedLearningAgent.ml.recommendation.recommend import recommend_top_k
    
    # Evaluate in batches or single loop
    count = 0
    for student_id in test_students:
        actual = test_targets[student_id]
        if len(actual) == 0:
            continue
            
        # Generate maximum K recommendations
        recs = recommend_top_k(student_id, R_train, S, student_to_idx, site_to_idx, idx_to_site, k=max_k)
        rec_ids = [r['id_site'] for r in recs]
        
        for k in k_list:
            slice_recs = rec_ids[:k]
            hits = len(set(slice_recs).intersection(actual))
            
            # Precision@K
            precision = hits / k
            # Recall@K
            recall = hits / len(actual)
            # Hit Rate@K
            hit_rate = 1.0 if hits > 0 else 0.0
            # NDCG@K
            ndcg = calculate_ndcg_at_k(slice_recs, actual, k)
            
            metrics[k]["precision"].append(precision)
            metrics[k]["recall"].append(recall)
            metrics[k]["ndcg"].append(ndcg)
            metrics[k]["hit_rate"].append(hit_rate)
            
        count += 1
        if count % 2000 == 0:
            print(f"  Evaluated {count}/{len(test_students)} students...")
            
    # Calculate average metrics
    summary = {}
    for k in k_list:
        summary[k] = {
            "Precision@K": float(np.mean(metrics[k]["precision"])),
            "Recall@K": float(np.mean(metrics[k]["recall"])),
            "NDCG@K": float(np.mean(metrics[k]["ndcg"])),
            "Hit Rate@K": float(np.mean(metrics[k]["hit_rate"]))
        }
        
    print("\nEvaluation Summary:")
    for k in k_list:
        print(f"  K = {k}:")
        for metric, val in summary[k].items():
            print(f"    {metric:<12}: {val:.4f}")
            
    return summary

if __name__ == "__main__":
    # Simple verification test
    from scipy.sparse import csr_matrix
    R_train = csr_matrix([
        [1.0, 0.0, 5.0],
        [0.0, 2.0, 0.0],
        [3.0, 3.0, 0.0]
    ])
    S = np.array([
        [0.0, 0.8, 0.2],
        [0.8, 0.0, 0.5],
        [0.2, 0.5, 0.0]
    ])
    s_map = {101: 0, 102: 1, 103: 2}
    i_map = {10: 0, 20: 1, 30: 2}
    idx_to_site = np.array([10, 20, 30])
    
    test_df = pd.DataFrame({
        'id_student': [102],
        'id_site': [30],
        'sum_click': [2]
    })
    
    summary = evaluate_recommender(R_train, test_df, S, s_map, i_map, idx_to_site, k_list=[1, 2])
