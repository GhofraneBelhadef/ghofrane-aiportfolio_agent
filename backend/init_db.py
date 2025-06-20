import sqlite3

conn = sqlite3.connect('database/projects.db')
c = conn.cursor()

# Table for projects
c.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    video_link TEXT,
    code_path TEXT,
    tags TEXT
)
''')

# Table for interaction logs (for dashboard)
c.execute('''
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY,
    question TEXT,
    count INTEGER,
    timestamp TEXT
)
''')

# Insert sample project data
c.execute('''
INSERT INTO projects (title, description, video_link, code_path, tags)
VALUES (?, ?, ?, ?, ?)
''', (
    "Image Classification",
    "Built a CNN to classify medical images using TensorFlow.",
    "https://youtube.com/example",
    "https://github.com/ghofrane/image-classification",
    "IA, Computer Vision, TensorFlow"
))

conn.commit()
conn.close()