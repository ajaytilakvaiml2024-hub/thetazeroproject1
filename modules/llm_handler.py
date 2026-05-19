import os
import logging
from typing import Optional, List, Dict
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMHandler:
    """Handle LLM interactions for medical report summarization using Groq"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "llama-3.1-8b-instant"):
        """Initialize Groq client"""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model_name
        logger.info(f"Groq LLM Handler initialized with model: {self.model}")
    
    def summarize_medical_report(self, report_text: str) -> str:
        """Summarize a medical report in plain English"""
        prompt = f"""You are a medical report analyzer. Provide a clear, 
plain-English summary that a patient without medical training can understand.

Instructions:
- Explain medical terms simply
- Highlight normal, borderline, and concerning values
- Organize by body system or test type
- Note any critical findings
- Do NOT provide medical advice

Report:
{report_text}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical report summarizer."},
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response.choices[0].message.content
            logger.info(f"Successfully generated summary ({len(summary)} chars)")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return f"Error: Could not generate summary. {str(e)}"
    
    def answer_question(self, report_text: str, question: str, 
                        conversation_history: Optional[List[Dict]] = None) -> str:
        """Answer a specific question about a medical report"""
        history_context = ""
        if conversation_history:
            history_context = "Previous conversation:\n"
            for turn in conversation_history[-5:]:
                history_context += f"Q: {turn.get('question','')}\nA: {turn.get('answer','')}\n\n"
        
        prompt = f"""You are a medical report analyzer helping patients understand their reports.

Report:
{report_text}

{history_context}

Patient's question:
{question}

Answer in simple, non-technical language:
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical Q&A assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message.content
            logger.info(f"Generated answer ({len(answer)} chars)")
            return answer
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return f"I couldn't generate an answer. Error: {str(e)}"
    
    def extract_key_values(self, report_text: str) -> Dict:
        """Extract key lab values and reference ranges"""
        prompt = f"""Extract all numerical values, measurements, and reference ranges from this medical report.
Return as a structured list with:
- Test name
- Patient value
- Reference range / Normal range
- Unit
- Status (Normal/Low/High/Critical)

Report:
{report_text}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical data extractor."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {"values": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Error extracting values: {str(e)}")
            return {"values": f"Error: {str(e)}"}

# Factory function
def create_llm_handler(model_name: str = "llama-3.1-8b-instant") -> Optional[LLMHandler]:
    try:
        return LLMHandler(model_name=model_name)
    except ValueError as e:
        logger.error(f"Failed to initialize Groq LLM: {str(e)}")
        return None
