import pandas as pd
import numpy as np
from pathlib import Path

def load_and_preprocess_data(data_dir):
    """
    Loads studentVle.csv and vle.csv, merges them, groups by student/site, 
    and sums the clicks.
    """
    data_dir = Path(data_dir)
    print("Loading studentVle.csv and vle.csv...")
    student_vle = pd.read_csv(data_dir / "studentVle.csv")
    vle = pd.read_csv(data_dir / "vle.csv")
    
    print("Merging datasets on id_site...")
    merged = pd.merge(student_vle, vle, on="id_site", how="inner")
    
    print("Aggregating interactions (summing clicks per student per site)...")
    grouped = (merged.groupby(["id_student", "id_site", "activity_type"])["sum_click"]
               .sum()
               .reset_index())
    
    # Also create a site-to-activity-type lookup dictionary for reference
    site_info = vle.set_index("id_site")["activity_type"].to_dict()
    
    print(f"Preprocessed {len(grouped)} student-site interactions.")
    return grouped, site_info

def split_interactions(df_grouped, test_ratio=0.2, seed=42):
    """
    Splits student-site interactions into Train (80%) and Test (20%) sets.
    Performs a student-stratified split so that each student in the test set
    has history in the train set.
    """
    print(f"Splits student-site interactions with test_ratio={test_ratio}...")
    # Shuffle dataframe
    shuffled = df_grouped.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    # Calculate group sizes and cumulative count per student in shuffled dataframe
    shuffled['g_count'] = shuffled.groupby('id_student').cumcount()
    shuffled['g_size'] = shuffled.groupby('id_student')['id_student'].transform('count')
    
    # Determine test mask: students with >= 5 interactions get 20% split into test set
    test_mask = (shuffled['g_size'] >= 5) & (shuffled['g_count'] < (shuffled['g_size'] * test_ratio).astype(int))
    
    train = shuffled[~test_mask].drop(columns=['g_count', 'g_size']).reset_index(drop=True)
    test = shuffled[test_mask].drop(columns=['g_count', 'g_size']).reset_index(drop=True)
    
    print(f"  Train interactions: {len(train)}")
    print(f"  Test interactions: {len(test)}")
    return train, test

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_dir = workspace_dir / "data"
    
    grouped, site_info = load_and_preprocess_data(data_dir)
    train, test = split_interactions(grouped)
    
    print("Sample Train:")
    print(train.head())
