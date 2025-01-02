from flask import Flask, request, jsonify, render_template
import openai
import os

# Configurar chave de API da OpenAI a partir das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Certifique-se de que a pasta 'uploads' existe para salvar arquivos temporários
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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
        
        # Em vez de diretamente usar `transcription`, acesse o campo de texto se for necessário
transcription_text = transcription.get("text", "")  # Ajuste conforme a estrutura da resposta
print(f"Texto transcrito: {transcription_text}")


        return jsonify({'text': transcription})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obter a porta do ambiente ou usar 5000 como padrão
    app.run(host='0.0.0.0', port=port, debug=True)

