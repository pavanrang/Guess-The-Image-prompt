import os
import random
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jellyfish import jaro_winkler_similarity

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://127.0.0.1:8001",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Function to generate a prompt using Groq
def Groq(query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.8,
        "max_tokens": 1024,
        "top_p": 1,
        "stop": None,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        llm_response = response.json()
        return llm_response
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def prompt_generator():
    prompt_template = "Generate a unique and brief prompt each time, with clear instructions and specifications, to create a good image for the Guess the Prompt game. The prompt should be specific enough to inspire an interesting image, but vague enough to make guessing challenging and fun. prompt should be brief, just 6-7 words."
    response = Groq(prompt_template)
    if response:
        return response['choices'][0]['message']['content']
    return None

# DeepInfra image generation function
def generate(prompt: str, model: str = "stability-ai/sdxl", negative_prompt: str = "", width: int = 512, height: int = 512, num_outputs: int = 1, prompt_strength: float = 0.8):
    url = f"https://api.deepinfra.com/v1/inference/{model}"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPINFRA')}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
    payload = {
        "input": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_outputs": num_outputs,
            "prompt_strength": prompt_strength
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()['output']
        if data is not None:
            return data  # Return the list of image URLs
        else:
            return response.text

    except Exception as e:
        return f"ERROR --> {e}\n{response.text}"

# Pydantic model for request body of /get-score endpoint
class PromptRequest(BaseModel):
    originalPrompt: str
    guessedPrompt: str

# Function to calculate similarity using Jaro-Winkler similarity
def calculate_similarity_score(text1: str, text2: str) -> float:
    similarity_score = jaro_winkler_similarity(text1, text2)
    return similarity_score

# Endpoint to handle GET request to generate an image and hints
@app.get("/get-image")
async def get_image():
    try:
        # Step 1: Generate a unique scene description
        prompt = prompt_generator()
        if not prompt:
            raise HTTPException(status_code=500, detail="Failed to generate prompt")

        # Step 2: Generate an image from the text description using your custom function
        result = generate(prompt)
        if isinstance(result, str) and result.startswith("ERROR"):
            raise HTTPException(status_code=500, detail=result)

        # Assuming the result is a list of image URLs
        image_url = result[0] if result else None
        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to generate image")

        # Step 3: Generate hints (3 random words from the prompt)
        prompt_words = prompt.split()
        hints = random.sample(prompt_words, 3)

        # Step 4: Return the response with the prompt, image URL, and hints
        return {"prompt": prompt, "imageUrl": image_url, "hints": hints}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to handle POST request to get the similarity score
@app.post("/get-score")
async def get_score(request: PromptRequest):
    try:
        # Generate image using DeepInfra
        image_url = generate(request.guessedPrompt)
        if "ERROR" in image_url:
            raise HTTPException(status_code=500, detail=image_url)

        # Calculate text similarity
        similarity_score = calculate_similarity_score(request.originalPrompt, request.guessedPrompt)

        # Return the results
        return {
            "generatedImage": image_url[0],
            "score": similarity_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
