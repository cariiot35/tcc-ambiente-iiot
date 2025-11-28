#!/usr/bin/env python3
"""
GÊMEO DIGITAL - SISTEMA FRIGORÍFICO IoT
Estrutura completamente limpa, sem redundâncias
"""
import paho.mqtt.client as mqtt
import time
import os
import psutil
from datetime import datetime
from collections import deque

# ==================== CONFIGURAÇÕES ====================
BROKER_REAL = os.getenv("BROKER_REAL", "172.20.0.10")
BROKER_REAL_PORT = int(os.getenv("BROKER_REAL_PORT", 1883))
BROKER_VIRTUAL = os.getenv("BROKER_VIRTUAL", "172.20.0.30")
BROKER_VIRTUAL_PORT = int(os.getenv("BROKER_VIRTUAL_PORT", 1883))

# ==================== THRESHOLDS ====================
TIMEOUT_SEM_DADOS = 15
MSG_RATE_FLOOD = 3
PACOTES_THRESHOLD_DOS = 50000
TEMP_MIN, TEMP_MAX = -40, 100

# ==================== ESTADO ====================
estado = {
    "temperatura": None,
    "nivel": None,
    "bomba": None,
    "ultima_msg": None,
    "sincronizado": False,
    "broker_real_conectado": False,
    "broker_virtual_conectado": False,
}

metricas = {
    "status": "INICIALIZANDO",
    "ataque_inicio": None,
    "ataque_duracao": 0,
    "mqtt_msgs_recebidas": 0,
    "mqtt_msgs_por_segundo": 0.0,
    "mqtt_valores_invalidos": 0,
    "cpu_percent": 0.0,
    "mem_percent": 0.0,
    "net_packets_anterior": 0,
    "net_packets_por_segundo": 0,
}

timestamps_msgs = deque(maxlen=100)
client_real = mqtt.Client(client_id="Gemeo_Sub_Real")
client_virtual = mqtt.Client(client_id="Gemeo_Pub_Virtual")

# ==================== FUNÇÕES ====================
def ts():
    return datetime.now().strftime('%H:%M:%S')

def coletar_metricas_sistema():
    metricas["cpu_percent"] = psutil.cpu_percent(interval=None)
    metricas["mem_percent"] = psutil.virtual_memory().percent
    
    net = psutil.net_io_counters()
    pacotes_atual = net.packets_recv
    metricas["net_packets_por_segundo"] = pacotes_atual - metricas["net_packets_anterior"]
    metricas["net_packets_anterior"] = pacotes_atual

def calcular_taxa_msgs():
    agora = time.time()
    return sum(1 for t in timestamps_msgs if agora - t < 5) / 5

def validar_temperatura(valor_str):
    try:
        v = float(valor_str)
        if TEMP_MIN <= v <= TEMP_MAX:
            return v, True
        metricas["mqtt_valores_invalidos"] += 1
        return v, False
    except:
        metricas["mqtt_valores_invalidos"] += 1
        return None, False

# ==================== DETECÇÃO ====================
def detectar_status():
    agora = time.time()
    taxa = calcular_taxa_msgs()
    metricas["mqtt_msgs_por_segundo"] = round(taxa, 2)
    coletar_metricas_sistema()
    
    tempo_sem_dados = (agora - estado["ultima_msg"]) if estado["ultima_msg"] else 0
    pacotes_s = metricas["net_packets_por_segundo"]
    status_anterior = metricas["status"]
    novo_status = "NORMAL"
    
    if not estado["broker_real_conectado"]:
        novo_status = "DESCONECTADO"
    
    elif pacotes_s > PACOTES_THRESHOLD_DOS or (pacotes_s > PACOTES_THRESHOLD_DOS/2 and tempo_sem_dados > 5):
        novo_status = "DOS"
        if status_anterior != "DOS":
            metricas["ataque_inicio"] = agora
            print(f"\n🚨 [{ts()}] DoS DETECTADO!")
            print(f"   Pacotes/s: {pacotes_s}")
            print(f"   🚫 DADOS OPERACIONAIS BLOQUEADOS")
    
    elif taxa > MSG_RATE_FLOOD:
        novo_status = "FLOOD"
        if status_anterior != "FLOOD":
            metricas["ataque_inicio"] = agora
            print(f"\n🚨 [{ts()}] MQTT FLOOD DETECTADO!")
            print(f"   Taxa: {taxa:.1f} msg/s")
    
    elif status_anterior in ["FLOOD", "DOS"]:
        duracao = agora - metricas["ataque_inicio"] if metricas["ataque_inicio"] else 0
        print(f"\n✅ [{ts()}] MITIGADO! Duração: {duracao:.1f}s")
        if status_anterior == "DOS":
            print(f"   ✅ DADOS OPERACIONAIS RETOMADOS")
        novo_status = "MITIGADO"
        metricas["ataque_duracao"] = round(duracao, 1)
    
    elif status_anterior == "MITIGADO":
        if metricas["ataque_inicio"] and (agora - metricas["ataque_inicio"]) > 10:
            novo_status = "NORMAL"
    
    elif status_anterior == "DESCONECTADO" and estado["broker_real_conectado"]:
        print(f"\n✅ [{ts()}] BROKER RECONECTADO")
        novo_status = "NORMAL"
    
    if novo_status in ["FLOOD", "DOS"] and metricas["ataque_inicio"]:
        metricas["ataque_duracao"] = round(agora - metricas["ataque_inicio"], 1)
    
    metricas["status"] = novo_status

# ==================== CALLBACKS BROKER REAL ====================
def on_connect_real(client, userdata, flags, rc):
    if rc == 0:
        estado["broker_real_conectado"] = True
        print(f"✅ Broker REAL conectado ({BROKER_REAL})")
        client.subscribe("frigorifico/fisico/#", qos=1)
    else:
        estado["broker_real_conectado"] = False

def on_message_real(client, userdata, msg):
    valor = msg.payload.decode()
    agora = time.time()
    
    timestamps_msgs.append(agora)
    estado["ultima_msg"] = agora
    metricas["mqtt_msgs_recebidas"] += 1
    
    if not estado["sincronizado"]:
        estado["sincronizado"] = True
        metricas["status"] = "NORMAL"
        print(f"✅ [{ts()}] Sincronizado com ESP32\n")
    
    if "temperatura" in msg.topic:
        temp, ok = validar_temperatura(valor)
        if ok:
            estado["temperatura"] = temp
    elif "nivel" in msg.topic:
        try:
            estado["nivel"] = int(valor)
        except:
            pass
    elif "bomba" in msg.topic:
        estado["bomba"] = valor

def on_disconnect_real(client, userdata, rc):
    estado["broker_real_conectado"] = False
    if rc != 0:
        print(f"⚠️  [{ts()}] Broker REAL desconectado")

# ==================== CALLBACKS BROKER VIRTUAL ====================
def on_connect_virtual(client, userdata, flags, rc):
    if rc == 0:
        estado["broker_virtual_conectado"] = True
        print(f"✅ Broker VIRTUAL conectado ({BROKER_VIRTUAL})")

def on_disconnect_virtual(client, userdata, rc):
    estado["broker_virtual_conectado"] = False

# ==================== PUBLICAÇÃO (ZERO REDUNDÂNCIA) ====================
def publicar_dados():
    """
    Estrutura FINAL - Completamente Limpa:
    
    frigorifico/virtual/
      ├─ operacional/              → Dados do sistema (bloqueados durante DoS)
      │   ├─ temperatura
      │   ├─ nivel
      │   └─ bomba
      │
      └─ monitoramento/            → Métricas (sempre publicadas)
          ├─ status                → Estado geral do sistema
          ├─ timestamp             → Sincronização temporal
          ├─ ataque/
          │   └─ duracao           → Duração do ataque em segundos
          ├─ trafego/
          │   ├─ taxa_msgs         → Mensagens MQTT por segundo
          │   ├─ msgs_invalidas    → Contador de valores inválidos
          │   └─ pacotes_rede      → Pacotes de rede por segundo
          └─ sistema/
              ├─ cpu               → % CPU
              └─ memoria           → % Memória
    """
    if not estado["broker_virtual_conectado"]:
        return
    
    # ===== 1. DADOS OPERACIONAIS (bloqueados durante DoS) =====
    if metricas["status"] not in ["DOS", "DESCONECTADO"]:
        temp = f"{estado['temperatura']:.2f}" if estado["temperatura"] else "0"
        nivel = str(estado["nivel"]) if estado["nivel"] is not None else "0"
        bomba = estado["bomba"] if estado["bomba"] else "OFF"
        
        client_virtual.publish("frigorifico/virtual/operacional/temperatura", temp, qos=1)
        client_virtual.publish("frigorifico/virtual/operacional/nivel", nivel, qos=1)
        client_virtual.publish("frigorifico/virtual/operacional/bomba", bomba, qos=1)
    
    # ===== 2. MONITORAMENTO =====
    # Status e timestamp
    client_virtual.publish("frigorifico/virtual/monitoramento/status", 
                          metricas["status"], qos=1)
    client_virtual.publish("frigorifico/virtual/monitoramento/timestamp", 
                          str(int(time.time() * 1000)), qos=1)
    
    # Ataque
    client_virtual.publish("frigorifico/virtual/monitoramento/ataque/duracao", 
                          str(metricas["ataque_duracao"]), qos=1)
    
    # Tráfego
    client_virtual.publish("frigorifico/virtual/monitoramento/trafego/taxa_msgs", 
                          f"{metricas['mqtt_msgs_por_segundo']:.2f}", qos=1)
    client_virtual.publish("frigorifico/virtual/monitoramento/trafego/msgs_invalidas", 
                          str(metricas["mqtt_valores_invalidos"]), qos=1)
    client_virtual.publish("frigorifico/virtual/monitoramento/trafego/pacotes_rede", 
                          str(metricas["net_packets_por_segundo"]), qos=1)
    
    # Sistema
    client_virtual.publish("frigorifico/virtual/monitoramento/sistema/cpu", 
                          f"{metricas['cpu_percent']:.1f}", qos=1)
    client_virtual.publish("frigorifico/virtual/monitoramento/sistema/memoria", 
                          f"{metricas['mem_percent']:.1f}", qos=1)

def exibir_status():
    icones = {
        "NORMAL": "🟢", "FLOOD": "🔴", "DOS": "🔴",
        "MITIGADO": "🟡", "DESCONECTADO": "⚫", 
        "INICIALIZANDO": "⏳"
    }
    icone = icones.get(metricas["status"], "⚪")
    
    temp = f"{estado['temperatura']:.1f}°C" if estado["temperatura"] else "--.-°C"
    
    if estado["nivel"] == 1:
        nivel = "CHEIO"
    elif estado["nivel"] == 0:
        nivel = "VAZIO"
    else:
        nivel = "-----"
    
    bomba = estado["bomba"] if estado["bomba"] else "---"
    
    dados_pub = "🚫 BLOQ" if metricas["status"] in ["DOS", "DESCONECTADO"] else "✅ OK  "
    
    print(f"{icone} [{ts()}] {metricas['status']:12} | "
          f"🌡️  {temp:>7} | 💧 {nivel:>5} | ⚙️  {bomba:>3} | "
          f"📨 {metricas['mqtt_msgs_por_segundo']:>4.1f}/s | {dados_pub}")

# ==================== MAIN ====================
def main():
    client_real.on_connect = on_connect_real
    client_real.on_message = on_message_real
    client_real.on_disconnect = on_disconnect_real
    client_virtual.on_connect = on_connect_virtual
    client_virtual.on_disconnect = on_disconnect_virtual
    
    print(f"\n{'='*70}")
    print("           🔷 GÊMEO DIGITAL - FRIGORÍFICO IoT 🔷")
    print(f"{'='*70}")
    print(f"  📡 Broker REAL    : {BROKER_REAL}:{BROKER_REAL_PORT}")
    print(f"  📡 Broker VIRTUAL : {BROKER_VIRTUAL}:{BROKER_VIRTUAL_PORT}")
    print(f"{'='*70}")
    print(f"\n  STATUS:")
    print(f"    🟢 NORMAL       - Sistema operando normalmente")
    print(f"    🔴 FLOOD        - Ataque MQTT Flood detectado")
    print(f"    🔴 DOS          - Ataque DoS (dados bloqueados)")
    print(f"    🟡 MITIGADO     - Ataque finalizado")
    print(f"    ⚫ DESCONECTADO - Sem conexão com broker")
    print(f"{'='*70}\n")
    
    try:
        client_real.connect(BROKER_REAL, BROKER_REAL_PORT, 60)
        client_real.loop_start()
        time.sleep(1)
        client_virtual.connect(BROKER_VIRTUAL, BROKER_VIRTUAL_PORT, 60)
        client_virtual.loop_start()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    time.sleep(2)
    print(f"🚀 Sistema inicializado! Aguardando dados do ESP32...\n")
    
    contador = 0
    try:
        while True:
            time.sleep(1)
            contador += 1
            detectar_status()
            
            if contador >= 5:
                publicar_dados()
                exibir_status()
                contador = 0
                
    except KeyboardInterrupt:
        print(f"\n{'='*70}")
        print("                   📊 RELATÓRIO FINAL")
        print(f"{'='*70}")
        print(f"  📨 Mensagens recebidas   : {metricas['mqtt_msgs_recebidas']}")
        print(f"  ⚠️  Valores inválidos     : {metricas['mqtt_valores_invalidos']}")
        if estado['temperatura']:
            print(f"  🌡️  Temperatura final    : {estado['temperatura']}°C")
        else:
            print(f"  🌡️  Temperatura final    : N/A")
        print(f"  💧 Nível final          : {'CHEIO' if estado['nivel'] == 1 else 'VAZIO' if estado['nivel'] == 0 else 'N/A'}")
        print(f"  ⚙️  Bomba final          : {estado['bomba'] or 'N/A'}")
        print(f"{'='*70}\n")
        
        client_real.loop_stop()
        client_virtual.loop_stop()

if __name__ == "__main__":
    main()
