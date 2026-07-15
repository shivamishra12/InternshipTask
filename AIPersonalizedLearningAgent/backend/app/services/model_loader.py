import os
import pickle
import json
from pathlib import Path
import pandas as pd
import numpy as np
import torch
from scipy.sparse import csr_matrix
from app.core.exceptions import ModelLoadError
from app.config.logging_config import get_logger
from app.services.dkt_model import DKTModel

logger = get_logger("model_loader")

class ModelLoader:
    _instance = None

    # Cached models
    _performance_model = None
    _performance_preprocessor = None
    _risk_model = None
    _risk_preprocessor = None
    _dkt_model = None
    _dkt_encoder = None
    _dkt_config = None
    _recommendation_package = None
    _recommendation_matrix_R = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_all_models(cls, workspace_dir: Path = None):
        """Loads all machine learning models into memory once at startup."""
        if cls._performance_model is not None:
            logger.info("Models already loaded in memory. Skipping reload.")
            return

        if workspace_dir is None:
            # Resolve workspace directory: file is in backend/app/services/model_loader.py
            # backend/app/services is 3 parents up
            workspace_dir = Path(__file__).resolve().parents[3]
        
        models_dir = workspace_dir / "models"
        data_processed_dir = workspace_dir / "data" / "processed"
        
        logger.info(f"Loading ML models from: {models_dir}")
        logger.info(f"Loading interaction data from: {data_processed_dir}")

        try:
            # 1. Load Performance Model & Preprocessor
            perf_model_path = models_dir / "performance_model.pkl"
            perf_prep_path = models_dir / "performance_preprocessor.pkl"
            
            if not perf_model_path.exists():
                raise FileNotFoundError(f"Performance model not found at {perf_model_path}")
            
            with open(perf_model_path, "rb") as f:
                cls._performance_model = pickle.load(f)
            
            if perf_prep_path.exists():
                with open(perf_prep_path, "rb") as f:
                    cls._performance_preprocessor = pickle.load(f)
            elif hasattr(cls._performance_model, "named_steps") and "preprocessor" in cls._performance_model.named_steps:
                cls._performance_preprocessor = cls._performance_model.named_steps["preprocessor"]
            
            logger.info("Performance model and preprocessor loaded successfully.")

            # 2. Load Risk Model & Preprocessor
            risk_model_path = models_dir / "risk_model.pkl"
            risk_prep_path = models_dir / "risk_preprocessor.pkl"
            
            if not risk_model_path.exists():
                raise FileNotFoundError(f"Risk model not found at {risk_model_path}")
            
            with open(risk_model_path, "rb") as f:
                cls._risk_model = pickle.load(f)
                
            if risk_prep_path.exists():
                with open(risk_prep_path, "rb") as f:
                    cls._risk_preprocessor = pickle.load(f)
            elif hasattr(cls._risk_model, "named_steps") and "preprocessor" in cls._risk_model.named_steps:
                cls._risk_preprocessor = cls._risk_model.named_steps["preprocessor"]
                
            logger.info("Risk model and preprocessor loaded successfully.")

            # 3. Load DKT Model, Encoder, and Config
            dkt_model_path = models_dir / "dkt_model.pt"
            dkt_config_path = models_dir / "dkt_config.json"
            if not dkt_config_path.exists():
                dkt_config_path = models_dir / "config.json"
                
            dkt_encoder_path = models_dir / "dkt_question_encoder.pkl"
            if not dkt_encoder_path.exists():
                dkt_encoder_path = models_dir / "question_encoder.pkl"

            if not dkt_model_path.exists():
                raise FileNotFoundError(f"DKT model weight file not found at {dkt_model_path}")
            if not dkt_config_path.exists():
                raise FileNotFoundError(f"DKT configuration not found at {dkt_config_path}")
            if not dkt_encoder_path.exists():
                raise FileNotFoundError(f"DKT question encoder not found at {dkt_encoder_path}")

            with open(dkt_config_path, "r") as f:
                cls._dkt_config = json.load(f)

            with open(dkt_encoder_path, "rb") as f:
                cls._dkt_encoder = pickle.load(f)

            num_questions = cls._dkt_config.get("num_questions", 500)
            embedding_dim = cls._dkt_config.get("embedding_dim", 128)
            hidden_dim = cls._dkt_config.get("hidden_dim", 128)
            num_layers = cls._dkt_config.get("num_layers", 2)
            dropout = cls._dkt_config.get("dropout", 0.3)

            cls._dkt_model = DKTModel(
                num_questions=num_questions,
                embedding_dim=embedding_dim,
                hidden_dim=hidden_dim,
                num_layers=num_layers,
                dropout=dropout
            )
            
            state_dict = torch.load(dkt_model_path, map_location=torch.device('cpu'))
            cls._dkt_model.load_state_dict(state_dict)
            cls._dkt_model.eval()
            logger.info("DKT model, config, and question encoder loaded successfully.")

            # 4. Load Recommendation model package
            rec_model_path = models_dir / "recommendation_model.pkl"
            if not rec_model_path.exists():
                raise FileNotFoundError(f"Recommendation model not found at {rec_model_path}")
            
            with open(rec_model_path, "rb") as f:
                cls._recommendation_package = pickle.load(f)

            train_interactions_path = data_processed_dir / "train_interactions.csv"
            if not train_interactions_path.exists():
                logger.warning(f"train_interactions.csv not found at {train_interactions_path}. Recommender fallback will be popularity-only.")
            else:
                train_df = pd.read_csv(train_interactions_path)
                cls._recommendation_matrix_R = cls._build_interaction_matrix(
                    train_df,
                    cls._recommendation_package["idx_to_student"],
                    cls._recommendation_package["idx_to_site"]
                )
            logger.info("Recommendation similarity package and interaction matrix loaded successfully.")
            
        except Exception as e:
            logger.critical(f"Failed to load machine learning models: {str(e)}", exc_info=True)
            raise ModelLoadError(f"Model initialization failed: {str(e)}")

    @classmethod
    def _build_interaction_matrix(cls, df: pd.DataFrame, student_list: np.ndarray, site_list: np.ndarray) -> csr_matrix:
        """Helper to reconstruct interaction matrix R from interactions dataset."""
        student_to_idx = {sid: idx for idx, sid in enumerate(student_list)}
        site_to_idx = {sid: idx for idx, sid in enumerate(site_list)}
        
        num_students = len(student_list)
        num_sites = len(site_list)
        
        valid_rows = df[df['id_student'].isin(student_to_idx) & df['id_site'].isin(site_to_idx)]
        
        rows = valid_rows['id_student'].map(student_to_idx).values
        cols = valid_rows['id_site'].map(site_to_idx).values
        clicks = np.log1p(valid_rows['sum_click'].values)
        
        return csr_matrix((clicks, (rows, cols)), shape=(num_students, num_sites), dtype=np.float32)

    # --- Getter methods ---
    @classmethod
    def get_performance_model(cls):
        return cls._performance_model

    @classmethod
    def get_performance_preprocessor(cls):
        return cls._performance_preprocessor

    @classmethod
    def get_risk_model(cls):
        return cls._risk_model

    @classmethod
    def get_risk_preprocessor(cls):
        return cls._risk_preprocessor

    @classmethod
    def get_dkt_model(cls):
        return cls._dkt_model

    @classmethod
    def get_dkt_encoder(cls):
        return cls._dkt_encoder

    @classmethod
    def get_dkt_config(cls):
        return cls._dkt_config

    @classmethod
    def get_recommendation_model(cls):
        # Alias for get_recommendation_package for the standard naming
        return cls._recommendation_package

    @classmethod
    def get_recommendation_package(cls):
        return cls._recommendation_package

    @classmethod
    def get_recommendation_matrix_R(cls):
        return cls._recommendation_matrix_R
