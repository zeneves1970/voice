from flask import Flask, request, jsonify
import openai
import os
from flask import render_template

# Configurar chave de API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Certifique-se de que a pasta 'uploads' existe para salvar arquivos temporários
os.makedirs('uploads', exist_ok=True)

@app.route('/convert-audio', methods=['POST'])
def convert_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum ficheiro de áudio foi enviado.'}), 400

    # Salvar o áudio enviado pelo cliente
    audio_file = request.files['audio']
    audio_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(audio_path)

    try:
        # Usar seu código para converter o áudio em texto
        with open(audio_path, "rb") as file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=file,
                response_format="text"
            )
        
        return jsonify({'text': transcription})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    @app.route('/')
def index():
    return render_template('index.html')
