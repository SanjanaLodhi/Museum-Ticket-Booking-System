from flask import Flask, request, render_template, jsonify
import json
import asyncio
import aiohttp
from deep_translator import GoogleTranslator

# Initialize the app
app = Flask(__name__)

# Load the knowledge base
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Cache for frequently asked questions
response_cache = {}
user_data={}


def find_answer_in_knowledge_base(user_query, language="en"):
    """Search the knowledge base for the user's query."""
    user_query = user_query.lower()
    for item in knowledge_base:
        if item["question"].lower() == user_query:
            if language == "ur":
                return item.get("urdu_answer", item["answer"])
            elif language == "hi":
                return item.get("hindi_answer", item["answer"])
            elif language=="fr":
                return item.get("franch_answer",item["answer"])
            else:
                return item["answer"]
    return "Sorry, I couldn't find an answer to your question."


async def fetch_ollama_response(session, prompt):
    """Fetch a response from the Ollama API asynchronously."""
    payload = {
        "model": "hf.co/bartowski/Dolphin3.0-Llama3.1-8B-GGUF:latest",
        "prompt": prompt, 
        "stream": False,
    }
    async with session.post(OLLAMA_API_URL, json=payload) as response:
        if response.status == 200:
            data = await response.json()
            return data["response"]
        return "Sorry, I couldn't generate a response. Please try again later."


def generate_response(user_query, language="en"):
    """Generate a response using the knowledge base or Ollama if necessary."""
    
    # 1. First, check the cache for a response
    if user_query in response_cache:
        return response_cache[user_query]

    # 2. Check if the query exists in the knowledge base
    answer = find_answer_in_knowledge_base(user_query, language)
    if answer:
        response_cache[user_query] = answer  # Cache it
        return answer

    # 3. If not found, use Ollama to generate a response
    prompt = f"""You are an AI assistant. Answer the following user query: 
    Knowledge Base:
    {json.dumps(knowledge_base, indent=2)}

    User Query: {user_query}"""

    async def get_response():
        async with aiohttp.ClientSession() as session:
            response = await fetch_ollama_response(session, prompt)
            if language == "ur":
                response = GoogleTranslator(source="auto", target="ur").translate(
                    response
                )
            elif language == "hi":
                response = GoogleTranslator(source="auto", target="hi").translate(
                    response
                )
            elif language == "fr":
                response = GoogleTranslator(source="auto", target="fr").translate(
                    response
                )
            response_cache[user_query] = response  # Cache the response
            return response

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(get_response())
    loop.close()

    return response


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.form["user_query"]
    language = request.form.get("language", "en")  # Default to English

    # Store user's language preference
    if "user_id" in request.form:  
        user_id = request.form["user_id"]  
        user_data[user_id] = user_data.get(user_id, {})
        user_data[user_id]["language"] = language  
    else:
        user_id = "default_user"
        user_data[user_id] = user_data.get(user_id, {})
        user_data[user_id]["language"] = language  

    # Retrieve user's preferred language
    language = user_data[user_id]["language"]

    # Check if user provided their name
    if "my name is" in user_query.lower():
        user_name = user_query.split("my name is")[-1].strip()
        user_data[user_id]["name"] = user_name
        response = f"Thanks, {user_name}! Can you please provide your email?"

    # Check if user provided their email
    elif "@" in user_query and "." in user_query:
        user_data[user_id]["email"] = user_query.strip()
        response = f"Thank you, {user_data[user_id]['name']}! Now, can you please provide your phone number?"

    # Check if user provided their phone number (Assuming it's 10 digits)
    elif user_query.isdigit() and len(user_query) == 10:
        user_data[user_id]["phone"] = user_query
        response = f"Great, {user_data[user_id]['name']}! Your details are saved: Email - {user_data[user_id]['email']}, Phone - {user_data[user_id]['phone']}."

    else:
        response = find_answer_in_knowledge_base(user_query, language)

    # Translate response if needed
    if language != "en":
        response = GoogleTranslator(source="auto", target=language).translate(response)

    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(debug=True)
