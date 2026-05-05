"""
app.py — Flask Application (Full Feature Build)
=================================================
Integrates:
  - Dual API (Gemini embed + Groq generate)
  - Hybrid Search (FAISS + BM25 + Re-rank)
  - Smart Memory (entity + summarized)
  - Symptom Triage
  - 7-Layer Firewall + Confidence Scoring
  - Multi-turn Injection Detection
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os, uuid
from dotenv import load_dotenv

from rag.pipeline      import RAGPipeline
from firewall.firewall import PromptFirewall

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "hospital-chatbot-secret-2024")
CORS(app)

print("=" * 55)
print("  MedAssist — City General Hospital AI Chatbot")
print("=" * 55)

print("\n🔄 Initializing RAG Pipeline...")
rag = RAGPipeline()

print("\n🛡️  Initializing Prompt Firewall...")
firewall = PromptFirewall()

status = rag.provider_status()
print(f"\n📡 Providers:")
print(f"   Embed     : Gemini ({status['embedding']})")
print(f"   Generate  : {status['generation']['primary']} "
      f"→ {status['generation']['fallback']} (fallback)")
print(f"\n⚙️  Features:")
for k, v in status.get("features", {}).items():
    icon = "✅" if v else "⚠️ "
    print(f"   {icon} {k.replace('_',' ').title()}")
print()


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message"}), 400

    user_message = data["message"].strip()
    session_id   = session.get("session_id", "default")

    # Get recent turns for multi-turn injection analysis
    recent_turns = rag.memory.get_recent_turns(session_id, last_n=5)

    # ── Firewall ───────────────────────────────────────────────
    fw = firewall.check(
        user_message,
        session_id   = session_id,
        recent_turns = recent_turns,
    )

    if not fw.allowed:
        return jsonify({
            "response"   : fw.message,
            "sources"    : [],
            "blocked"    : True,
            "block_layer": fw.layer,
            "action"     : fw.action,
            "risk_score" : round(fw.risk_score, 3),
            "provider"   : "firewall",
        })

    # ── RAG + Triage ───────────────────────────────────────────
    try:
        result = rag.query(user_message, session_id=session_id)

        response_text = result["answer"]

        # Append caution note if confidence scorer flagged borderline risk
        if fw.action == "caution" and fw.note:
            response_text += f"\n\n_{fw.note}_"

        resp = {
            "response"  : response_text,
            "sources"   : result.get("sources", []),
            "blocked"   : False,
            "provider"  : result.get("provider", "unknown"),
            "confidence": result.get("confidence", "high"),
            "risk_score": round(fw.risk_score, 3),
        }

        if fw.warning:
            resp["warning"] = fw.warning

        # Pass triage data if present
        if "triage" in result:
            resp["triage"] = result["triage"]

        return jsonify(resp)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback; traceback.print_exc()
        return jsonify({
            "response": (
                "I'm having trouble right now. "
                "Please call City General Hospital at +1-800-HOSPITAL."
            ),
            "sources" : [],
            "blocked" : False,
            "provider": "error",
        }), 500


@app.route("/api/health")
def health():
    return jsonify({
        "status"   : "ok",
        "rag_ready": rag.is_ready(),
        "providers": rag.provider_status(),
        "firewall" : "active",
    })


@app.route("/api/firewall/stats")
def fw_stats():
    sid = session.get("session_id", "default")
    return jsonify({
        "rate_limits": firewall.stats(sid),
        "risk_score" : firewall.conv.get_risk_score(sid),
    })


@app.route("/api/clear", methods=["POST"])
def clear():
    sid = session.get("session_id", "default")
    rag.clear_history(sid)
    firewall.reset_conversation(sid)
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5007)