from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Read your Groq API key
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize OpenAI client for Groq API if API key exists
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None  # fallback to local responses

# Pydantic model for incoming requests
class ChatRequest(BaseModel):
    message: str

# FastAPI app
app = FastAPI(title="BrainBot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


username = None

#  ------------
#  | Subjects |
#  ------------
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


States_of_US = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

count = len(States_of_US)


Family = {
    "Sudeep Telang" : "Father",
    "Deepa Telang"  : "Mother",
    "Dev Telang" : "Son and My Creator",
    "Diya Telang": "Sister",
    "Sachin Telang": "Uncle",
    "Arpana Telang" : "GrandMother",
    "Sudhir Telang" : "GrandFather"
}


Physics = {
    "force": "A force is a push or pull that can change an object's motion or shape.",
    "motion": "Motion is the change in position of an object over time.",
    "velocity": "Velocity is the speed of an object in a specific direction.",
    "acceleration": "Acceleration is the rate at which velocity changes over time.",
    "gravity": "Gravity is the force that attracts objects with mass toward each other.",
    "mass": "Mass is the amount of matter in an object.",
    "weight": "Weight is the force of gravity acting on an object.",
    "energy": "Energy is the ability to do work.",
    "kinetic energy": "Kinetic energy is the energy an object has due to its motion.",
    "potential energy": "Potential energy is stored energy based on an object's position or condition.",
    "work": "Work is done when a force causes an object to move a distance.",
    "power": "Power is the rate at which work is done.",
    "momentum": "Momentum is the product of an object's mass and velocity.",
    "friction": "Friction is a force that resists motion between two surfaces in contact.",
    "electricity": "Electricity is the flow of electric charge.",
    "current": "Electric current is the flow of electric charge through a conductor.",
    "voltage": "Voltage is the electrical potential difference between two points.",
    "resistance": "Resistance is the opposition to the flow of electric current.",
    "wave": "A wave is a disturbance that transfers energy through space or matter.",
    "frequency": "Frequency is the number of wave cycles per second.",
    "atom": "An atom is the smallest unit of matter that retains the properties of an element."
}







Biology = {
    "cell": "A cell is the basic structural and functional unit of all living organisms.",
    "dna": "DNA is the molecule that carries genetic information used in growth, development, and reproduction.",
    "photosynthesis": "Photosynthesis is the process by which plants use sunlight, carbon dioxide, and water to make glucose and oxygen.",
    "mitosis": "Mitosis is the process by which a cell divides to produce two identical daughter cells.",
    "meiosis": "Meiosis is a type of cell division that produces four genetically different sex cells.",
    "osmosis": "Osmosis is the movement of water across a semi-permeable membrane from low solute concentration to high solute concentration.",
    "enzyme": "An enzyme is a protein that speeds up chemical reactions in living cells.",
    "ecosystem": "An ecosystem is a community of living organisms interacting with their physical environment.",
    "homeostasis": "Homeostasis is the ability of an organism to maintain a stable internal environment.",
    "evolution": "Evolution is the change in traits of populations over generations through natural selection.",
    "respiration": "Respiration is the process by which cells convert glucose into energy.",
    "chlorophyll": "Chlorophyll is the green pigment in plants that absorbs light for photosynthesis."
}

#----------------------------------------------------------------------------------------------------------------------------------------



def get_bot_response(user_message: str) -> str:
    """
    Returns a response from BrainBot.
    Uses Groq API if available; otherwise, provides offline fallback.
    """
    global username
    clean_message = user_message.strip()
    msg_lower = clean_message.lower()

    if model:
        try:
            response = model.generate_content(
                f" You are Brainbot, A helpful AI chatbot..\nUser: {clean_message}"
            )
            return response.text
        except Exception as e:
            print("Gemini error:", e)
            
            
            
    else:
        if any(greet in msg_lower for greet in ["hello", "hi", "hey"]):
            return "Hello! I am BrainBot. How are you today?"
         
        elif "my name is" in msg_lower:
            user_name = clean_message.split("my name is")[-1].strip().title()
            return f"Nice to meet you, {user_name}!"
        
        

        
        #Family
        elif "family" in msg_lower:
            return f"Here is the Telang Family: {Family}"
        
        
        
        

        #Mathematics 
        elif any(char.isdigit() for char in clean_message) and any(op in msg_lower for op in ["+", "-", "*", "/", "calculate", "solve"]):
            try:
                result = eval(clean_message.replace("x", "*"))
                return f"The answer is {result}"
            except:
                return "I can only solve simple arithmetic offline. Try a simpler calculation."
            
        #Science
        elif any(term in msg_lower for term in Physics):
            for term, definition in Physics.items():
                    if term in msg_lower:
                        return definition
            
            
        elif any(term in msg_lower for term in Biology):
            for term, definition in Biology.items():
                if term in msg_lower:
                    return definition + "Another One!"
            
            else:
                return "I know some basic science facts, but my AI brain online can give more detailed explanations."
            

       # World Countries and US states
        elif "capital" in msg_lower:
            for country, capital in Capitals.items():
                if country in msg_lower:
                     display_country = country.upper() if country in ["usa", "uk"] else country.title()
                     return f"The capital of {display_country} is {capital}."
            return "I know the capitals of many countries. Go ahead, Ask"
        elif "states" in msg_lower:
            state_list = ", ".join(s.title() for s in States_of_US)
            return f"Here are some U.S. states: {state_list}" + f"As you can see, there are {count} states "  


         #History
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
    return {"status": "BrainBot API is running 🚀"}



