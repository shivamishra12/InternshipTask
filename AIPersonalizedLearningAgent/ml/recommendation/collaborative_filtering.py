import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def fit_similarity(R):
    """
    Computes the Item-Item Cosine Similarity Matrix from the User-Item matrix R.
    
    R: SciPy sparse matrix or dense array of shape (num_students, num_sites)
    
    Returns:
        S: Dense numpy array of shape (num_sites, num_sites) containing
           item-to-item cosine similarity scores.
    """
    print("Fitting Collaborative Filtering similarity matrix...")
    # R is (users, items). R.T is (items, users)
    # Cosine similarity on columns of R (which are rows of R.T)
    S = cosine_similarity(R.T, dense_output=True)
    
    # Fill diagonal with 0 to prevent recommending the item itself
    np.fill_diagonal(S, 0.0)
    
    # Replace negative values with 0 (cosine similarity can be negative, 
    # but for recommendation we only care about positive correlation)
    S = np.clip(S, 0.0, None)
    
    print(f"  Similarity matrix calculated. Shape: {S.shape}")
    return S

if __name__ == "__main__":
    from scipy.sparse import csr_matrix
    R_test = csr_matrix([
        [1.0, 0.0, 5.0],
        [0.0, 2.0, 1.0],
        [3.0, 3.0, 0.0]
    ])
    S = fit_similarity(R_test)
    print("Item Similarity Matrix:")
    print(S)
