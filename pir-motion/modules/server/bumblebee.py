# pir-motion/modules/server/mock_server.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
os.makedirs("received_audios", exist_ok=True)

@app.route("/alert", methods=["POST"])
def receive_alert():
    """
    Autobot Bumblebee (U1) recebendo a mensagem de Optimus Prime.
    """
    sensor_id = request.form.get("sensor_id", "UNKNOWN_UNIT")
    timestamp = request.form.get("timestamp", "UNKNOWN_TIME")

    audio_file = request.files.get("audio")
    if audio_file:
        filename = f"{sensor_id}_{timestamp}_{audio_file.filename}"
        save_path = os.path.join("received_audios", filename)
        audio_file.save(save_path)
        # Mensagem temática do Bumblebee
        print(f"[BUMBLEBEE – U1] Recebido áudio de {sensor_id} às {timestamp}. Salvando em {save_path}", flush=True)
        print("[BUMBLEBEE – U1] Confirmado: transmissão de Optimus Prime armazenada com sucesso.\n", flush=True)
    else:
        print(f"[BUMBLEBEE – U1] ALERTA: Nenhum arquivo de áudio encontrado no alerta de {sensor_id}!", flush=True)

    # Pedido de confirmação de status
    print(f"[BUMBLEBEE – U1] Status: Pronto para retransmissão de dado para a matriz Autobot.\n", flush=True)
    return jsonify({"status": "received", "unit": "Bumblebee"}), 200

if __name__ == "__main__":
    import sys
    port = 5001
    unit_id = 1
    if len(sys.argv) >= 2:
        try:
            port    = int(sys.argv[1])
            unit_id = int(sys.argv[2])
        except:
            pass
    app.config['UNIT_ID'] = unit_id
    app.run(host="0.0.0.0", port=port)
