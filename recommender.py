import openai
import pandas as pd
import sqlite3

openai.api_key = "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"

def build_prompt(userinfo, content_df):
    content_str = "\n".join([
    f"- {row['name']} ({row['type']})"
    for _, row in content_df.iterrows()
])
    prompt = f"""
You are an AI wellness assistant. Based on the user's profile, recommend the top 3 most relevant content items from the list.

User Profile:
- Name: {userinfo['name']}
- Age: {userinfo['age']}
- Goals: {userinfo['goals']}
- Interests: {userinfo['interests']}
- Content Preference: {userinfo['content_preference']}

Available Content:
{content_str}

Respond with the top 3 recommended titles in order, and explain briefly why each is recommended.
"""
    return prompt

def get_recommendations(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for mental health and wellness."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def generate_recommendations_for_pending_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get users who don’t yet have recommendations
    user_rows = cursor.execute("SELECT * FROM userinfo WHERE recommended = 0").fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Load content
    content_df = pd.read_sql("SELECT * FROM content", conn)

    for row in user_rows:
        user_info = dict(zip(columns, row))
        prompt = build_prompt(userinfo, content_df)
        recommendations = get_recommendations(prompt)

        # Save the result into a new column (or a separate table)
        cursor.execute("UPDATE userinfo SET recommendations = ?, recommended = 1 WHERE id = ?", ...),
        (recommendations, userinfo['id'])
        conn.commit()

    conn.close()