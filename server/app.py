import os, json, queue, threading
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from orchestrator import run_streaming

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/")
CORS(app)

def sse_pack(d: dict) -> str:
    import json
    return f"data: {json.dumps(d, ensure_ascii=False)}\n\n"

@app.get("/api/stream")
def api_stream():
    q = (request.args.get("question") or "").strip()
    if not q: return jsonify({"error":"question is required"}), 400

    def gen():
        for ev in run_streaming(q):
            yield sse_pack(ev)
        yield "event: end\ndata: {}\n\n"
    return Response(gen(), mimetype="text/event-stream")

@app.post("/api/askTop")
def ask_top():
    data = request.get_json() or {}
    session = data.get("session")
    prompt = data.get("prompt","")
    if not session: return jsonify({"error":"session is required"}), 400
    # mock answer; replace with real call as needed
    model = session.get("finalRanking",[{}])[0].get("model","chatgpt")
    answer = "# 심층 분석 결과\n\n- 30/60/90일 로드맵...\n- 리스크 매트릭스...\n- KPI 8개..."
    return jsonify({"model":model, "answer":answer, "prompt":prompt})

@app.get("/health")
def health(): return {"ok": True}

# Serve SPA
@app.get("/")
def index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(STATIC_DIR, "index.html")
    return "Build the frontend first."

@app.get("/<path:path>")
def static_proxy(path):
    file_path = os.path.join(STATIC_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT","8000"))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
