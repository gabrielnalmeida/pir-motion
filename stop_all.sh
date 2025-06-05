#!/usr/bin/env bash

# =============================================================================
#    Script para encerrar todos os processos referentes ao PIR-Simulator
#    e aos mock_servers (Autobot U1 e U2). Basta rodar:
#        ./stop_all.sh
# =============================================================================

echo "[SHUTDOWN] Iniciando protocolo de desligamento da FROTA AUTOBOT..."

# 1) Encontrar e matar processos que estejam executando os scripts
#    (ajuste o grep caso você tenha renomeado algum arquivo)

PIDS=$(ps -f | grep -E "pir_simulator.py|bumblebee.py|ironhide.py" | grep -v grep | awk '{print $2}')

if [[ -z "$PIDS" ]]; then
    echo "[SHUTDOWN] Nenhum processo Autobot encontrado em execução."
    exit 0
fi

# 2) Matar cada PID encontrado
for pid in $PIDS; do
    echo "[SHUTDOWN] Encerrando processo PID $pid ..."
    kill -9 $pid
    # Se quiser forçar, substitua por: kill -9 $pid
done

echo "[SHUTDOWN] Todos os processos sinalizados para término. Verifique com 'ps -f' se algum ainda está ativo."
echo "[SHUTDOWN] Operação concluída."
