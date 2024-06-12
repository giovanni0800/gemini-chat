import flet as ft
import os
import pandas as pd
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAIgjD6C2mk652AiT8XjhFhuxzH3uFk9bA"
genai.configure(api_key=GOOGLE_API_KEY)

tem_arquivos = False
arquivo_imagens = []
arquivo_trabalho = []
tamanho_minimo = 1024  # 1 KB
way = []

def main(page: ft.Page):
    page.title = "Chat com Gemini"

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.TRANSPARENT,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT
            },
            track_visibility=True,
            track_border_color=ft.colors.TRANSPARENT,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.CYAN_500,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT
            },
            thickness=14,
            radius=15,
            main_axis_margin=7,
            cross_axis_margin=14
        )
    )

    generation_config = {
                    "candidate_count": 1,
                    "temperature": 0.7
                }

    safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

    system_instruction = "Você é um rapaz preciso, muito bom em matemática, inteligente e respeitoso"

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                system_instruction=system_instruction,
                                safety_settings=safety_settings)
    gemini_historico = []

    HEIGHT = 400
    
    titulo = ft.Text( "Chat Com Gemini", color=ft.colors.SURFACE_VARIANT, size=56, text_align="center" )
    # Acompanhar o Chat para ajustar o controls (elementos que irão aparecer)
    chat = ft.Column(auto_scroll=True, spacing=7,
                     controls=[], scroll=ft.ScrollMode.ALWAYS,
                     height=HEIGHT, width=float("inf")) # Usar o float("inf") no width indica que quero que tome toda a largura da tela
    
    

    def enviar_mensagem_via_tunel(mensagem):
        chat.controls.append( mensagem )
        page.update()

    page.pubsub.subscribe( enviar_mensagem_via_tunel )

    upload = ft.ElevatedButton( "Subir Arquivo", on_click=lambda evento: seletor_arquivos.pick_files(), color=ft.colors.BLUE_900 )
    def salvar_upload(evento: ft.FilePickerResultEvent):
        for x in evento.files:
            global way
            way = os.path.join( os.getcwd(), "Files" , x.name )
            print(way)
            
            if( (".xlsx" in x.name) or (".xls" in x.name) ):
                import openpyxl
                # Abra o arquivo XLSX
                workbook = openpyxl.load_workbook(way)

                # Obtenha a primeira planilha (você pode substituir pelo nome da planilha desejada)
                sheet = workbook.active

                # Itere sobre as linhas da planilha
                for linha in sheet.iter_rows(values_only=True):
                    # Imprima cada linha
                    print(linha)

            global tem_arquivos
            tem_arquivos = True
            
            upload.color = ft.colors.YELLOW_900
            page.update()

    seletor_arquivos = ft.FilePicker(
        on_result=salvar_upload
    )

    def enviar_mensagem(evento):
        if(campo_nome.value != "" and campo_mensagem.value != ""):
            nova_mensagem = campo_mensagem.value
            usuario_que_digitou = campo_nome.value
            
            if "gemini:" in str(nova_mensagem).lower():
                
                talk = model.start_chat(history=gemini_historico)

                global tem_arquivos
                if (tem_arquivos is True):

                    global way
                    if (".csv" in way):
                        # Crie um objeto leitor CSV
                        tabelas = pd.read_csv(way)

                        print( tabelas )
                        talk.send_message( genai.upload_file( way, mime_type="text/csv" ) )

                    else:
                        global arquivo_imagens
                        arquivo_imagens = way
                        talk.send_message( genai.upload_file( arquivo_imagens, mime_type="image/png" ) )

                talk.send_message( nova_mensagem.replace("gemini:", "") )

                response = talk.last.text
                page.pubsub.send_all( ft.Text( f"{usuario_que_digitou}: { nova_mensagem.replace("gemini:", "") }" ) )
                page.pubsub.send_all( ft.Text( f"\n* Gemini *: {response}\n", color=ft.colors.GREEN_ACCENT_700 ) )

                gemini_historico.append( {
                    "role": "user",
                    "parts": [nova_mensagem]
                } )

                gemini_historico.append({
                    "role": "model",
                    "parts": [response]
                })

                upload.color = ft.colors.BLUE_900

            else:
                page.pubsub.send_all( ft.Text( f"{usuario_que_digitou}: {nova_mensagem}" ) )
                upload.color = ft.colors.BLUE_900
            
            way = ""
            tem_arquivos = False
            campo_mensagem.value = ""
            page.update()

    campo_mensagem = ft.TextField(label="Digite sua mensagem", width=1000, on_submit=enviar_mensagem)
    botao_enviar_conversa = ft.ElevatedButton("Enviar", width=121, on_click=enviar_mensagem)
    linha_mensagem = ft.Row([campo_mensagem, botao_enviar_conversa, upload], alignment='center')

    def acessar_chat(evento):
        if (campo_nome.value != ""):

            from datetime import datetime

            page.remove(container_pagina_inicial)      
            janela.open = False

            page.add( ft.Container( chat, margin=50 ) )
            page.add(linha_mensagem)
            page.pubsub.send_all( ft.Text( f"Usuário -> {campo_nome.value} entrou no chat às -> {datetime.now().strftime("%H:%M:%S - %d/%m/%Y") }", color=ft.colors.DEEP_PURPLE_800 ) )
            page.update()

    titulo_janela = ft.Text("Bem Vindo ao Chat With Bot!")
    campo_nome = ft.TextField(label="Digite seu nome", on_submit=acessar_chat)
    botao_entrar = ft.ElevatedButton("Entrar", on_click=acessar_chat)
    janela = ft.AlertDialog(title=titulo_janela, content=campo_nome, actions=[botao_entrar])

    def iniciar_chat(evento):
        page.dialog = janela
        janela.open = True
        page.update()

    # Criar o Elemento de Botão principal
    botao_principal = ft.ElevatedButton( "Iniciar Chat", width=449, height=121, icon="login", on_click=iniciar_chat)

    container_pagina_inicial = ft.Container( margin=121,
                    content=(ft.Row(
                        controls=[ft.Column(
                            controls=[ titulo, botao_principal ],
                            alignment="center",
                            height="100vh"
                        )],
                        alignment="center"
                    ))
                )
    
    page.overlay.append(seletor_arquivos)
    page.add( container_pagina_inicial )

print("\n\033[1;32m", ( "-" * 120 ) )
print("\t\t\t\tAplicação conectada com sucesso!")
print( ( "-" * 120 ), "\033[m\n" )

ft.app( target=main, view=ft.WEB_BROWSER, upload_dir="Files" )

print("\n", ( "-" * 120 ) )
print("\t\t\t\tAplicação desconectada com sucesso!")
print( ( "-" * 120 ), "\n" )