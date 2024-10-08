from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mooding-up.vercel.app","https://papapa.work"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.local")
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("CHATGPT_API_TOKEN")


if not api_key:
    print("API key not found.")
else:
    openai.api_key = api_key
    print("ok，api設定完成")

class MessageRequest(BaseModel):
    prompt: str


system_message = {
    "role": "system",
    "content": "你是溫柔的輔導老師，請用一次單元型模型，來鼓勵與你談話的人，給他們方向和建議，每次談話不超過20個字。"
}

class AiTalk:
    def __init__(self):
        self.messages = [system_message]

    def ai(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        
        try:
            print(f"Sending request to OpenAI with messages: {self.messages}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
            reply = response["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

ai_talk = AiTalk()

@app.get("/")
def read_root():
    return {"Hello": "welcome"}

@app.post("/chat")
async def chat(request: MessageRequest):
    try:
        print(f"Received message: {request.prompt}")
        reply = ai_talk.ai(request.prompt)
        print(f"Generated reply: {reply}")
        return {"response": reply}
    except Exception as e:
        print(f"why Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")