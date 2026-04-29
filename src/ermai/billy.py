import os
import json
import time
from google import genai
from google.genai import types

class Billy:
    def __init__(self, api_key, model_id="gemma-4-31b-it", memory_file="billy_chat.json"):
        # Core configuration
        self.api_key = api_key
        self.model_id = model_id
        self.memory_file = memory_file
        self.max_memory = 20
        
        # Initialize the Supreme Client
        self.client = genai.Client(api_key=self.api_key)
        
        # Friendly greeting for the console
        self._print_banner()

    def _print_banner(self):
        print("ErmAI Billy initialized. Sus but Supreme.")

    def _load_memory(self):
        """Loads chat history from disk to save RAM."""
        if not os.path.exists(self.memory_file):
            return []
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_memory(self, history):
        """Saves chat history to disk and crops it to stay efficient."""
        if len(history) > self.max_memory:
            history = history[-self.max_memory:]
        
        with open(self.memory_file, "w") as f:
            json.dump(history, f)

    def code(self, user_input):
        """The core brain of Billy."""
        history = self._load_memory()
        
        # Add the user's new message to the local history
        history.append({"role": "user", "content": user_input})
        
        print(f"Billy is thinking... (Gemma 4 @ 10 RPM)")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are ErmAI Billy, a friendly, ultra-efficient coding buddy. "
                        "Slogan: 'Sus but Supreme.' You live on a Raspberry Pi 3B+. "
                        "Keep answers concise. Use local tools. Be a helpful peer."
                    ),
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(include_thoughts=False)
                ),
                contents=history
            )
            
            billy_res = response.text
            
            # Update history
            history.append({"role": "model", "content": billy_res})
            self._save_memory(history)
            
            # Respect the 10 RPM free tier limit
            time.sleep(6)
            
            return billy_res

        except Exception as e:
            return f"Billy: Oof, something went 'sus'. Error: {str(e)}"

