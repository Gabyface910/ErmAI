import requests
import io
import random
import os
from datetime import datetime
from groq import Groq
from PIL import Image

class ChatGPSimon:
    """The flagship ErmAI Persona with custom branding and memory."""
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

    def ask(self, query: str) -> str:
        """Standard professional return. Best for background tasks."""
        self.memory.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.memory
        )
        response = completion.choices[0].message.content
        self.memory.append({"role": "assistant", "content": response})
        return response

    def ask_stream(self, query: str):
        """Generator for UI streaming. Saves to memory automatically upon completion."""
        self.memory.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model=self.model, messages=self.memory, stream=True
        )
        full_res = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                full_res += content
                yield content
        self.memory.append({"role": "assistant", "content": full_res})

class AI4:
    """Lightweight general-purpose assistant (optimized for Pi performance)."""
    def __init__(self, api_key, system_prompt="You are a helpful assistant."):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.memory = [{"role": "system", "content": system_prompt}]

    def chat(self, query: str) -> str:
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
        self.model = "llama-3.3-70b-versatile"

    def translate(self, text: str, target_lang: str, source_lang: str = "Auto") -> str:
        messages = [
            {"role": "system", "content": f"Translate from {source_lang} to {target_lang}. Output ONLY translation."},
            {"role": "user", "content": text}
        ]
        completion = self.client.chat.completions.create(model=self.model, messages=messages)
        return completion.choices[0].message.content

class Imagine:
    """Visual generation module using a 'Director' prompt expansion."""
    def __init__(self, groq_key, hf_token):
        self.client = Groq(api_key=groq_key)
        self.hf_token = hf_token
        self.api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.director_prompt = "Professional prompt engineer. Describe chess pieces geometrically. 8k, studio lighting. Output ONLY prompt."

    def generate(self, text: str, seed: int = None) -> Image.Image:
        # 1. Expand prompt via Groq
        chat = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": self.director_prompt}, {"role": "user", "content": text}]
        )
        refined = chat.choices[0].message.content
        
        # 2. Call HF Inference
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": refined, "parameters": {"seed": seed or random.randint(0, 99999)}}
        res = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        
        if res.status_code == 200:
            return Image.open(io.BytesIO(res.content))
        raise Exception(f"HF Error {res.status_code}: {res.text}")

def manual():
	print("==== ErmAI Manual ====")
	print("AI4 - Usage\nai = ermai.AI4(api_key)\nprint(ai.chat(\"Hello!\"))")
	print("\nChatGPSimon - Usage\nai = ermai.ChatGPSimon(api_key)\nprint(ai.ask(\"Sing a song about a free pawn\")")
	print("\nTranslate - Usage\ninterpreter = ermai.Translate(api_key)\nprint(interppreter.translate(text=\"Hello, world\", source_lang=\"English\", target_lang=\"German\"))")

