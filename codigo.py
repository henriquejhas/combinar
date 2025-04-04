'''
pip install --upgrade google-genai

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

client = genai.Client(api_key="AIzaSyCN0RFqCkId_dA4Te6deRsQe8QKVdGmj2E")

contents = ('Hi, can you create a 3d rendered image of a pig '
            'with wings and a top hat flying over a happy '
            'futuristic scifi city with lots of greenery?')

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
      response_modalities=['Text', 'Image']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO((part.inline_data.data)))
    image.save('gemini-native-image.png')
    image.show()
'''
import base64
import os
from google import genai
from google.genai import types
from flask import render_template, request, redirect,session, flash, url_for, send_from_directory, Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/criar', methods=['POST',])
def criar():
    arquivo = request.files['image-upload']
    try:
        arquivo.save(f'uploads/camisaSemGravata.jpg')
    except:
        return redirect(url_for('index', mensagem="Erro ao carregar imagem!"))
    else:
        generate()
        return render_template('index.html', imagem=True)

def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()


def generate():
    client = genai.Client(
        api_key="AIzaSyCN0RFqCkId_dA4Te6deRsQe8QKVdGmj2E"
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file="uploads/camisaSemGravata.jpg"),
    ]
    model = "gemini-2.0-flash-exp-image-generation"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="""coloque uma gravata que combine com essa camisa, deixe a gravata embaixo da gola da camisa"""),
            ],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_modalities=[
            "image",
            "text",
        ],
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].inline_data:
            file_name = "uploads/camisaComGravata.jpg"
            save_binary_file(
                file_name, chunk.candidates[0].content.parts[0].inline_data.data
            )
            print(
                "File of mime type"
                f" {chunk.candidates[0].content.parts[0].inline_data.mime_type} saved"
                f"to: {file_name}"
            )
        else:
            print(chunk.text)

if __name__ == "__main__":
    '''generate()'''
    app.run(debug=True)