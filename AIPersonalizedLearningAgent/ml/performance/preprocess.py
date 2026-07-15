import os
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

def preprocess_features(raw_dir=None, processed_dir=None):
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    if raw_dir is None:
        raw_dir = workspace_dir / "data"
    if processed_dir is None:
        processed_dir = workspace_dir / "data"
        
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    
    print("Loading datasets for feature engineering...")
    student_info = pd.read_csv(raw_dir / "studentInfo.csv")
    student_registration = pd.read_csv(raw_dir / "studentRegistration.csv")
    student_assessment = pd.read_csv(raw_dir / "studentAssessment.csv")
    assessments = pd.read_csv(raw_dir / "assessments.csv")
    student_vle = pd.read_csv(raw_dir / "studentVle.csv")
    vle = pd.read_csv(raw_dir / "vle.csv")
    
    # ------------------ 1. Target Variables ------------------
    print("Engineering target variables...")
    # success = 1 for Pass/Distinction, 0 for Fail/Withdrawn (Model 1)
    student_info['success'] = student_info['final_result'].isin(['Pass', 'Distinction']).astype(int)
    # risk = 1 for Fail/Withdrawn, 0 for Pass/Distinction (Model 2)
    student_info['risk'] = student_info['final_result'].isin(['Fail', 'Withdrawn']).astype(int)
    
    # ------------------ 2. Registration Features ------------------
    print("Engineering registration features...")
    # date_registration represents the days before course start the student registered (usually negative)
    reg_features = student_registration[['id_student', 'code_module', 'code_presentation', 'date_registration']].copy()
    reg_features['days_registered'] = reg_features['date_registration']  # Will handle missing with Median Imputer
    
    # ------------------ 3. Assessment Features ------------------
    print("Engineering assessment features...")
    # Exclude Exams since we are predicting performance throughout the module based on coursework
    assessments_non_exam = assessments[assessments['assessment_type'] != 'Exam'].copy()
    
    # Total scheduled assessments per module presentation
    scheduled_counts = assessments_non_exam.groupby(['code_module', 'code_presentation']).size().reset_index(name='total_scheduled_assessments')
    
    # Merge student assessment with assessment metadata
    sa_merged = pd.merge(student_assessment, assessments_non_exam, on='id_assessment', how='inner')
    
    # Calculate delay: date_submitted - date
    sa_merged['submission_delay'] = sa_merged['date_submitted'] - sa_merged['date']
    
    # Aggregate assessment metrics per student-module-presentation
    # late_submission_count: number of submissions where delay > 0
    student_assess_agg = sa_merged.groupby(['id_student', 'code_module', 'code_presentation']).agg(
        total_submitted=('score', 'count'),
        mean_score=('score', 'mean'),
        avg_submission_delay=('submission_delay', 'mean'),
        late_submission_count=('submission_delay', lambda x: (x > 0).sum())
    ).reset_index()
    
    # Mean score by assessment type (TMA vs CMA)
    tma_scores = sa_merged[sa_merged['assessment_type'] == 'TMA'].groupby(['id_student', 'code_module', 'code_presentation'])['score'].mean().reset_index(name='mean_tma_score')
    cma_scores = sa_merged[sa_merged['assessment_type'] == 'CMA'].groupby(['id_student', 'code_module', 'code_presentation'])['score'].mean().reset_index(name='mean_cma_score')
    
    # Merge aggregations
    assess_features = pd.merge(student_assess_agg, tma_scores, on=['id_student', 'code_module', 'code_presentation'], how='left')
    assess_features = pd.merge(assess_features, cma_scores, on=['id_student', 'code_module', 'code_presentation'], how='left')
    
    # Merge with scheduled count to calculate missed assessments
    assess_features = pd.merge(assess_features, scheduled_counts, on=['code_module', 'code_presentation'], how='left')
    
    # Fill missing values for students with no submissions in the merged assessment dataframe
    assess_features['total_submitted'] = assess_features['total_submitted'].fillna(0)
    assess_features['missed_assessments'] = assess_features['total_scheduled_assessments'] - assess_features['total_submitted']
    # If a student submitted more than scheduled (can happen due to adjustments), clip missed to 0
    assess_features['missed_assessments'] = assess_features['missed_assessments'].clip(lower=0)
    assess_features['missed_assessment_rate'] = assess_features['missed_assessments'] / assess_features['total_scheduled_assessments']
    
    # Drop total_scheduled_assessments here, but we will reconstruct/keep total_assessments and completed_assessments
    assess_features['total_assessments'] = assess_features['total_scheduled_assessments']
    assess_features['completed_assessments'] = assess_features['total_submitted']
    assess_features['assessment_completion_rate'] = assess_features['completed_assessments'] / assess_features['total_assessments']
    
    assess_features.drop(columns=['total_scheduled_assessments'], inplace=True)
    
    # ------------------ 4. VLE Features ------------------
    print("Engineering VLE interaction features...")
    # Basic clicks aggregation
    vle_agg = student_vle.groupby(['id_student', 'code_module', 'code_presentation']).agg(
        total_clicks=('sum_click', 'sum'),
        active_days=('date', 'nunique')
    ).reset_index()
    
    # Clicks before start (date < 0)
    early_clicks = student_vle[student_vle['date'] < 0].groupby(['id_student', 'code_module', 'code_presentation'])['sum_click'].sum().reset_index(name='early_clicks')
    vle_agg = pd.merge(vle_agg, early_clicks, on=['id_student', 'code_module', 'code_presentation'], how='left')
    vle_agg['early_clicks'] = vle_agg['early_clicks'].fillna(0)
    
    # Clicks by activity type (pivot)
    sv_vle = pd.merge(student_vle, vle, on=['id_site', 'code_module', 'code_presentation'], how='inner')
    activity_clicks = sv_vle.groupby(['id_student', 'code_module', 'code_presentation', 'activity_type'])['sum_click'].sum().reset_index()
    
    # Pivot activity types
    activity_pivot = activity_clicks.pivot(
        index=['id_student', 'code_module', 'code_presentation'],
        columns='activity_type',
        values='sum_click'
    ).reset_index()
    
    # Prefix activity columns
    activity_cols = [col for col in activity_pivot.columns if col not in ['id_student', 'code_module', 'code_presentation']]
    rename_dict = {col: f"vle_{col}" for col in activity_cols}
    activity_pivot.rename(columns=rename_dict, inplace=True)
    activity_pivot.fillna(0, inplace=True)
    
    # Merge basic vle aggregations and pivoted activity clicks
    vle_features = pd.merge(vle_agg, activity_pivot, on=['id_student', 'code_module', 'code_presentation'], how='left')
    
    # ------------------ 5. Clicks Before Exam (Weighted deadlines) ------------------
    print("Engineering Clicks Before Exam...")
    deadlines_dict = assessments_non_exam.groupby(['code_module', 'code_presentation'])['date'].apply(
        lambda x: sorted(x.dropna().tolist())
    ).to_dict()
    
    # Group studentVle by module, presentation, date to compute weight once
    vle_grouped = student_vle.groupby(['code_module', 'code_presentation', 'date'])['sum_click'].sum().reset_index()
    
    def get_weight(row):
        key = (row['code_module'], row['code_presentation'])
        if key not in deadlines_dict:
            return 0
        deadlines = deadlines_dict[key]
        return sum(1 for d in deadlines if d >= row['date'])
        
    vle_grouped['weight'] = vle_grouped.apply(get_weight, axis=1)
    
    # Merge weights back to student_vle
    student_vle_weighted = pd.merge(
        student_vle, 
        vle_grouped[['code_module', 'code_presentation', 'date', 'weight']], 
        on=['code_module', 'code_presentation', 'date'], 
        how='left'
    )
    student_vle_weighted['weight'] = student_vle_weighted['weight'].fillna(0)
    student_vle_weighted['weighted_clicks'] = student_vle_weighted['sum_click'] * student_vle_weighted['weight']
    
    student_clicks_before_exam = student_vle_weighted.groupby(
        ['id_student', 'code_module', 'code_presentation']
    )['weighted_clicks'].sum().reset_index(name='clicks_before_exam')
    
    # ------------------ 6. Merge All Features ------------------
    print("Merging all feature sets together...")
    df = pd.merge(student_info, reg_features, on=['id_student', 'code_module', 'code_presentation'], how='left')
    df = pd.merge(df, assess_features, on=['id_student', 'code_module', 'code_presentation'], how='left')
    df = pd.merge(df, vle_features, on=['id_student', 'code_module', 'code_presentation'], how='left')
    df = pd.merge(df, student_clicks_before_exam, on=['id_student', 'code_module', 'code_presentation'], how='left')
    
    # Handle students who had no VLE interactions at all
    vle_cols = [col for col in df.columns if col.startswith('vle_') or col in ['total_clicks', 'active_days', 'early_clicks', 'clicks_before_exam']]
    df[vle_cols] = df[vle_cols].fillna(0)
    
    # Handle students who had no assessments at all
    df['total_submitted'] = df['total_submitted'].fillna(0)
    df['completed_assessments'] = df['completed_assessments'].fillna(0)
    df['late_submission_count'] = df['late_submission_count'].fillna(0)
    
    # Calculate schedule maps to fill missing missed assessments and total assessments
    schedule_map = scheduled_counts.set_index(['code_module', 'code_presentation'])['total_scheduled_assessments'].to_dict()
    
    def fill_missed(row):
        if pd.isna(row['missed_assessments']):
            mod_pres = (row['code_module'], row['code_presentation'])
            total_sch = schedule_map.get(mod_pres, 0)
            return total_sch
        return row['missed_assessments']
    
    df['missed_assessments'] = df.apply(fill_missed, axis=1)
    
    def fill_missed_rate(row):
        if pd.isna(row['missed_assessment_rate']):
            mod_pres = (row['code_module'], row['code_presentation'])
            total_sch = schedule_map.get(mod_pres, 0)
            return 1.0 if total_sch > 0 else 0.0
        return row['missed_assessment_rate']
        
    df['missed_assessment_rate'] = df.apply(fill_missed_rate, axis=1)
    
    # Re-fill/compute total_assessments and assessment_completion_rate
    def fill_total_assessments(row):
        if pd.isna(row['total_assessments']):
            mod_pres = (row['code_module'], row['code_presentation'])
            return schedule_map.get(mod_pres, 0)
        return row['total_assessments']
        
    df['total_assessments'] = df.apply(fill_total_assessments, axis=1)
    df['assessment_completion_rate'] = df['completed_assessments'] / df['total_assessments'].replace(0, np.nan)
    df['assessment_completion_rate'] = df['assessment_completion_rate'].fillna(0.0)
    
    # ------------------ 7. Add Multi-model Alias & Engagement Score ------------------
    print("Engineering model-specific features (Engagement Score, etc.)...")
    # Engagement Score = 0.6 * normalized_clicks + 0.4 * normalized_active_days
    min_clicks = df['total_clicks'].min()
    max_clicks = df['total_clicks'].max()
    norm_clicks = (df['total_clicks'] - min_clicks) / (max_clicks - min_clicks + 1e-8)
    
    min_days = df['active_days'].min()
    max_days = df['active_days'].max()
    norm_days = (df['active_days'] - min_days) / (max_days - min_days + 1e-8)
    
    df['engagement_score'] = 0.6 * norm_clicks + 0.4 * norm_days
    
    # Explicit aliases for readability & requirements
    df['avg_score'] = df['mean_score']                     # Imputation handled by pipeline imputer
    df['submission_delay'] = df['avg_submission_delay']     # Imputation handled by pipeline imputer
    df['previous_performance_indicator'] = df['num_of_prev_attempts']
    
    # Save the final engineered dataset
    output_path = processed_dir / "engineered_features.csv"
    df.to_csv(output_path, index=False)
    print(f"Feature engineering completed successfully. Shape: {df.shape}")
    print(f"Engineered dataset saved to {output_path}")
    
    try:
        from PersonalizedLearningAgent.ml.recommendation.preprocess import load_and_preprocess_data
        vle_agg, _ = load_and_preprocess_data(raw_dir)
        vle_agg.to_csv(processed_dir / "vle_interactions_aggregated.csv", index=False)
    except Exception as e:
        print(f"Could not aggregate VLE data: {e}")
        vle_agg = pd.DataFrame()
        
    return df, vle_agg

if __name__ == "__main__":
    preprocess_features()
