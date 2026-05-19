import json
import logging
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationMemory:
    """Manage chat history and conversation context"""
    
    def __init__(self, max_turns: int = 20):
        """
        Initialize conversation memory
        
        Args:
            max_turns: Maximum number of Q&A pairs to keep in memory
        """
        self.history: List[Dict] = []
        self.max_turns = max_turns
        self.report_text = ""
        self.report_summary = ""
    
    def load_report(self, text: str, summary: str = ""):
        """Load medical report context"""
        self.report_text = text
        self.report_summary = summary
        logger.info("Report loaded into memory")
    
    def add_turn(self, question: str, answer: str):
        """
        Add a Q&A turn to history
        
        Args:
            question: User's question
            answer: AI's answer
        """
        turn = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer
        }
        self.history.append(turn)
        
        # Keep only recent turns
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]
        
        logger.info(f"Added turn #{len(self.history)}")
    
    def get_recent_context(self, num_turns: int = 5) -> str:
        """
        Get recent conversation for context
        """
        context = ""
        for turn in self.history[-num_turns:]:
            context += f"Q: {turn['question']}\nA: {turn['answer'][:200]}...\n\n"
        return context
    
    def get_full_history(self) -> List[Dict]:
        """Return full conversation history"""
        return self.history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        logger.info("Conversation history cleared")
    
    def export_conversation(self, filepath: str):
        """
        Export conversation to JSON file
        """
        try:
            data = {
                "report_summary": self.report_summary,
                "conversation": self.history
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Conversation exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export: {str(e)}")
    
    def get_stats(self) -> Dict:
        """Get conversation statistics"""
        return {
            "total_turns": len(self.history),
            "first_question": self.history[0]['question'] if self.history else None,
            "conversation_started": self.history[0]['timestamp'] if self.history else None,
        }