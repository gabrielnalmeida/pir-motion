# pir-motion/modules/server/mock_server1.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
os.makedirs("received_audios", exist_ok=True)

@app.route("/alert", methods=["POST"])
def receive_alert():
    """
    Autobot Ironhide (U2) recebendo a mensagem de Optimus Prime.
    """
    sensor_id = request.form.get("sensor_id", "UNKNOWN_UNIT")
    timestamp = request.form.get("timestamp", "UNKNOWN_TIME")

    audio_file = request.files.get("audio")
    if audio_file:
        filename = f"{sensor_id}_{timestamp}_{audio_file.filename}"
        save_path = os.path.join("received_audios", filename)
        audio_file.save(save_path)
        # Mensagem temática do Ironhide
        print(f"[IRONHIDE – U2] Sinal de {sensor_id} detectado às {timestamp}. Processando arquivo em {save_path}", flush=True)
        print("[IRONHIDE – U2] Confirmado: áudio integridade verificada. Preparando resposta.\n", flush=True)
    else:
        print(f"[IRONHIDE – U2] ALERTA: Payload ausente no pacote de {sensor_id}! Conferir link de comunicação.", flush=True)

    # Instrução de protocolo de defesa
    print(f"[IRONHIDE – U2] Status: Mantendo posição de guarda até novas ordens.\n", flush=True)
    return jsonify({"status": "received", "unit": "Ironhide"}), 200

if __name__ == "__main__":
    import sys
    port = 5002
    unit_id = 2
    if len(sys.argv) >= 2:
        try:
            port    = int(sys.argv[1])
            unit_id = int(sys.argv[2])
        except:
            pass
    app.config['UNIT_ID'] = unit_id
    app.run(host="0.0.0.0", port=port)
