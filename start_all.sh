#!/usr/bin/env bash

# =============================================================================
#    Script de inicialização “Operação Autobot Online”
#    Agora o start_all.sh está **fora** da pasta pir-motion/, na raiz do workspace.
#    Ele irá:
#      1) subir mock_server.py  (Unidade Autobot U1, porta 5001)
#      2) subir mock_server1.py (Unidade Autobot U2, porta 5002)
#      3) subir pir_simulator.py (Sensor PIR_SIM_01)
#    As saídas serão redirecionadas para logs na raiz.
# =============================================================================

# ---------------------------------------------------
# 1) checa se o python3 está disponível
# ---------------------------------------------------
command -v python3 >/dev/null 2>&1 || {
    echo "[STARTUP] Erro: python3 não encontrado no PATH."
    echo "[STARTUP] Instale o Python 3.x antes de prosseguir."
    exit 1
}

echo -e "\n[STARTUP] Iniciando componentes da FROTA AUTOBOT...\n"

# ---------------------------------------------------
# 2) Inicia o Autobot SERVER U1 (mock_server.py) na porta 5001
# ---------------------------------------------------
echo "[STARTUP] Desdobrando AUTOBOT SERVER U1 (porta 5001)..."
python3 -u pir-motion/modules/server/bumblebee.py 5001 1 \
    >> logs_server_U1.txt 2>&1 &

# ---------------------------------------------------
# 3) Inicia o Autobot SERVER U2 (mock_server1.py) na porta 5002
# ---------------------------------------------------
echo "[STARTUP] Desdobrando AUTOBOT SERVER U2 (porta 5002)..."
python3 -u pir-motion/modules/server/ironhide.py 5002 2 \
    >> logs_server_U2.txt 2>&1 &

# ---------------------------------------------------
# 4) Inicia o SENSOR PIR_SIM_01 (pir_simulator.py)
# ---------------------------------------------------
echo "[STARTUP] Ativando SENSOR PIR_SIM_01 e canais de comunicação..."
python3 -u pir-motion/modules/raspberry/pir_simulator.py \
    >> logs_pir_simulator.txt 2>&1 &

# ---------------------------------------------------
# 5) Mostra PIDs das instâncias levantadas
# ---------------------------------------------------
echo -e "\n[STARTUP] Instâncias em execução (PIDs):"
ps -f | grep -E "bumblebee.py|ironhide.py|pir_simulator.py" | grep -v grep

echo -e "\n[STARTUP] Todas as unidades Autobots estão ONLINE.\n"
echo "[STARTUP] Logs sendo salvos em: logs_server_U1.txt, logs_server_U2.txt, logs_pir_simulator.txt"
echo "[STARTUP] Para encerrar, use 'kill <PID>' de cada processo ou 'killall python3' se apropriado."
echo
