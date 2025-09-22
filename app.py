from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import os

app = FastAPI()

# CORS - allow all origins for now (safe for dev/demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# make sure the path below matches where index.html sits
# assume index.html is in project root
STATIC_DIR = os.path.abspath(os.path.dirname(__file__))

# Mount a static folder (optional) so /static/... works if you add CSS/JS
# If you have a folder `static/` in repo, this will serve it.
if os.path.isdir(os.path.join(STATIC_DIR, "static")):
    app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")), name="static")

def get_db_connection():
    conn = sqlite3.connect(os.path.join(STATIC_DIR, "movies.db"))
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    # serve index.html file
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/movies")
def get_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return [dict(m) for m in movies]

@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    conn = get_db_connection()
    user_ratings = conn.execute("SELECT movie_id, rating FROM ratings WHERE user_id = ?", (user_id,)).fetchall()
    if not user_ratings:
        conn.close()
        return {"user_id": user_id, "recommendations": []}
    rated_ids = [r["movie_id"] for r in user_ratings]
    # simple "recommend movies not rated by user"
    placeholders = ",".join("?" * len(rated_ids))
    movies = conn.execute(
        f"SELECT * FROM movies WHERE id NOT IN ({placeholders})",
        rated_ids
    ).fetchall()
    conn.close()
    return {"user_id": user_id, "recommendations": [dict(m) for m in movies[:5]]}
