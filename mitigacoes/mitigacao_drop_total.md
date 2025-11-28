# Mitigação: Bloqueio Total do Tráfego MQTT

Comando utilizado:

```bash
sudo iptables -I OUTPUT -p tcp --dport 1883 -j DROP

Bloqueia toda saída TCP na porta 1883, impedindo que qualquer pacote MQTT seja enviado.

Usado para conter instantaneamente ataques ativos, como DoS ou MQTT Flood.

Efeito: todo o tráfego MQTT do host é bloqueado.
