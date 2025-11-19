from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    mood: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    mood: str

def generate_reply(message: str, mood: str) -> str:
    message = message.strip()

    if mood == "happy":
        style_prefix = "😄 Kamu lagi happy ya! Seru banget. "
    elif mood == "sad":
        style_prefix = "😢 Aku ikut ngerasain, semoga kamu cepat lebih baik ya. "
    elif mood == "angry":
        style_prefix = "😠 Wah, kedengeran kamu lagi kesal. Tarik napas dulu ya. "
    elif mood == "neutral":
        style_prefix = "🙂 Oke, aku dengerin. "
    else:
        style_prefix = ""

    base_reply = (
        f'Kamu barusan bilang: "{message}". '
        "Ceritain lagi kalau mau, aku siap dengerin dan bantu sebisanya."
    )

    return style_prefix + base_reply

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    mood = req.mood or "neutral"
    reply = generate_reply(req.message, mood)
    return ChatResponse(reply=reply, mood=mood)

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
