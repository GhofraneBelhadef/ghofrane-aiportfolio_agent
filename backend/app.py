from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/projects', methods=['GET'])
def get_projects():
    try:
        conn = sqlite3.connect("database/projects.db")
        cur = conn.cursor()
        cur.execute("SELECT title, description, tags FROM projects")
        projects = cur.fetchall()
        conn.close()
        return jsonify([{"title": p[0], "description": p[1], "tags": p[2]} for p in projects])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    persona = data.get('persona', 'default')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    try:
        conn = sqlite3.connect("database/projects.db")
        cur = conn.cursor()
        cur.execute("SELECT title, description, tags FROM projects")
        projects = cur.fetchall()
        conn.close()
        context = "\n".join([f"Project: {p[0]}\nDescription: {p[1]}\nTags: {p[2]}" for p in projects])
        persona_prompts = {
            'default': "You are an AI assistant showcasing Ghofrane's AI portfolio.",
            'technical': "You are a technical AI assistant, providing detailed answers.",
            'creative': "You are a creative AI assistant, using engaging storytelling."
        }
        system_prompt = persona_prompts.get(persona, persona_prompts['default'])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)