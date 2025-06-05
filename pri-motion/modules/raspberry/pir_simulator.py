# pir_simulator.py
import time
import random
import requests
import os
from datetime import datetime
import threading

# Se quiser tocar áudio localmente
try:
    import pygame
    pygame.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Configurações
SENSOR_ID = "PIR_SIM_01"
SERVER_URLS = [
    "http://localhost:5001/alert",
    "http://localhost:5002/alert"
]

# Construindo o caminho absoluto para o MP3 (se o script estiver em modules/raspberry)
script_dir   = os.path.dirname(__file__)                                 # .../pri-motion/modules/raspberry
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))     # .../pri-motion
AUDIO_PATH   = os.path.join(project_root, "assets", "optimus.mp3")

if not os.path.isfile(AUDIO_PATH):
    raise FileNotFoundError(f"[AUTOBOT COMMS] Erro: áudio não encontrado em: {AUDIO_PATH}")

def play_audio(path):
    """
    Toca áudio em background, se o pygame estiver disponível.
    """
    if not PYGAME_AVAILABLE:
        print("[AUTOBOT COMMS] pygame não instalado; ignorando reprodução local de áudio.")
        return

    try:
        # Se já está tocando algo, não interrompe
        if pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        # O pygame lida internamente em outra thread, então não bloqueamos aqui.
    except Exception as e:
        print(f"[AUTOBOT COMMS] Erro ao tentar tocar áudio: {e}")

def send_alert():
    """
    Carrega o arquivo de áudio e envia para todos os SERVER_URLS.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files = {
        "audio": (os.path.basename(AUDIO_PATH), open(AUDIO_PATH, "rb"), "audio/mpeg")
    }
    data = {
        "sensor_id": SENSOR_ID,
        "timestamp": timestamp
    }

    # Mensagem de saída temática antes de enviar
    print(f"[AUTOBOT COMMS] Unidade de vigilância {SENSOR_ID} detectou atividade inimiga.")
    print(f"[AUTOBOT COMMS] Preparando transmissão de áudio de Optimus Prime (t= {timestamp}).\n")

    for url in SERVER_URLS:
        try:
            response = requests.post(url, data=data, files=files, timeout=5)
            if response.status_code == 200:
                print(f"[AUTOBOT COMMS] Transmissão bem-sucedida para {url} — Recebido e replicado.")
            else:
                print(f"[AUTOBOT COMMS] Falha na transmissão para {url} (código {response.status_code}) — Solicitar retransmissão.")
        except Exception as e:
            print(f"[AUTOBOT COMMS] Erro ao alcançar {url}: {e} — Retentativa agendada em breve.")

    # Tocar o áudio **apenas** se não estiver já tocando
    if PYGAME_AVAILABLE:
        if not pygame.mixer.music.get_busy():
            # Em thread separada, para não bloquear o envio HTTP
            threading.Thread(target=play_audio, args=(AUDIO_PATH,), daemon=True).start()
            print(f"[AUTOBOT COMMS] Iniciando reprodução da mensagem de Optimus Prime...\n")
        else:
            print("[AUTOBOT COMMS] Protocolo de transmissão ativo — áudio ainda em execução. Nova mensagem adiada.\n")

def simulate_pir_loop():
    """
    Loop infinito que, em intervalos aleatórios, dispara o send_alert(),
    mas só se não houver áudio tocando no momento.
    """
    print("[AUTOBOT COMMS] Iniciando patrulha de vigilância PIR. Sistema de escaneamento ativo.")
    try:
        while True:
            # Aguarda de 5 a 15 segundos antes de “detectar movimento”
            wait_time = random.uniform(5.0, 15.0)
            time.sleep(wait_time)

            # Hora atual (para exibir no log)
            hora = datetime.now().strftime('%H:%M:%S')

            # Se pygame disponível e áudio tocando, mostra mensagem temática e pula
            if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
                print(f"[{hora}] [AUTOBOT COMMS] {SENSOR_ID}: "
                      "Detecção secundária ignorada. Transmissão corrente em execução.")
                continue

            # Caso não esteja tocando, dispara o alerta + reprodução
            print(f"[{hora}] [AUTOBOT COMMS] {SENSOR_ID}: Movimento detectado! Iniciando procedimento de transmissão...")
            send_alert()

    except KeyboardInterrupt:
        print("\n[AUTOBOT COMMS] Simulação interrompida pelo usuário. Lembre-se: a batalha continua!")

if __name__ == "__main__":
    simulate_pir_loop()
