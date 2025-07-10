from typing import Union
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

VALID_TOKEN = "secrettoken"

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()
app.mount("/", StaticFiles(directory="static",html = True), name="static")



class LoginData(BaseModel):
    username: str
    password: str

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for login endpoint
        if request.url.path == "/login":
            return await call_next(request)

        # Get token from cookies or Authorization header
        token = request.cookies.get("token") or request.headers.get("Authorization")

        if token == f"Bearer {VALID_TOKEN}" or token == VALID_TOKEN:
            return await call_next(request)

        # Invalid token
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or missing token! Sorry!"},
        )
        response.delete_cookie("token")
        return response

app.add_middleware(AuthMiddleware)

# Pydantic model for login request body
class LoginCredentials(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginData, response: Response):
    if data.username == "free" and data.password == "mason":
        # Return token in both cookie and body
        response.set_cookie(key="token", value=VALID_TOKEN, httponly=True)
        return {"token": VALID_TOKEN}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.get("/secure-data")
async def secure_data():
    return {"message": "This is secret society data!"}

@app.get("/")
async def root():
    return FileResponse('index.html')
