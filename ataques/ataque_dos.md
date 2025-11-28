# Ataque DoS com hping3

Comando utilizado:

```bash
hping3 -S -p 1883 --flood 172.20.0.20

Envia pacotes TCP SYN de forma massiva (--flood) para a porta 1883 (MQTT).

IP alvo: 172.20.0.20 (réplica)

Objetivo: sobrecarregar a réplica e impedir publicação de dados no broker associado..

Estratégia: ataque DoS clássico via SYN flood.
