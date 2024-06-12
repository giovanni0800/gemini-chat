"""
    Este script servirá para listar os models da gemini ai que realizam a criação de conteúdos,
    ou seja, onde eu consigo criar uma interação entre o meu código e a IA
"""

import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAIgjD6C2mk652AiT8XjhFhuxzH3uFk9bA"
genai.configure(api_key=GOOGLE_API_KEY)

print("\n\033[1;33mVersões do Gemini AI que estão disponíveis para interação e uso da geração de conteúdo:\033[m\n")

# Aqui eu consigo trabalhar com a geração de conteudos com essas versões apresentadas pelo Gemini AI
for generators_model in genai.list_models():
    if "generateContent" in  generators_model.supported_generation_methods:
        print("\t\033[1;32m" + generators_model.name + "\033[m")

print("\n")

"""
Diferença entre gemini Pro e Pro Vision:
    - Pro > Posso fazer solicitações (enviar prompt) somente de texto;
    - Pro Vision > Posso enviar uma imagem, um texto (conteúdos multimídia) tudo junto em uma única requisição.
"""