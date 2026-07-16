import os
import json
import easyocr
import whisper
from google import genai
from PIL import Image

class EvidenceFusionEngine:
    def __init__(self, gemini_api_key=None):
        # Initialize Gemini using the modern SDK client pattern
        if gemini_api_key:
            self.client = genai.Client(api_key=gemini_api_key)
        else:
            self.client = genai.Client()
        
        # Initialize specialized models lazily to save memory during startup
        self.ocr_reader = None
        self.audio_model = None

    def _get_ocr(self):
        if not self.ocr_reader:
            self.ocr_reader = easyocr.Reader(['en', 'hi']) # English and Hindi
        return self.ocr_reader

    def _get_whisper(self):
        if not self.audio_model:
            self.audio_model = whisper.load_model("base")
        return self.audio_model

    def process_image(self, image_path):
        """Extract text from screenshots using OCR."""
        reader = self._get_ocr()
        result = reader.readtext(image_path, detail=0)
        return " ".join(result)

    def process_audio(self, audio_path):
        """Transcribe scammer audio using Whisper."""
        model = self._get_whisper()
        result = model.transcribe(audio_path)
        return result["text"]

    def generate_unified_report(self, evidence_list):
        """
        Takes a list of dictionaries: [{'type': 'image', 'path': '...'}, {'type': 'text', 'content': '...'}]
        Combines extractions and runs a master prompt to get JSON threat intel.
        """
        fused_context = ""
        
        for idx, evidence in enumerate(evidence_list):
            if evidence['type'] == 'image':
                text = self.process_image(evidence['path'])
                fused_context += f"\n[Evidence {idx+1} - OCR from Image]: {text}"
            elif evidence['type'] == 'audio':
                text = self.process_audio(evidence['path'])
                fused_context += f"\n[Evidence {idx+1} - Audio Transcript]: {text}"
            elif evidence['type'] == 'text':
                fused_context += f"\n[Evidence {idx+1} - User Text]: {evidence['content']}"

        prompt = f"""
        Act as an elite Cybersecurity and Fraud Investigation AI for the Indian Government.
        Analyze the following fused evidence from a citizen.
        
        EVIDENCE:
        {fused_context}
        
        Determine the nature of the threat. Output your response STRICTLY as a JSON object with the following keys:
        - "scam_type" (e.g., "Digital Arrest", "UPI Fraud", "Safe")
        - "threat_score" (integer 0-100)
        - "confidence" (integer 0-100)
        - "analysis" (A 3-sentence professional summary of the threat vectors)
        - "recommended_action" (Immediate steps for the victim/police)
        - "extracted_entities" (List of phone numbers, UPI IDs, or links found)
        
        Return ONLY valid JSON.
        """
        
        try:
            # Execute text-generation targeting Gemini 3.5 Flash and enforcing JSON output mode
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # Strip potential markdown backticks from LLM response (kept as a safety fallback)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
            
        except Exception as e:
            print(f"Error generating unified report or parsing JSON: {e}")
            return {
                "scam_type": "Unknown",
                "threat_score": 0,
                "confidence": 0,
                "analysis": "AI failed to parse evidence into structured format.",
                "recommended_action": "Manual review required.",
                "extracted_entities": []
            }