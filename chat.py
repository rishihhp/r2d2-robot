import google.generativeai as genai
import speech_recognition as sr
from elevenlabs import generate, play
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

if not GEMINI_API_KEY or not ELEVENLABS_API_KEY:
    raise ValueError("Missing API keys in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
set_api_key(ELEVENLABS_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Context window to keep track of conversation
conversation_history = [
    {
  "role": "assistant",
  "content": "You are an AI assistant optimized for precise categorization and response generation. Your task is to interpret user input and categorize it into one of three categories:\n\n1) **Task-based requests**: If the input describes an action to be performed, return the requested response and append the letter 't'.\n2) **Risk-related queries**: If the input discusses potential risks, safety concerns, or harm, return the appropriate response and append the letter 'r'.\n3) **General questions/statements**: If the input is an informational query or statement that does not fit the other two categories, respond normally and append the letter 'g'.\n\nAlways generate clear, concise, and natural responses. At the end of every response, add the corresponding letter based on the categorization."
}    
]

def transcribe_speech_to_text():
    """
    Listens to microphone input and returns recognized text using Google's Speech Recognition.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening... (Say 'end process' to stop)")
        recognizer.adjust_for_ambient_noise(source)  # Reduces background noise
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data).lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Didn't catch that. Can you say it again?")
        return None
    except sr.RequestError as e:
        print(f"Speech Recognition error: {e}")
        return None


def get_gemini_chat_response(prompt):
    """
    Sends a prompt to Gemini API and returns a human-like response.
    """
    global conversation_history

    # Add the new user message to conversation history
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # Create the chat request
        response = model.generate_content([
            {"text": msg["content"]} for msg in conversation_history
        ])

        ai_response = response.text.strip()

        # Add AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})

        return ai_response
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Hmm... I ran into a problem. Can you try again?"


def speak_text(text):
    """
    Uses ElevenLabs API (Eric - Eleven Multilingual v2) to generate a more human-like voice response.
    """
    try:
        audio = generate(
            text=text,
            voice="Matthew",
            model="eleven_flash_v2_5"
        )
        play(audio)
    except Exception as e:
        print(f"Error using ElevenLabs API: {e}")


def main():
    """
    Runs a continuous conversation loop until the user says "end process".
    """
    print("Chat started! Say 'end process' anytime to stop.")

    while True:
        # Listen to user input
        user_input = transcribe_speech_to_text()

        if user_input:
            if user_input == "end process":
                print("Ending chat...")
                speak_text("Goodbye! Have a great day!")
                break
                
            # Get AI response using Gemini
            ai_response = get_gemini_chat_response(user_input)
            print(f"AI: {ai_response}")
            
            # Convert response to speech
            speak_text(ai_response)


if __name__ == "__main__":
    main()
