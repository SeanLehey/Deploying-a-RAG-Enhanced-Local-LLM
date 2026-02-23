import json
import lancedb
import ollama
from http.server import HTTPServer, BaseHTTPRequestHandler
from sentence_transformers import SentenceTransformer

# Settings
DB_PATH = r"C:\Users\Temporary\Documents\RAGProject\VectorDB"
MODEL_NAME = "qwen3-coder:30b"
N_RESULTS = 5
PORT = 8765

print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
db = lancedb.connect(DB_PATH)
table = db.open_table("godot_docs")
print(f"Ready. Server starting on http://localhost:{PORT}\n")


def query_rag(question):
    question_embedding = embedding_model.encode(question).tolist()

    results = table.search(question_embedding).limit(N_RESULTS).to_list()

    context_parts = []
    for r in results:
        context_parts.append(
            f"[Source: {r['source']} | Section: {r['section']}]\n{r['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "You are a helpful Godot game engine assistant. "
        "You are helping a developer who is coding in GDScript. "
        "Answer questions using only the provided documentation context. "
        "If the answer is not in the context, say so clearly."
    )

    user_prompt = f"Documentation context:\n\n{context}\n\nQuestion: {question}"

    response = ollama.chat(
        model=MODEL_NAME,
        options={"num_ctx": 16384},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    sources = [{"source": r["source"], "section": r["section"]} for r in results]
    return response.message.content, sources


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"Request: {args[0]} {args[1]}")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_POST(self):
        if self.path == "/query":
            length = int(self.headers["Content-Length"])
            body = json.loads(self.rfile.read(length))
            question = body.get("question", "").strip()

            if not question:
                self.send_response(400)
                self.end_headers()
                return

            print(f"Question: {question}")
            answer, sources = query_rag(question)
            print(f"Answer generated.\n")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "answer": answer,
                "sources": sources
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Server running at http://localhost:{PORT}")
    print("Open interface.html in your browser to start querying.")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
