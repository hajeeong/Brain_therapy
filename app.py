from flask import Flask, request, jsonify
from recommender import generate_recommendations_for_pending_users
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)
DB_PATH = "braintherapy" 

# -------------------------
# User Signup Route
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert new user info into DB (set 'recommended' to 0)
    cursor.execute("""
    INSERT INTO userinfo (name, age, personality, hobbies, music_taste, emotional_needs, common_moods, learning_style, recommended, recommendations)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
""", (data['name'], data['age'], data['personality'], data['hobbies'], data['music_taste'], data['emotional_needs'], data['common_moods'], data['learning_style']))
    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful! Recommendations will be available soon."})

# -------------------------
# Scheduler for AI Recommender
# -------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: generate_recommendations_for_pending_users(DB_PATH), trigger="interval", seconds=30)
scheduler.start()

# -------------------------
# Run Flask app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
