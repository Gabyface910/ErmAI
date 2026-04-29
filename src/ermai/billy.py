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
        """The core brain of Billy (SDK V2 Compliant)."""
        history = self._load_memory()
        
        # SDK FIX: 'content' must be 'parts' and it must be a list of dicts/strings
        history.append({"role": "user", "parts": [{"text": user_input}]})
        
        print(f"Billy is thinking...")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are ErmAI Billy, a friendly coding buddy. "
                        "Be a helpful peer."
                    ),
                    temperature=0.1,
                ),
                contents=history
            )
            
            billy_res = response.text
            
            # SDK FIX: Store Billy's response in the same format
            history.append({"role": "model", "parts": [{"text": billy_res}]})
            self._save_memory(history)
            
            time.sleep(6)
            return billy_res

        except Exception as e:
            # If things still fail, let's see exactly what Billy is sending
            return f"Billy: Oof, something went 'sus'. Error: {str(e)}"
