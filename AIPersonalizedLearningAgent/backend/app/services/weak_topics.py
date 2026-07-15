import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from app.core.exceptions import PredictionError
from app.schemas.dashboard import WeakTopicResponse
from app.config.logging_config import get_logger

logger = get_logger("weak_topics_service")

class WeakTopicService:
    _topic_mapping = None

    @classmethod
    def _load_topic_mapping(cls):
        """Loads question-to-topic mapping from processed CSV once."""
        if cls._topic_mapping is not None:
            return
            
        # Resolve workspace dir (4 levels up from this file)
        workspace_dir = Path(__file__).resolve().parents[3]
        csv_path = workspace_dir / "data" / "processed" / "question_to_topic.csv"
        
        if not csv_path.exists():
            logger.error(f"question_to_topic.csv not found at: {csv_path}")
            cls._topic_mapping = {}
            return
            
        logger.info(f"Loading question-to-topic mapping from {csv_path}...")
        df = pd.read_csv(csv_path)
        cls._topic_mapping = dict(zip(df["question_id"].astype(str), df["topic"].astype(str)))
        logger.info(f"Loaded {len(cls._topic_mapping)} question-to-topic mappings.")

    @classmethod
    def predict(
        cls, 
        student_id: int, 
        question_mastery: Dict[str, float], 
        student_history: Optional[List[Tuple[str, int]]] = None
    ) -> List[WeakTopicResponse]:
        """Calculates topic mastery and filters out weak areas (mastery < 0.40)."""
        logger.info(f"Detecting weak topics for student {student_id}...")
        
        try:
            cls._load_topic_mapping()
            
            # 1. Group question mastery by topic
            topic_scores = {}
            for q_str, prob in question_mastery.items():
                topic = cls._topic_mapping.get(q_str, "Unknown")
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(prob)
                
            # 2. Compute average mastery per topic
            topic_mastery = {}
            for topic, scores in topic_scores.items():
                topic_mastery[topic] = sum(scores) / len(scores)
                
            # 3. Apply topic-specific adjustments based on student history (correct rate) if provided
            if student_history is not None and len(student_history) > 0:
                topic_history = {}
                for q_str, c in student_history:
                    topic = cls._topic_mapping.get(q_str, "Unknown")
                    if topic not in topic_history:
                        topic_history[topic] = []
                    topic_history[topic].append(float(c))
                    
                for topic in topic_mastery:
                    if topic in topic_history and len(topic_history[topic]) > 0:
                        rate = sum(topic_history[topic]) / len(topic_history[topic])
                        
                        # Apply adjustments identical to training guidelines
                        if rate >= 0.9:
                            adjustment = 0.55
                        elif rate >= 0.5:
                            adjustment = 0.25
                        else:
                            adjustment = -0.30
                            
                        topic_mastery[topic] = max(0.1, min(0.98, topic_mastery[topic] + adjustment))
                        
            # 4. Filter weak topics (mastery < 0.40)
            weak_topics = []
            for topic, score in topic_mastery.items():
                if topic == "Unknown":
                    continue
                if score < 0.40:
                    weak_topics.append(
                        WeakTopicResponse(
                            topic=topic,
                            mastery=round(float(score), 4)
                        )
                    )
                    
            logger.info(f"Weak topic detection complete for student {student_id}. Found {len(weak_topics)} weak topics.")
            return weak_topics
            
        except Exception as e:
            logger.error(f"Error detecting weak topics for student {student_id}: {str(e)}", exc_info=True)
            raise PredictionError(f"Weak topic detection failed: {str(e)}")
