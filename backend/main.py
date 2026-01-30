from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read your Groq API key
api_key = os.environ.get("GROQ_API_KEY")

# Initialize OpenAI client for Groq API if API key exists
if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = None  # fallback to local responses

# Pydantic model for incoming requests
class ChatRequest(BaseModel):
    message: str

# FastAPI app
app = FastAPI(title="BrainBot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


username = None
Capitals = {
    "usa": "Washington, D.C.",
    "united states": "Washington, D.C.",
    "india": "New Delhi",
    "france": "Paris",
    "germany": "Berlin",
    "italy": "Rome",
    "spain": "Madrid",
    "canada": "Ottawa",
    "japan": "Tokyo",
    "china": "Beijing",
    "uk": "London",
    "united kingdom": "London",
    "mexico": "Mexico City",
    "brazil": "Brasília",
    "australia": "Canberra",
}


def get_bot_response(user_message: str) -> str:
    """
    Returns a response from BrainBot.
    Uses Groq API if available; otherwise, provides offline fallback.
    """
    global username
    clean_message = user_message.strip()
    msg_lower = clean_message.lower()

    if client:
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are BrainBot, a helpful and knowledgeable AI assistant. "
                        "Explain math step-by-step. Explain science clearly. "
                        "Answer history questions with accurate facts. "
                        "Be concise, clear, and friendly."
                    )
                },
                {"role": "user", "content": clean_message}
            ]
            
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Sorry, API request failed. ({str(e)})"
    else:
        if any(greet in msg_lower for greet in ["hello", "hi", "hey"]):
            return "Hello! I am BrainBot. How are you today?"
         
        elif "my name is" in msg_lower:
            user_name = clean_message.split("my name is")[-1].strip().title()
            return f"Nice to meet you, {user_name}!"
        
        

        
        
        
        
        
        

        #Mathematics 
        elif any(char.isdigit() for char in clean_message) and any(op in msg_lower for op in ["+", "-", "*", "/", "calculate", "solve"]):
            try:
                result = eval(clean_message.replace("x", "*"))
                return f"The answer is {result}"
            except:
                return "I can only solve simple arithmetic offline. Try a simpler calculation."
            
        #Science
        elif any(word in msg_lower for word in ["physics", "chemistry", "biology", "photosynthesis", "gravity"]):
            if "photosynthesis" in msg_lower:
                return "Photosynthesis is the process by which plants use sunlight to convert carbon dioxide and water into glucose and oxygen."
            elif "gravity" in msg_lower:
                return "Gravity is a force that attracts objects with mass toward each other. On Earth, it gives weight to objects."
            else:
                return "I know some basic science facts, but my AI brain online can give more detailed explanations."
            

        #History
        elif "capital" in msg_lower:
            for country, capital in Capitals.items():
                if country in msg_lower:
                    return f"The capital of{country.title} is {capital}. "
                return "I know the capitals of many countries. Go ahead, Ask"
        
        elif any(word in msg_lower for word in ["war", "history", "who", "when", "wwii","wwi"]):
            if "napoleon" in msg_lower:
                return "Napoleon Bonaparte was a French military leader and emperor who lived from 1769 to 1821."
            elif "wwii" in msg_lower or "world war 2" in msg_lower:
                return "World War II (1939–1945) was a global conflict that pitted the Axis Powers (Germany, Italy, Japan) against the Allies (Great Britain, the United States, the Soviet Union, China). It was the deadliest war in history, resulting in an estimated 60-80 million deaths, including the state-sponsored genocide of the Holocaust. The conflict ended with the defeat of the Axis powers and reshaped the modern world, leading to the creation of the United Nations and setting the stage for the Cold War."
            elif "civil war" in msg_lower:
                return "The American Civil War lasted from 1861 to 1865 between the Union and the Confederacy."
            elif "wwi" in msg_lower:
                return " World War I (1914–1918) was a global struggle between the Allied Powers (led by France, Britain, and Russia) and the Central Powers (led by Germany and Austria-Hungary). Triggered by the assassination of Archduke Franz Ferdinand, the conflict became infamous for its grueling trench warfare and the first major use of tanks and chemical weapons. The war ended with an armistice on November 11, 1918, resulting in over 16 million deaths and the collapse of four major empires."
            else:
                return "I can answer basic history questions, but my AI brain online can provide more details."
        
            


        #News    
        elif any(word in msg_lower for word in ["news", "local"]):
            return (
        "Here are some news sources:\n"
        "• Google News: https://news.google.com\n"
        "• CNN: https://www.cnn.com\n"
        "• BBC: https://www.bbc.com/news"
    )
        

        
        else:
            return "Sorry, I didn't understand. Try asking math, science, or history questions."


            


   
         
            

# FastAPI endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    reply = get_bot_response(request.message)
    return {"reply": reply}


@app.get("/")
def root():
    return {"status": "BrainBot API is running"}
