# Personalized Learning Agent

A comprehensive, AI-driven personalized learning platform designed to enhance student outcomes through predictive modeling, personalized recommendations, and dynamic study planning.

## Features

- **Predictive Analytics & Risk Radar**: Identify students at risk and predict performance using historical interaction data.
- **Deep Knowledge Tracing (DKT)**: Track student mastery over time on various topics and concepts.
- **Personalized Recommendations**: Provide tailored content and resource recommendations based on collaborative filtering and knowledge state.
- **Dynamic Study Planner**: Leverage Large Language Models (LLMs) to generate actionable, personalized study plans.
- **Weak Topic Analyzer**: Pinpoint specific areas where a student is struggling to optimize study focus.
- **Premium Dashboard**: A modern React-based frontend providing analytics, progress tracking, and interactive learning tools.

## Architecture & Structure

The repository is divided into several main components:

- **`/backend`**: FastAPI application serving predictions, recommendations, and analytics to the frontend.
- **`/frontend-premium`**: A React + Vite frontend application featuring a premium UI/UX, dashboards, and interactive learning assessments.
- **`/ml`**: Machine learning pipelines for training models (DKT, Performance Prediction, Recommendation, Risk Analysis).
- **`/notebooks`**: Jupyter notebooks for exploratory data analysis (EDA) and initial model prototyping.
- **`/data` & `/models`**: Local storage for raw/processed datasets (e.g., OULA, EdNet) and compiled model artifacts (excluded from version control).

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### Running the Backend
1. Navigate to the `backend` directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the FastAPI server: `uvicorn main:app --reload` (or run `python main.py`)

### Running the Frontend
1. Navigate to the `frontend-premium` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## Data & Models Notice
Due to size constraints, the `data/` and `models/` directories are ignored by Git. To fully run the ML pipelines, please ensure you have the necessary raw datasets (OULA, EdNet) placed in the appropriate `data/raw/` directories and run the data preparation notebooks/scripts to generate the local models.