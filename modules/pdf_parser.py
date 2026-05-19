import pdfplumber
import fitz
from typing import Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFParser:
    """Extract text from both text-based and scanned PDFs"""
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """
        Extract text from text-native PDFs using pdfplumber
        Returns: Full document text
        """
        try:
            full_text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text += f"\n--- Page {page_num + 1} ---\n{text}"
            
            if not full_text.strip():
                logger.warning(f"No text extracted from {pdf_path} using pdfplumber")
                return ""
            
            logger.info(f"Successfully extracted {len(full_text)} chars from {pdf_path}")
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {str(e)}")
            return ""
    
    def extract_text_pymupdf(self, pdf_path: str) -> str:
        """
        Extract text using PyMuPDF (alternative method)
        Useful for some PDFs that pdfplumber struggles with
        """
        try:
            full_text = ""
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text:
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"
            
            doc.close()
            logger.info(f"PyMuPDF extracted {len(full_text)} chars from {pdf_path}")
            return full_text
            
        except Exception as e:
            logger.error(f"Error with PyMuPDF: {str(e)}")
            return ""
    
    def detect_scanned_pdf(self, pdf_path: str) -> bool:
        """
        Detect if PDF is scanned (image-based) or text-native
        Returns: True if scanned, False if text-native
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:3]:  # Check first 3 pages
                    text = page.extract_text()
                    if text and len(text.strip()) > 50:
                        return False  # Text-native
            return True  # Likely scanned
        except:
            return True
    
    def extract_images_from_pdf(self, pdf_path: str) -> List[bytes]:
        """
        Extract images from PDF for OCR processing
        Useful for mixed documents with text and images
        """
        images = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index in image_list:
                    xref = img_index[0]
                    pix = fitz.Pixmap(doc, xref)
                    img_data = pix.tobytes("png")
                    images.append(img_data)
            
            doc.close()
            logger.info(f"Extracted {len(images)} images from PDF")
            return images
            
        except Exception as e:
            logger.error(f"Error extracting images: {str(e)}")
            return []


# Initialize parser
pdf_parser = PDFParser()