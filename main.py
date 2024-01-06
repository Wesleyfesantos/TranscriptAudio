import whisper
import telebot
import requests

CHAVE_API = "########" #Coloque a sua chave de API aqui

bot = telebot.TeleBot(CHAVE_API)
modelo = whisper.load_model("small") #na documentação do Whisper tem as velocidades que você pode configurar de acordo com seu computador.


@bot.message_handler(content_types=['voice', 'audio']) #Configura a aplicação para atuar somente se receber audio ou mensagem de voz
def handle_audio(message):
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # URL completa do arquivo
    file_url = f"https://api.telegram.org/file/bot{CHAVE_API}/{file_path}"

    # Baixar o arquivo de áudio
    arquivo = requests.get(file_url, allow_redirects=True)
    if arquivo.status_code == 200:
        with open("audio_recebido.ogg", 'wb') as f:
            f.write(arquivo.content)

        resposta = modelo.transcribe("audio_recebido.ogg", fp16=False) #você pede que a biblioteca whisper transcreva o audio
        transcricao = resposta['text'] if 'text' in resposta else 'Não foi possível transcrever o áudio.'

        bot.send_message(message.chat.id, f"{transcricao}") #bot responde a trasncrição
    else:
        bot.reply_to(message, "Ocorreu um erro ao baixar o áudio recebido.")

@bot.message_handler(func=lambda message: True) #uma resposta automática caso não recebe audio
def handle_other_messages(message):
    bot.reply_to(message, "Por favor, envie apenas mensagem de áudio.")

bot.polling()