from jose import jwt,JWTError
from datetime import timedelta,datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "fastapi"
EXPIRE_TIME = 30
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    encode_text = data.copy()
    expire = (datetime.now()+timedelta(minutes = EXPIRE_TIME))
    encode_text.update({"exp":expire})
    token = jwt.encode(encode_text,SECRET_KEY,algorithm = ALGORITHM)
    return token


def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except:
        raise HTTPException(status_code=401, detail="Invalid token")