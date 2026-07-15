import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def run_eda():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_dir = workspace_dir / "data"
    artifacts_dir = workspace_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    print("Loading datasets...")
    student_info = pd.read_csv(data_dir / "studentInfo.csv")
    student_registration = pd.read_csv(data_dir / "studentRegistration.csv")
    student_assessment = pd.read_csv(data_dir / "studentAssessment.csv")
    assessments = pd.read_csv(data_dir / "assessments.csv")
    student_vle = pd.read_csv(data_dir / "studentVle.csv")
    vle = pd.read_csv(data_dir / "vle.csv")
    courses = pd.read_csv(data_dir / "courses.csv")

    print("\n--- Dataset Summary Statistics ---")
    print(f"studentInfo.csv: {student_info.shape}")
    print(f"studentRegistration.csv: {student_registration.shape}")
    print(f"studentAssessment.csv: {student_assessment.shape}")
    print(f"assessments.csv: {assessments.shape}")
    print(f"studentVle.csv: {student_vle.shape}")
    print(f"vle.csv: {vle.shape}")
    print(f"courses.csv: {courses.shape}")

    # Set styling
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (10, 6)

    # 1. Target Class Distribution (Multi-class final_result)
    plt.figure()
    order = ['Distinction', 'Pass', 'Fail', 'Withdrawn']
    sns.countplot(data=student_info, x='final_result', order=order, palette='viridis')
    plt.title('Distribution of Final Results (Multi-class)')
    plt.xlabel('Final Result')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(artifacts_dir / 'eda_final_result_dist.png', dpi=300)
    plt.close()

    # 2. Binary Target Class Distribution
    student_info['success'] = student_info['final_result'].isin(['Pass', 'Distinction']).astype(int)
    plt.figure()
    sns.countplot(data=student_info, x='success', palette='Set2')
    plt.title('Distribution of Student Success (Binary)')
    plt.xticks([0, 1], ['Unsuccessful (Fail/Withdrawn)', 'Successful (Pass/Distinction)'])
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(artifacts_dir / 'eda_binary_target_dist.png', dpi=300)
    plt.close()
    
    success_rate = student_info['success'].mean() * 100
    print(f"\nTarget Variable Success Rate: {success_rate:.2f}% (Pass/Distinction)")
    print(f"Class Breakdown:\n{student_info['final_result'].value_counts()}")

    # 3. Demographics vs Success
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.countplot(data=student_info, x='gender', hue='success', palette='Set2')
    plt.title('Success by Gender')
    plt.xlabel('Gender')
    plt.legend(['Unsuccessful', 'Successful'])

    plt.subplot(1, 2, 2)
    sns.countplot(data=student_info, x='age_band', hue='success', palette='Set2')
    plt.title('Success by Age Band')
    plt.xlabel('Age Band')
    plt.legend(['Unsuccessful', 'Successful'])
    plt.tight_layout()
    plt.savefig(artifacts_dir / 'eda_demographics.png', dpi=300)
    plt.close()

    # 4. VLE Clicks distribution by student
    # Let's aggregate clicks by student-presentation
    print("\nAggregating student clicks on VLE...")
    student_clicks = student_vle.groupby(['id_student', 'code_module', 'code_presentation'])['sum_click'].sum().reset_index()
    student_merged_clicks = pd.merge(student_info, student_clicks, on=['id_student', 'code_module', 'code_presentation'], how='left')
    student_merged_clicks['sum_click'] = student_merged_clicks['sum_click'].fillna(0)

    plt.figure()
    # Log-scale boxplot of clicks vs success
    student_merged_clicks['log_clicks'] = np.log1p(student_merged_clicks['sum_click'])
    sns.boxplot(data=student_merged_clicks, x='success', y='log_clicks', palette='Set2')
    plt.title('Log of VLE Clicks vs Student Success')
    plt.xticks([0, 1], ['Unsuccessful', 'Successful'])
    plt.ylabel('Log(Clicks + 1)')
    plt.xlabel('Outcome')
    plt.tight_layout()
    plt.savefig(artifacts_dir / 'eda_clicks_vs_success.png', dpi=300)
    plt.close()
    
    print("VLE Click Statistics (Successful vs Unsuccessful):")
    print(student_merged_clicks.groupby('success')['sum_click'].describe())

    # 5. Assessment scores vs success
    print("\nAnalyzing student assessment results...")
    # Calculate average assessment score for each student
    # Note: excluding exams from calculations as exams are often not in studentAssessment
    assessments_non_exam = assessments[assessments['assessment_type'] != 'Exam']
    sa_merged = pd.merge(student_assessment, assessments_non_exam, on='id_assessment', how='inner')
    student_avg_score = sa_merged.groupby(['id_student'])['score'].mean().reset_index()
    student_avg_score.rename(columns={'score': 'avg_assessment_score'}, inplace=True)
    
    student_merged_score = pd.merge(student_info, student_avg_score, on='id_student', how='left')
    
    plt.figure()
    sns.histplot(data=student_merged_score, x='avg_assessment_score', hue='success', kde=True, bins=30, multiple='stack', palette='Set2')
    plt.title('Average Assessment Score Distribution by Success Status')
    plt.xlabel('Average Assessment Score')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(artifacts_dir / 'eda_assessment_score_dist.png', dpi=300)
    plt.close()

    print("\nEDA completed. Plots saved to artifacts directory.")

if __name__ == "__main__":
    run_eda()
