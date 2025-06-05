# mock_server.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Crie um diretório para armazenar os áudios recebidos
os.makedirs("received_audios", exist_ok=True)

@app.route("/alert", methods=["POST"])
def receive_alert():
    """
    Espera receber um multipart/form-data com um campo 'audio' (arquivo)
    e, opcionalmente, outros campos JSON (por ex. timestamp, sensor_id, etc).
    """
    # 1) Ler dados extras (campo JSON ou form)
    sensor_id = request.form.get("sensor_id", "desconhecido")
    timestamp = request.form.get("timestamp", "sem_timestamp")

    # 2) Receber o arquivo de áudio
    audio_file = request.files.get("audio")
    if audio_file:
        # Salvar em disco com nome baseado em sensor_id + timestamp
        filename = f"{sensor_id}_{timestamp}_{audio_file.filename}"
        save_path = os.path.join("received_audios", filename)
        audio_file.save(save_path)
        print(f"[{sensor_id}] Áudio salvo em: {save_path}")
    else:
        print(f"[{sensor_id}] Nenhum arquivo de áudio enviado.")

    # 3) Exibir um log simples
    print(f"[{sensor_id}] Alerta recebido em {timestamp}")
    return jsonify({"status": "ok", "sensor_id": sensor_id}), 200

if __name__ == "__main__":
    """
    Para rodar múltiplos servidores fictícios, basta executar este script
    em terminais diferentes, alterando a porta:
        python mock_server.py 5001
        python mock_server.py 5002
    Ou então, parametrizar via argumento.
    """
    import sys

    port = 5001
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
        except:
            pass

    app.run(host="0.0.0.0", port=port)
