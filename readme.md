# Guess the Prompt Game


## About the Game

**Guess the Prompt Game** is an engaging and interactive web-based game where players challenge their creativity and intuition. The game involves generating an AI-created image based on a hidden prompt and providing a few hints. Players then attempt to guess the original prompt based on the generated image and hints. The game evaluates the similarity between the original prompt and the player's guess using a sophisticated similarity algorithm, providing a fun and educational experience.

### How It Works

1. **Generate an Image:**
   - Start the game by clicking the "Generate Image and Hints" button.
   - The system generates a unique and interesting prompt, which is used to create an AI-generated image.
   - You will also receive three hints extracted from the original prompt to aid in your guessing.

2. **Make Your Guess:**
   - Look at the generated image and read the hints carefully.
   - Enter your guess for what the original prompt might have been.
   - Submit your guess by clicking the "Submit Guess" button.

3. **View the Results:**
   - The game generates a new image based on your guessed prompt.
   - You will receive a similarity score that indicates how close your guess was to the original prompt.
   - Both the original prompt and your guessed prompt are displayed along with the respective images, allowing you to compare and learn.

### Game Features

- **AI-Generated Content:** Leverages powerful AI models to create unique prompts and generate images, ensuring a new experience every time you play.
- **Hints System:** Provides three hints to guide your guessing, striking a balance between challenge and assistance.
- **Similarity Score:** Uses Jaro-Winkler similarity to calculate a score, giving you insight into how accurate your guess was.
- **Interactive UI:** A user-friendly interface designed for seamless interaction and enhanced game experience.

### Screenshots

Here are some screenshots of the game in action:

1. **Start Screen:**
   - ![Start Screen](screenshots/start_screen.png)

2. **Generated Image and Hints:**
   - ![Generated Image](screenshots/generated_image.png)

3. **Submit Your Guess:**
   - ![Submit Guess](screenshots/submit_guess.png)

4. **View Results:**
   - ![View Results](screenshots/view_results.png)

---


## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/guess-the-prompt-game.git
    cd guess-the-prompt-game
    ```

2. **Install the necessary Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```sh
    GROQ_API_KEY=your_groq_api_key
    DEEPINFRA_API_KEY=your_deepinfra_api_key
    ```

4. **Run the FastAPI application:**
    ```sh
    uvicorn main:app --reload
    ```

5. **Open `index.html` in your web browser:**
    Navigate to the root directory and open the `index.html` file in your preferred web browser.

## Usage

1. **Generate an Image and Hints:**
    - Click the "Generate Image and Hints" button to get a new image based on a generated prompt and receive three hints.

2. **Guess the Prompt:**
    - Enter your guessed prompt into the input field and click "Submit Guess."
    - View the similarity score between your guessed prompt and the original prompt, along with the generated image for your guessed prompt.

## Endpoints

### `GET /get-image`
Generates a new image based on a unique prompt and provides three hints from the prompt.
- **Response:**
    ```json
    {
        "prompt": "Generated prompt text",
        "imageUrl": "URL of the generated image",
        "hints": ["hint1", "hint2", "hint3"]
    }
    ```

### `POST /get-score`
Calculates the similarity score between the original prompt and the guessed prompt.
- **Request Body:**
    ```json
    {
        "originalPrompt": "Original prompt text",
        "guessedPrompt": "Guessed prompt text"
    }
    ```
- **Response:**
    ```json
    {
        "generatedImage": "URL of the image generated from the guessed prompt",
        "score": "Similarity score",
        "originalPrompt": "Original prompt text"
    }
    ```


Make sure to install the Python packages using `pip install -r requirements.txt` and include the jQuery library in your HTML.

