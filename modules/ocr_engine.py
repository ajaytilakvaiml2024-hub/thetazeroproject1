import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
import logging
from io import BytesIO
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Ajay Tilak V\Downloads\tesseract.exe"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCREngine:
    """Handle OCR for scanned medical documents"""
    
    def __init__(self):
        """Initialize both Tesseract and EasyOCR readers"""
        try:
            self.reader = easyocr.Reader(['en'], gpu=False)
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"EasyOCR initialization failed: {str(e)}")
            self.reader = None
    
    def preprocess_image(self, image_input) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy
        - Convert to grayscale
        - Denoise
        - Enhance contrast
        - Deskew if needed
        """
        # Handle different input types
        if isinstance(image_input, str):
            # File path
            image = cv2.imread(image_input)
        elif isinstance(image_input, bytes):
            # Bytes from PDF
            nparr = np.frombuffer(image_input, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            # Assume it's already an array
            image = image_input
        
        if image is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Optional: Threshold for very poor quality images
        _, binary = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY)
        
        return binary
    
    def ocr_with_easyocr(self, image_input) -> str:
        """
        Perform OCR using EasyOCR
        More accurate for medical documents
        """
        if self.reader is None:
            logger.warning("EasyOCR reader not available")
            return ""
        
        try:
            preprocessed = self.preprocess_image(image_input)
            
            # EasyOCR
            results = self.reader.readtext(preprocessed)
            
            # Extract text with structure preservation
            text = ""
            current_y = 0
            for (bbox, extracted_text, confidence) in results:
                # Simple line detection based on Y coordinate
                y_coord = bbox[0][1]  # Top-left Y
                if y_coord - current_y > 10:  # New line
                    text += "\n"
                text += extracted_text + " "
                current_y = y_coord
            
            logger.info(f"EasyOCR extracted {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            logger.error(f"EasyOCR failed: {str(e)}")
            return ""
    
    def ocr_with_tesseract(self, image_input) -> str:
        """
        Perform OCR using Tesseract (fallback)
        """
        try:
            preprocessed = self.preprocess_image(image_input)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(preprocessed)
            
            # Tesseract OCR
            text = pytesseract.image_to_string(pil_image)
            
            logger.info(f"Tesseract extracted {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Tesseract failed: {str(e)}")
            logger.info("Make sure Tesseract is installed: brew install tesseract (macOS)")
            return ""
    
    def extract_text_from_image(self, image_input, method='easyocr') -> str:
        """
        Main OCR method with fallback
        """
        if method == 'easyocr':
            text = self.ocr_with_easyocr(image_input)
            if text:
                return text
            logger.info("Falling back to Tesseract...")
            return self.ocr_with_tesseract(image_input)
        else:
            text = self.ocr_with_tesseract(image_input)
            if text:
                return text
            logger.info("Falling back to EasyOCR...")
            return self.ocr_with_easyocr(image_input)
    
    def batch_ocr_images(self, image_list: list) -> str:
        """
        Process multiple images and combine text
        """
        combined_text = ""
        for idx, image in enumerate(image_list):
            text = self.extract_text_from_image(image)
            if text:
                combined_text += f"\n--- Image {idx + 1} ---\n{text}"
        
        return combined_text


# Initialize OCR engine
ocr_engine = OCREngine()