import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAIgjD6C2mk652AiT8XjhFhuxzH3uFk9bA"
genai.configure(api_key=GOOGLE_API_KEY)

print("\n")

for embed in genai.list_models():
    if "embedContent" in embed.supported_generation_methods:
        print("\t\033[1;32m", embed.name, "\033[m")

print("\n")