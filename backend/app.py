from flask import Flask, request, jsonify
import openai
import sqlite3
import os
from gtts import gTTS
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Allow frontend requests
load_dotenv()  # Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.get_json()
    question = data.get("question")
    persona = data.get("persona", "default")
    local_info = get_context_from_db(question)

    prompt = f"Contexte personnel : {local_info}\nQuestion : {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Tu es GhofraneBot, un assistant vocal IA. Persona: {persona}"},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content']

    # Save interaction to database
    save_interaction(question)

    # Generate TTS
    tts = gTTS(answer, lang='fr')
    tts.save("audio/reply.mp3")
    return jsonify({"answer": answer, "audio": "/audio/reply.mp3"})

@app.route('/projects', methods=['GET'])
def get_projects():
    conn = sqlite3.connect("database/projects.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/why-synhive', methods=['GET'])
def why_synhive():
    bio = "Je suis étudiante en ingénierie informatique passionnée par l’IA, la data science et la vision par ordinateur."
    projets = "J’ai développé un agent IA multimodal, un modèle de classification d’images médicales, et un chatbot vocal."
    valeurs = "Synhive valorise la transformation numérique, l’automatisation et l’innovation, des domaines où mes projets s’alignent parfaitement."
    message = f"{bio}\n\nCe que je peux apporter à Synhive : {projets}\n\nConnexion avec les valeurs : {valeurs}"
    return jsonify({"message": message})

@app.route('/analytics', methods=['GET'])
def analytics():
    conn = sqlite3.connect("database/projects.db")
    cur = conn.cursor()
    cur.execute("SELECT question, count, timestamp FROM interactions ORDER BY count DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

def get_context_from_db(query):
    conn = sqlite3.connect("database/projects.db")
    c = conn.cursor()
    c.execute("SELECT description FROM projects WHERE title LIKE ? OR tags LIKE ?", ('%' + query + '%', '%' + query + '%'))
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""

def save_interaction(question):
    conn = sqlite3.connect("database/projects.db")
    c = conn.cursor()
    c.execute("SELECT count FROM interactions WHERE question = ?", (question,))
    result = c.fetchone()
    if result:
        c.execute("UPDATE interactions SET count = count + 1, timestamp = datetime('now') WHERE question = ?", (question,))
    else:
        c.execute("INSERT INTO interactions (question, count, timestamp) VALUES (?, 1, datetime('now'))", (question,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    os.makedirs("audio", exist_ok=True)  # Create audio folder
    app.run(debug=True)