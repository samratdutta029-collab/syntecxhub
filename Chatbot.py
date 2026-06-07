import re
import json
import random
from datetime import datetime
from pathlib import Path


class RuleBasedChatbot:
    def __init__(self, name="Sage", log_file="conversation_log.json"):
        self.name = name
        self.log_file = Path(log_file)
        self.history = []
        self.intents = self._build_intents()
        self.knowledge_base = self._build_knowledge_base()

    def _build_intents(self):
        """Define intents as (regex pattern, list of possible responses)."""
        return {
            "greeting": {
                "patterns": [
                    r"\b(hi|hello|hey|hola|greetings|good\s*(morning|afternoon|evening))\b"
                ],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What's on your mind?",
                    "Hey! Ask me anything.",
                ],
            },
            "farewell": {
                "patterns": [r"\b(bye|goodbye|see\s*you|cya|later|quit|exit)\b"],
                "responses": [
                    "Goodbye! Have a great day.",
                    "See you later!",
                    "Take care!",
                ],
            },
            "thanks": {
                "patterns": [r"\b(thanks|thank\s*you|thx|appreciate)\b"],
                "responses": ["You're welcome!", "Happy to help.", "Anytime!"],
            },
            "help": {
                "patterns": [r"\b(help|what\s*can\s*you\s*do|commands|options)\b"],
                "responses": [
                    "I can chat, answer questions about Python, "
                    "tell you the time, or just make small talk. "
                    "Try asking: 'What is Python?' or 'Tell me a joke.'"
                ],
            },
            "name": {
                "patterns": [r"\b(your\s*name|who\s*are\s*you|what\s*are\s*you)\b"],
                "responses": [f"I'm {self.name}, a simple rule-based chatbot."],
            },
            "time": {
                "patterns": [r"\b(time|what\s*time|current\s*time)\b"],
                "responses": [lambda: f"It's {datetime.now().strftime('%H:%M:%S')}."],
            },
            "date": {
                "patterns": [r"\b(date|today|what\s*day)\b"],
                "responses": [lambda: f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."],
            },
            "mood": {
                "patterns": [r"\b(how\s*are\s*you|how\s*do\s*you\s*feel|you\s*ok)\b"],
                "responses": [
                    "I'm just code, but I'm running smoothly!",
                    "All systems go. How about you?",
                ],
            },
            "joke": {
                "patterns": [r"\b(joke|funny|make\s*me\s*laugh)\b"],
                "responses": [
                    "Why do programmers prefer dark mode? Because light attracts bugs.",
                    "There are 10 types of people: those who understand binary and those who don't.",
                ],
            },
        }

    def _build_knowledge_base(self):
        """Domain Q&A — keys are keyword sets, values are answers."""
        return [
            {
                "keywords": {"python"},
                "answer": "Python is a high-level, interpreted programming "
                          "language known for its readable syntax and large ecosystem.",
            },
            {
                "keywords": {"machine", "learning"},
                "answer": "Machine learning is a branch of AI where systems learn "
                          "patterns from data rather than following explicit rules.",
            },
            {
                "keywords": {"chatbot"},
                "answer": "A chatbot is a program that simulates conversation. "
                          "Rule-based bots use patterns; modern ones use neural networks.",
            },
            {
                "keywords": {"regex", "regular", "expression"},
                "answer": "Regular expressions are patterns used to match character "
                          "combinations in strings — great for input parsing.",
            },
            {
                "keywords": {"ai", "artificial", "intelligence"},
                "answer": "Artificial Intelligence is the field of building systems "
                          "that perform tasks requiring human-like reasoning.",
            },
        ]

    def detect_intent(self, message):
        """Return the first matching intent name, or None."""
        msg = message.lower()
        for intent, data in self.intents.items():
            for pattern in data["patterns"]:
                if re.search(pattern, msg):
                    return intent
        return None

    def query_knowledge_base(self, message):
        """Look for keyword matches in the KB and return the best answer."""
        msg_words = set(re.findall(r"\w+", message.lower()))
        best_match, best_score = None, 0
        for entry in self.knowledge_base:
            score = len(entry["keywords"] & msg_words)
            if score > best_score:
                best_match, best_score = entry, score
        return best_match["answer"] if best_match else None

    def respond(self, message):
        """Generate a response: intent → knowledge base → fallback."""
        intent = self.detect_intent(message)
        if intent:
            response = random.choice(self.intents[intent]["responses"])
            return response() if callable(response) else response

        kb_answer = self.query_knowledge_base(message)
        if kb_answer:
            return kb_answer

        return "I'm not sure I understand. Try asking for 'help' to see what I can do."

    def log(self, user_msg, bot_msg):
        """Append the exchange to history and persist to disk."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_msg,
            "bot": bot_msg,
        }
        self.history.append(entry)
        with self.log_file.open("w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def chat(self):
        """Interactive console loop."""
        print(f"{self.name}: Hi! I'm {self.name}. Type 'bye' to exit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.name}: Goodbye!")
                break

            if not user_input:
                continue

            reply = self.respond(user_input)
            print(f"{self.name}: {reply}\n")
            self.log(user_input, reply)

            if self.detect_intent(user_input) == "farewell":
                break


if __name__ == "__main__":
    bot = RuleBasedChatbot()
    bot.chat()
