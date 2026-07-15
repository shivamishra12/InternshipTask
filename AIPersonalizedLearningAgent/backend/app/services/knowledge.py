import pandas as pd
import numpy as np
import torch
from pathlib import Path
from typing import List, Optional
from app.core.exceptions import PredictionError
from app.services.model_loader import ModelLoader
from app.schemas.predict import KnowledgeResponse, HistoryItem
from app.config.logging_config import get_logger

logger = get_logger("knowledge_service")

class KnowledgeTracingService:
    _history_cache = None

    @classmethod
    def _load_history_cache(cls):
        """Loads and parses EdNet preprocessed interactions into memory once."""
        if cls._history_cache is not None:
            return
        
        # Resolve workspace dir (4 levels up from this file)
        workspace_dir = Path(__file__).resolve().parents[3]
        csv_path = workspace_dir / "data" / "processed" / "ednet_preprocessed.csv"
        
        if not csv_path.exists():
            logger.error(f"EdNet interactions CSV not found at: {csv_path}")
            cls._history_cache = {}
            return
            
        logger.info(f"Loading EdNet interaction history from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        # Sort by timestamp to preserve temporal order
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
            
        cache = {}
        for _, row in df.iterrows():
            uid = str(row["user_id"])
            q_id = str(row["question_id"])
            correct = int(row["correct"])
            
            if uid not in cache:
                cache[uid] = []
            cache[uid].append((q_id, correct))
            
        cls._history_cache = cache
        logger.info(f"Loaded interaction history for {len(cache)} students into memory.")

    @classmethod
    def get_student_history_tuples(cls, student_id: int) -> List[tuple]:
        """Convenience method to retrieve student history as raw (question_id, correct) tuples."""
        cls._load_history_cache()
        user_id = f"u{student_id}"
        
        if user_id in cls._history_cache:
            return cls._history_cache[user_id]
        else:
            # Fallback to map student_id to a valid cached user
            fallback_id = f"u{student_id % 100 + 1}"
            return cls._history_cache.get(fallback_id, [])

    @classmethod
    def predict(cls, student_id: int, history: Optional[List[HistoryItem]] = None) -> KnowledgeResponse:
        """Runs Deep Knowledge Tracing to predict question mastery for all questions in the bank."""
        logger.info(f"Running Knowledge Tracing (DKT) for student {student_id}...")
        
        try:
            # 1. Retrieve model resources
            model = ModelLoader.get_dkt_model()
            encoder = ModelLoader.get_dkt_encoder()
            config = ModelLoader.get_dkt_config()
            
            if model is None or encoder is None or config is None:
                raise PredictionError("DKT model components are not loaded in memory.")
                
            num_questions = config.get("num_questions", 500)
            seq_len = config.get("seq_len", 50)
            
            # 2. Get student history
            sim_history = []
            if history is not None:
                sim_history = [(item.question_id, item.correctness) for item in history]
            else:
                sim_history = cls.get_student_history_tuples(student_id)
            
            # 3. Encode student history
            encoded_history_q = []
            history_c = []
            
            for q_str, c in sim_history:
                try:
                    q_enc = encoder.transform([q_str])[0]
                    encoded_history_q.append(q_enc)
                    history_c.append(float(c))
                except ValueError:
                    # Skip unknown questions silently
                    continue
                    
            k = len(encoded_history_q)
            if k == 0:
                logger.warning(f"No history available for student {student_id}. Returning baseline 0.50 mastery.")
                question_mastery = {q_str: 0.50 for q_str in encoder.classes_}
            else:
                # Truncate history if it exceeds seq_len - 1
                if k > seq_len - 1:
                    encoded_history_q = encoded_history_q[-(seq_len - 1):]
                    history_c = history_c[-(seq_len - 1):]
                    k = len(encoded_history_q)
                    
                # Build padded tensors
                questions_tensor = torch.full((num_questions, seq_len), num_questions, dtype=torch.long)
                prev_c_tensor = torch.zeros((num_questions, seq_len), dtype=torch.float)
                
                pad_len = seq_len - k - 1
                
                # Fill history in [pad_len : pad_len+k]
                questions_tensor[:, pad_len:pad_len+k] = torch.tensor(encoded_history_q, dtype=torch.long)
                # Fill final step with candidate question indices (0..num_questions-1)
                questions_tensor[:, seq_len - 1] = torch.arange(num_questions, dtype=torch.long)
                
                # Shift correctness
                prev_c_tensor[:, pad_len+1:pad_len+k+1] = torch.tensor(history_c, dtype=torch.float)
                
                # Model evaluation forward pass
                with torch.no_grad():
                    logits = model(questions_tensor, prev_c_tensor)
                    probs = torch.sigmoid(logits[:, -1])
                    
                # Map probabilities back to question IDs
                question_mastery = {}
                for idx, q_str in enumerate(encoder.classes_):
                    question_mastery[q_str] = float(probs[idx].item())
                    
            logger.info(f"Knowledge Tracing complete for student {student_id} (mastered {len(question_mastery)} questions)")
            
            return KnowledgeResponse(
                student_id=student_id,
                question_mastery=question_mastery
            )
            
        except Exception as e:
            logger.error(f"Error running Knowledge Tracing for student {student_id}: {str(e)}", exc_info=True)
            raise PredictionError(f"Knowledge Tracing failed: {str(e)}")
