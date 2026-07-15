import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

def build_user_item_matrix(df, student_list=None, site_list=None):
    """
    Builds a SciPy CSR sparse user-item interaction matrix from a DataFrame.
    Applies log1p scaling on click counts.
    
    df: DataFrame containing ['id_student', 'id_site', 'sum_click']
    student_list: list/array of unique student IDs (optional)
    site_list: list/array of unique site IDs (optional)
    
    Returns:
        R: SciPy CSR sparse matrix of shape (num_students, num_sites)
        student_to_idx: dict mapping student_id -> row_index
        site_to_idx: dict mapping site_id -> col_index
        idx_to_student: array mapping row_index -> student_id
        idx_to_site: array mapping col_index -> site_id
    """
    print("Building User-Item Sparse Matrix...")
    
    if student_list is None:
        student_list = sorted(df['id_student'].unique())
    if site_list is None:
        site_list = sorted(df['id_site'].unique())
        
    student_to_idx = {sid: idx for idx, sid in enumerate(student_list)}
    site_to_idx = {sid: idx for idx, sid in enumerate(site_list)}
    
    idx_to_student = np.array(student_list)
    idx_to_site = np.array(site_list)
    
    num_students = len(student_list)
    num_sites = len(site_list)
    
    # Map IDs to codes
    # Filter rows that might not be in the mapping (if mappings are pre-defined from train)
    valid_rows = df[df['id_student'].isin(student_to_idx) & df['id_site'].isin(site_to_idx)]
    
    rows = valid_rows['id_student'].map(student_to_idx).values
    cols = valid_rows['id_site'].map(site_to_idx).values
    
    # Log1p clicks scaling
    clicks = np.log1p(valid_rows['sum_click'].values)
    
    # Build CSR matrix
    R = csr_matrix((clicks, (rows, cols)), shape=(num_students, num_sites), dtype=np.float32)
    
    print(f"  Matrix shape: {R.shape} | Non-zero count: {R.nnz}")
    return R, student_to_idx, site_to_idx, idx_to_student, idx_to_site

if __name__ == "__main__":
    # Small test
    test_df = pd.DataFrame({
        'id_student': [101, 101, 102, 103],
        'id_site': [1, 2, 2, 3],
        'sum_click': [10, 5, 20, 1]
    })
    
    R, s_map, i_map, s_idx, i_idx = build_user_item_matrix(test_df)
    print("Dense equivalent:")
    print(R.toarray())
    print("Student index for 101:", s_map[101])
