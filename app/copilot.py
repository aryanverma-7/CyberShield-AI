import os
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
import logging
from google import genai

logger = logging.getLogger(__name__)
copilot_bp = Blueprint('copilot', __name__)

# Keep your clean, verified key here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the client
client = genai.Client(api_key=GEMINI_API_KEY)

@copilot_bp.route('/copilot/')
def chat_interface():
    return render_template('copilot.html')

@copilot_bp.route('/copilot/api/chat', methods=['POST'])
def handle_chat_message():
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"status": "error", "error": "Message content is empty."}), 400

    logger.info(f"Forwarding live query to Gemini Engine: {message[:30]}...")

    try:
        # Clean background guardrails context
        system_prompt = """
        You are the CyberShield Legal Defense Assistant, an expert AI agent deployed in a cybercrime safety dashboard.
        Your job is to answer the user's question regarding cyber fraud, digital safety, phishing, legal rights, or online scams.
        
        Keep your answer protective, clear, and action-oriented. Do not include markdown headers like '#' or '##'.
        
        CRUCIAL FORMATTING RULE: You must split your response into two sections using a triple pipe '|||' delimiter.
        Section 1: The dynamic safety answer.
        Section 2: A comma-separated list of 1 to 3 real legal bodies, acts, or portals relevant to the query (e.g., CERT-In, RBI Guidelines, NPCI Portal, Section 66D IT Act).
        
        Example format:
        No legitimate authority will place you under arrest via video call...
        |||
        MHA Cyberdost Advisory, Indian Penal Code Section 419
        """
        
        # 🚀 Supercharged Low-Latency Configuration (Direct Dict Matching)
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=message,
            config={
                'system_instruction': system_prompt,
                # 🧠 CRUCIAL: Force thinking down to minimal to eliminate the 24s token delay
                'thinking_config': {
                    'thinking_level': 'minimal'
                },
                # 🚫 Disable automatic tool pre-scans
                'automatic_function_calling': {
                    'disable': True
                }
            }
        )
        response_text = response.text.strip()
        
        # Map out text chunks cleanly for your JavaScript app architecture
        if "|||" in response_text:
            ai_reply, citations_raw = response_text.split("|||", 1)
            ai_reply = ai_reply.strip()
            citations = [c.strip() for c in citations_raw.split(",") if c.strip()]
        else:
            ai_reply = response_text
            citations = ["CyberShield Core Heuristics Engine"]

        return jsonify({
            "status": "success",
            "answer": ai_reply,
            "citations": citations,
            "timestamp": datetime.now().strftime('%H:%M')
        }), 200

    except Exception as e:
        logger.error(f"Gemini Engine Execution Fault: {str(e)}")
        return jsonify({
            "status": "error",
            "answer": f"⚠️ **Engine Error:** {str(e)}",
            "citations": ["System Configuration Logs"],
            "timestamp": datetime.now().strftime('%H:%M')
        }), 500