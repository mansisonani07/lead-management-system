import os
import json
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is where your Groq key is used
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT,
            email           TEXT,
            phone           TEXT,
            message         TEXT,
            source          TEXT,
            classification  TEXT,
            suggested_reply TEXT,
            status          TEXT DEFAULT 'new',
            created_at      TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Lead(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    source: str

class ClassifyRequest(BaseModel):
    message: str

class StatusUpdate(BaseModel):
    status: str

def classify_with_groq(message: str):
    prompt = f"""You are a sales lead classifier.

Classify this message as exactly one of: Hot, Warm, or Cold
- Hot  = clear buying intent, mentions budget or timeline
- Warm = interested but exploring, has questions
- Cold = spam, unsubscribe, just saying hello with no intent

Also write a 1-2 sentence friendly reply to the person.

Message: "{message}"

Reply ONLY with this JSON format, nothing else:
{{"classification": "Hot", "suggested_reply": "Your reply here."}}"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

@app.post("/lead")
def create_lead(lead: Lead):
    try:
        result = classify_with_groq(lead.message)
        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leads
              (name, email, phone, message, source, classification, suggested_reply, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'new', ?)
        """, (
            lead.name, lead.email, lead.phone, lead.message, lead.source,
            result["classification"], result["suggested_reply"],
            datetime.now().isoformat(),
        ))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads")
def get_all_leads():
    conn = sqlite3.connect("leads.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/classify")
def classify_only(request: ClassifyRequest):
    try:
        return classify_with_groq(request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/leads/{lead_id}/status")
def update_status(lead_id: int, update: StatusUpdate):
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (update.status, lead_id))
    conn.commit()
    conn.close()
    return {"message": f"Lead {lead_id} updated"}