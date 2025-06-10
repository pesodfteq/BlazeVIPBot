import requests
import time
from telegram import Bot
from collections import Counter

TOKEN = '8001499858:AAEUBMJQzLaJG7wW17Xpjx5hZbaGS8SwzWU'
CHAT_ID = '4915577545'
bot = Bot(token=TOKEN)

ultima_partida_id = None
historico_cores = []

# Mapear cores
# 0 = branco, 1 = vermelho, 2 = preto
cor_nome = {0: '⚪️ Branco', 1: '🔴 Vermelho', 2: '⚫️ Preto'}

def pegar_resultados():
    try:
        url = 'https://blaze.com/api/roulette_games/recent'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.json()
    except:
        pass
    return []

def analisar_tendencias(cores):
    ultimos_20 = cores[:20]
    contagem = Counter(ultimos_20)
    vermelho = contagem[1]
    preto = contagem[2]
    branco = contagem[0]

    mensagem = ""
    if vermelho >= 14:
        mensagem += "🔴 Tendência muito forte de vermelho (14+ nos últimos 20)\n"
    elif preto >= 14:
        mensagem += "⚫️ Tendência muito forte de preto (14+ nos últimos 20)\n"

    if cores[:5].count(1) >= 4:
        mensagem += "🔴 Padrão recente vermelho (4+ em 5)\n"
    if cores[:5].count(2) >= 4:
        mensagem += "⚫️ Padrão recente preto (4+ em 5)\n"

    if branco == 0:
        mensagem += "⚪️ Nenhum branco nas últimas 20 rodadas\n"

    return mensagem.strip()

def checar_padrao_reincidente(cores):
    if len(cores) >= 12:
        if cores[0] == 0 and cores[6] == 0:
            return "⚪️ Dois brancos em padrão de repetição a cada 6 rodadas. Alerta branco!"
    return None

def decidir_e_enviar():
    global ultima_partida_id, historico_cores

    resultados = pegar_resultados()
    if not resultados:
        return

    rodada_atual = resultados[0]
    if rodada_atual['id'] == ultima_partida_id:
        return

    ultima_partida_id = rodada_atual['id']
    cores = [r['color'] for r in resultados]
    historico_cores = cores + historico_cores
    historico_cores = historico_cores[:100]

    analise = analisar_tendencias(historico_cores)
    reincidente = checar_padrao_reincidente(historico_cores)

    if analise:
        bot.send_message(chat_id=CHAT_ID, text='📊 Análise:\n' + analise)
    if reincidente:
        bot.send_message(chat_id=CHAT_ID, text=reincidente)

def main():
    bot.send_message(chat_id=CHAT_ID, text='🤖 Bot Blaze VIP iniciado com lógica avançada.')
    while True:
        decidir_e_enviar()
        time.sleep(15)

if _name_ == "_main_":
    main()