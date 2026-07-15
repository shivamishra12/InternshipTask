import numpy as np

def recommend_top_k(student_id, R, S, student_to_idx, site_to_idx, idx_to_site, k=5):
    """
    Generates Top-K resource recommendations for a student using Item-Based CF.
    If the student has no history in the matrix (cold-start), falls back to 
    recommending the most popular resources overall.
    
    Returns:
        recommendations: list of dicts [{"rank": 1, "id_site": 1234, "score": 0.95}]
    """
    num_sites = len(idx_to_site)
    
    # 1. Cold-start check
    if student_id not in student_to_idx:
        # Fallback: Recommend most popular items in train matrix
        # Sum of log-clicks across all users
        popularity = np.array(R.sum(axis=0)).flatten()
        top_popular_indices = np.argsort(popularity)[::-1][:k]
        
        recs = []
        for rank, idx in enumerate(top_popular_indices):
            # Normalize popularity score to [0, 1] for presentation
            max_pop = popularity.max() if popularity.max() > 0 else 1.0
            recs.append({
                "rank": rank + 1,
                "id_site": int(idx_to_site[idx]),
                "score": float(round(popularity[idx] / max_pop, 4)),
                "type": "Popularity (Fallback)"
            })
        return recs
        
    # 2. Get student interaction vector
    u_idx = student_to_idx[student_id]
    r_u = R[u_idx].toarray().flatten()  # shape (num_sites,)
    
    # Check if user has zero clicks in train (edge case)
    if r_u.sum() == 0:
        # Fallback to popularity
        popularity = np.array(R.sum(axis=0)).flatten()
        top_popular_indices = np.argsort(popularity)[::-1][:k]
        recs = []
        for rank, idx in enumerate(top_popular_indices):
            max_pop = popularity.max() if popularity.max() > 0 else 1.0
            recs.append({
                "rank": rank + 1,
                "id_site": int(idx_to_site[idx]),
                "score": float(round(popularity[idx] / max_pop, 4)),
                "type": "Popularity (Fallback)"
            })
        return recs
        
    # 3. Compute predicted scores: scores = S * r_u
    # S is shape (num_sites, num_sites), r_u is shape (num_sites,)
    scores = S.dot(r_u)
    
    # 4. Mask already interacted resources
    interacted_mask = r_u > 0
    scores[interacted_mask] = -np.inf  # set to negative infinity so they are not recommended
    
    # 5. Retrieve top-K indices
    top_indices = np.argsort(scores)[::-1][:k]
    
    # Normalize score to [0, 1] for presentation relative to max score
    max_score = scores[top_indices[0]] if scores[top_indices[0]] > 0 else 1.0
    
    recs = []
    for rank, idx in enumerate(top_indices):
        score = scores[idx]
        if score == -np.inf:
            # Handle case where student has interacted with all items (unlikely)
            score = 0.0
        normalized_score = float(round(score / max_score, 4)) if max_score > 0 else 0.0
        recs.append({
            "rank": rank + 1,
            "id_site": int(idx_to_site[idx]),
            "score": normalized_score,
            "type": "Collaborative Filtering"
        })
        
    return recs

if __name__ == "__main__":
    from scipy.sparse import csr_matrix
    
    # Test data
    R_test = csr_matrix([
        [1.0, 0.0, 5.0],
        [0.0, 2.0, 0.0],
        [3.0, 3.0, 0.0]
    ])
    S_test = np.array([
        [0.0, 0.8, 0.2],
        [0.8, 0.0, 0.5],
        [0.2, 0.5, 0.0]
    ])
    s_map = {101: 0, 102: 1, 103: 2}
    i_map = {10: 0, 20: 1, 30: 2}
    idx_to_site = np.array([10, 20, 30])
    
    # Generate recommendations for student 102
    recs = recommend_top_k(102, R_test, S_test, s_map, i_map, idx_to_site, k=2)
    print("Recommendations for 102:", recs)
