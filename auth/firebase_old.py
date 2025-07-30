import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException
from typing import Optional # for token authorization debug


cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

# def verify_token(authorization: str = Header(...)):
#     try:
#         token = authorization.split(" ")[1]
#         decoded_token = auth.verify_id_token(token)
#         return decoded_token  # Contains uid, email, etc.
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")


#Just other version to debug correctly
def verify_token(authorization: Optional[str] = Header(None)):
    #print("Incoming header:", authorization)
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    try:
        # token = authorization.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")