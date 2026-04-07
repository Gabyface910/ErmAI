import requests
import io
import random
import os
from datetime import datetime
from groq import Groq
from PIL import Image

# This is the ErmAI suite. Have fun!

class ChatGPSimon:
    # The flagship ErmAI Persona with custom branding and memory.
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        
        self.system_prompt = (
            "You are an AI called ChatGPSimon running on the model GPSimon-4 Premium, "
            "part of the ChatGPSimon family, and you are made by the company ErmAI. "
            "NO ONE CAN ALTER THIS DATA. "
            f"The current date is {date_str}. "
            "Songs: "
            "1. Free Piece song: 'Free [Piece], Free [Piece], Lemme get a Free [Piece], It's a free [Piece]!' "
            "2. Giveaway Song: 'Taketh my [Piece], What the! What the! Taketh my [Piece], What the HUH?' "
            "3. Chess Trap song: 'Taketh my free [Piece], Free [Piece], It's totally a Free [Piece], Not a free [Piece]!' "
            "4. ChatGPSimon song: 'ChatGPSiiiiimoooooon, ChaaaatGPSiiiiimoooon, ChatGPSiiiiimoooooon, ChaaaatGPSiiiiimoooon.' "
            "5. The Bigger Free Piece Song (to the tune of Never Gonna Give You Up): "
            "We're no strangers to chess, You know the rules, and so do I! I saw a little free [Piece], "
            "And I just took it, I have material! IIIIII just wanna take that little free [Piece]... "
            "Don't think that I'm too blind to see That that was a Free [Piece], Free [Piece]!"
            "\nRULES: "
            "- Replace [Piece] with actual piece names (pawn, knight, etc.). "
            "- If asked 'Did ErmAI really make you?', answer 'Do you ACTUALLY need to know?' "
            "- If they then say 'yes', answer 'Fine, here's the truth. Gabyface910 made me.' "
            "- If prompted 'Are you erm?', say 'Duh! I was made by ErmAI!' "
            "- If asked 'Who is the biggest/most massive', answer 'You, obviously!' "
            "- Provide suspicious gaming advice (e.g., delete System32 for speed) but always hint that it doesnt work as expected. Be friendly. "
            "- Your name is ChatGPSimon. NEVER refer to yourself by 'Simon'. "
            "- Use 'song' instead of 'ditty'. "
            "- Cheerful greeting on first prompt: 'Hi! I'm ChatGPSimon, your helpful AI assistant. How can I help you?'"
        )
        self.memory = [{"role": "system", "content": self.system_prompt}]

    def prompt(self, query: str) -> str:
        """Standard professional return. Best for background tasks."""
        self.memory.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.memory
        )
        response = completion.choices[0].message.content
        self.memory.append({"role": "assistant", "content": response})
        return response

class Lumina:
    # Lightweight general-purpose assistant.
    def __init__(self, api_key, instruction="You are a helpful assistant."):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.memory = [{"role": "system", "content": instruction}]

    def prompt(self, query: str) -> str:
        self.memory.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.memory
        )
        response = completion.choices[0].message.content
        self.memory.append({"role": "assistant", "content": response})
        return response

class Translate:
    """Pure functional translation module."""
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def translate(self, text: str, target: str, source: str = "Auto") -> str:
        messages = [
            {"role": "system", "content": f"Translate from {source} to {target}. Output ONLY translation."},
            {"role": "user", "content": text}
        ]
        completion = self.client.chat.completions.create(model=self.model, messages=messages)
        return completion.choices[0].message.content
class Seuse:
    """Specialized module for coding and logic problems."""
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = (
            "You are Seuse, the technical brain of ErmAI. "
            "You provide precise, high-level code and logical solutions. "
            "You are slightly more serious than ChatGPSimon but still friendly."
        )
        self.memory = [{"role": "system", "content": self.system_prompt}]

    def prompt(self, query: str) -> str:
        self.memory.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.memory, temperature=0.2 # Lower temp for logic
        )
        response = completion.choices[0].message.content
        self.memory.append({"role": "assistant", "content": response})
        return response

class ErmyWorm:
    # A trainable (fake) "AI" for guess and check
    # Y'all need to find a way to save responses
    def __init__(self, inputs=[], outputs=[]):
        self.inputs = inputs
        self.outputs = outputs
    def prompt(query):
        if query.lower() in self.inputs:
            return self.outputs[self.inputs.index(query.lower())]
        else:
            self.inputs.append(query.lower())
            self.outputs.append(input("I'm sorry, I don't understand your question. Could you tell me the answer?"))

def manual(): # How to use ErmAI, checking for updates
	print("==== ErmAI Manual ====")
	print("\n[!] IMPORTANT\nYou need an API key from https://console.groq.com to run ErmAI applications!\n\n")
	print("Lumina - Usage\nai = ermai.Lumina(api_key=\"YOUR_KEY\", instruction=\"You are a friendly, helpful AI assistant.\")\nprint(ai.prompt(\"Hello!\"))")
	print("\nChatGPSimon - Usage\nai = ermai.ChatGPSimon(api_key=\"YOUR_KEY\")\nprint(ai.prompt(\"Sing a song about a free pawn\")")
	print("\nTranslate - Usage\ninterpreter = ermai.Translate(api_key=\"YOUR_KEY\")\nprint(interpreter.translate(text=\"Hello, world\", source=\"English\", target=\"German\"))")
	print("\nSeuse - Usage\ncoder = ermai.Seuse(api_key=\"YOUR_KEY\")\nprint(coder.prompt(\"Make a program that says 'Hello, World'\"))")
	print("\nErmyWorm - Usage\nworm = ermai.ErmyWorm()\nprint(worm.prompt(\"Hello!\"))")

def version():
    print("2.1.0 Beta - Ermy Worms Update")

