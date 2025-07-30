from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import shutil, os

from query import ask_question
from ingest import ingest_uploaded_file
from google_api.gmail import read_latest_emails
from google_api.calendar import list_upcoming_events, create_calendar_event

app = FastAPI()

# CORS (for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "TARS is alive"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = f"uploads/{file.filename}" 
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer) #copies/stores file to local
    try:
        ingest_uploaded_file(filename)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query")
async def query_doc(question: str = Form(...)):
    try:
        answer = ask_question(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/gmail/messages")
def gmail_messages():
    return {"emails": read_latest_emails()}

@app.get("/calendar/events")
def calendar_events():
    return {"events": list_upcoming_events()}

@app.post("/calendar/create")
def calendar_create(summary: str = Form(...), start: str = Form(...), end: str = Form(...)):
    link = create_calendar_event(summary, start, end)
    return {"event_link": link}
