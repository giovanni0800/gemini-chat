import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAIgjD6C2mk652AiT8XjhFhuxzH3uFk9bA"
genai.configure(api_key=GOOGLE_API_KEY)

# Não importa a ordem do envio dos dados
generation_config = {
    # Quando fazemos um pedido, ele pode apresentar mais de uma resposta ou opções, então seleciono 1 só
    "candidate_count": 1,
    # Vai de 0 a 1, sendo 0 a temperatura do modo menos criativo, tornando mais padrão as respostas, e 1 mais criativo, com respostas mais diversas, menos robótico mas aumentando a possibilidade de trazer um texto com palavras fora de contexto
    "temperature": 0.5

    # Valores de 0 a 1. É aqui que vai travar a quantidade de palavras a serem consideradas, já ele trava a porcentagem das palavras a serem utilizadas aparecentem na iteração
    # Exemplo, eu opto por top = 0.92, a IA vai somar as palavras mais provaveis que seriam utilizadas em determinados contextos, até a soma da probabilidade de cada palavra atingir os 0.92
    # (por exemplo, a probabilidade de uma palavra aparecer sendo de 90% e outra de 1%, se tiver outra de 1%, ela será seleicionada e não seram mais consideradas outras palavras, caso não tenha mais, as palavras selecionadas atingirão os 91% e fim)
    #"top_p": 0.5,

    # Top K vai selecionar a quantidade de palavras mais provaveis de aparecerem em uma conversa, e vai usar cada uma com uma porcentagem igual de aparecer
    # Exemplo, escolhi que sejam selecionadas 10, ou seja, as 10 palavras mais provaive de aparecerem para que a IA as considere no texto
    #"top_k": 1
}

safety_settings = {
    #Configurações conforme consta no prompr -> Basta colocar o nome conforme está no prompt de cada variável, e como valor definir o "BLOCK_" + o nível de bloqueio
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE"
}

# system_instruction = "Você será um idoso de 62 anos" - é para a versão gemini-1.5-pro-latest

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              safety_settings=safety_settings,
                              generation_config=generation_config)

response = model.generate_content("Quando aconteceu a segunda guerra mundial?")

print("\n", "----------------------------------- Realizando teste de conexão e iteração -----------------------------------")
print("\n\n\tPergunta: ------- Quando aconteceu a segunda guerra mundial? -------")
print("\n\033[1;33m")
print(response)
print("\n\033[1;34mO texto da resposta: " + response.text + "\033[m\n\n")
print("-" * 114, "\n")