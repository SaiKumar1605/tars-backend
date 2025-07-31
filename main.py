from fastapi import FastAPI, File, UploadFile, Form, Depends, APIRouter 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi #added later for firabse authorization (APIRouter)

import shutil, os

from query import ask_question
from ingest import ingest_uploaded_file
from google_api.gmail import read_latest_emails
from google_api.calendar import list_upcoming_events, create_calendar_event
from slack_bot.client import send_slack_message
from auth.firebase import verify_token

app = FastAPI()

#For endroute secure docs
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="TARS Backend API",
#         version="1.0.0",
#         description="Secure endpoints with Firebase",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }
#     for path in openapi_schema["paths"]:
#         for method in openapi_schema["paths"][path]:
#             openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# 👇 Apply the custom OpenAPI
# app.openapi = custom_openapi

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
    
    # filename = f"uploads/{file.filename}" 
    # with open(filename, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer) #copies/stores file to local

    temp_path = f"/tmp/{file.filename}"  # safe on Render & temporary path on 
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        ingest_uploaded_file(temp_path)
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

@app.post("/slack/send")
def slack_send(channel: str = Form(...), message: str = Form(...)):
    result = send_slack_message(channel, message)
    if result["ok"]:
        return {"status": "sent", "timestamp": result["ts"]}
    else:
        return {"error": result["error"]}
    
#End point to secure routes    
# @app.get("/secure-docs")
# def secure_docs(user=Depends(verify_token)):
#     return {
#         "message": f"Welcome, {user['email']}",
#         "uid": user["uid"]
#     }

router = APIRouter() 

@router.get("/secure-docs")
def secure_docs(user=Depends(verify_token)):
    # return {"message": "Authorized access!","message": f"Welcome, {user['email']}" ,"uid": user["uid"]}
    return {
        "status": "Authorized",
        "welcome": f"Welcome, {user['email']}",
        "uid": user["uid"]
    }

app.include_router(router)