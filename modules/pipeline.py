import os
import logging
from modules.pdf_parser import PDFParser
from modules.ocr_engine import OCREngine
from modules.llm_handler import create_llm_handler
from modules.chat_memory import ConversationMemory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalReportPipeline:
    """Complete pipeline from document to Q&A"""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.parser = PDFParser()
        self.ocr = OCREngine()
        self.llm = create_llm_handler(model_name=model_name)
        self.memory = ConversationMemory()
        self.current_report_text = ""
        self.current_summary = ""
    
    def process_document(self, file_path: str) -> tuple:
        """Process a medical document (PDF or image) with robust error handling"""
        try:
            # ✅ Validate file exists
            if not os.path.exists(file_path):
                return "", "", "File not found"
            
            # ✅ Validate file size (max 50MB)
            if os.path.getsize(file_path) > 50 * 1024 * 1024:
                return "", "", "File too large (max 50MB)"
            
            extracted_text = ""
            
            # Detect file type
            if file_path.lower().endswith('.pdf'):
                # Check if scanned
                is_scanned = self.parser.detect_scanned_pdf(file_path)
                
                if is_scanned:
                    logger.info("PDF is scanned, using OCR...")
                    images = self.parser.extract_images_from_pdf(file_path)
                    extracted_text = self.ocr.batch_ocr_images(images)
                else:
                    logger.info("PDF is text-native, extracting text...")
                    extracted_text = self.parser.extract_text_pdfplumber(file_path)
            
            else:  # Image file (JPG, PNG)
                logger.info("Processing image with OCR...")
                with open(file_path, "rb") as f:
                    extracted_text = self.ocr.extract_text_from_image(f.read())
            
            if not extracted_text.strip():
                return "", "", "Could not extract text from document"
            
            # Generate summary
            logger.info("Generating summary...")
            summary = self.llm.summarize_medical_report(extracted_text)
            
            # Store in memory
            self.current_report_text = extracted_text
            self.current_summary = summary
            self.memory.load_report(extracted_text, summary)
            
            logger.info("Document processed successfully")
            return extracted_text, summary, None
        
        except ValueError as e:
            return "", "", f"Invalid input: {str(e)}"
        except MemoryError:
            return "", "", "Out of memory - file too large"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return "", "", f"Unexpected error: {str(e)}"
    
    def ask_question(self, question: str) -> str:
        """Ask a question about the loaded report"""
        if not self.current_report_text:
            return "Please load a medical report first."
        
        answer = self.llm.answer_question(
            self.current_report_text,
            question,
            self.memory.get_full_history()
        )
        
        # Store in memory
        self.memory.add_turn(question, answer)
        
        return answer
    
    def get_conversation_history(self):
        """Get current conversation history"""
        return self.memory.get_full_history()
    
    def clear_session(self):
        """Clear loaded report and conversation"""
        self.current_report_text = ""
        self.current_summary = ""
        self.memory.clear_history()
        logger.info("Session cleared")
