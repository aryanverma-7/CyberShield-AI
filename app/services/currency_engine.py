import os
import cv2
import json
from PIL import Image
from google import genai

class CurrencyVerificationEngine:
    def __init__(self, gemini_api_key=None):
        # Initialize Gemini using the modern SDK client pattern
        if gemini_api_key:
            self.client = genai.Client(api_key=gemini_api_key)
        else:
            self.client = genai.Client()

    def preprocess_and_audit_geometry(self, image_path, output_filename):
        """
        Uses OpenCV to perform edge detection and structural analysis.
        Generates a diagnostic image highlighting lines and alignment markers.
        """
        # Load image in grayscale
        img = cv2.imread(image_path)
        if img is None:
            return False
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur and Canny Edge Detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find structural alignment contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw a premium engineering analysis overlay on the original image
        diagnostic_img = img.copy()
        cv2.drawContours(diagnostic_img, contours, -1, (0, 255, 0), 1) # Green contours
        
        # Overlay a scanning target reticle matrix
        h, w, _ = diagnostic_img.shape
        cv2.line(diagnostic_img, (0, int(h/2)), (w, int(h/2)), (255, 0, 0), 1) # Blue horizontal line
        cv2.line(diagnostic_img, (int(w/2), 0), (int(w/2), h), (255, 0, 0), 1) # Blue vertical line
        
        # Save structural output frame
        dir_name = os.path.dirname(image_path)
        diagnostic_path = os.path.join(dir_name, output_filename)
        cv2.imwrite(diagnostic_path, diagnostic_img)
        
        return diagnostic_path

    def analyze_banknote(self, front_path, back_path):
        """
        Performs structural CV preprocessing and pipes assets to Gemini for deep forensic audit.
        """
        # 1. Run OpenCV Diagnostic Pass
        diag_front = self.preprocess_and_audit_geometry(front_path, "diag_front.png")
        diag_back = self.preprocess_and_audit_geometry(back_path, "diag_back.png")
        
        # 2. Package for Multimodal LLM Verification
        pil_front = Image.open(front_path)
        pil_back = Image.open(back_path)
        
        prompt = """
        Act as a Senior Forensic Currency Expert for the Reserve Bank of India (RBI).
        Analyze the uploaded Front and Back images of this banknote.
        
        Perform a rigorous verification checklist checking for the following:
        1. Security Thread: Check continuity, color-shifting properties, and text alignment.
        2. Watermark: Examine the visibility and clarity of the Mahatma Gandhi portrait profile.
        3. Alignment: Verify the see-through registration mark accuracy.
        4. Microprint & Lettering: Inspect sharp font definitions along the borders.
        5. Serial Number: Confirm proper font scaling and spacing regularities.
        
        Respond STRICTLY with a JSON object structured exactly as follows:
        {
            "authenticity_score": 85,
            "security_thread": "Verified continuous color-shift windowing matching standard specification",
            "watermark": "Clear profile contrast matching structural baseline",
            "alignment": "Geometric registration lines align correctly across both planes",
            "serial_number": "Legitimate ascending spacing configuration discovered",
            "suspicious_features": [
                "Minor microprint bleeding noticed along top margin text",
                "Slight ink density variance near reserve seal"
            ],
            "recommendation": "Pass structural validation. Note slight cosmetic variations. Safe for circulation."
        }
        
        Return ONLY valid JSON. Ensure numerical score represents safe (75+), suspicious (40-74), or highly counterfeit (0-39).
        """
        
        try:
            # Execute text-generation targeting Gemini 3.5 Flash, handling multi-modal image buffers, and enforcing JSON responses
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[prompt, pil_front, pil_back],
                config={"response_mime_type": "application/json"}
            )
            
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json)
            
            # Append paths of generated diagnostic overlays so front-end can show them
            result['diag_front_url'] = "/static/uploads/diag_front.png"
            result['diag_back_url'] = "/static/uploads/diag_back.png"
            return result
            
        except Exception as e:
            return {
                "authenticity_score": 0,
                "security_thread": "Error during vision processing",
                "watermark": "Failed parsing",
                "alignment": "Failed parsing",
                "serial_number": "Failed parsing",
                "suspicious_features": [f"Processing error: {str(e)}"],
                "recommendation": "Manual technical review required."
            }