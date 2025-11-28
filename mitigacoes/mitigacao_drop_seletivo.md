# Mitigação: Bloqueio Seletivo (Whitelist do Gêmeo)

Comando utilizado:

```bash
sudo iptables -A OUTPUT -p tcp --dport 1883 ! -s <IP do alvo> -j DROP //Ip do microcontrolador

Bloqueia toda saída TCP na porta 1883, exceto do IP do gêmeo (10.88.47.252).

Permite que o gêmeo continue operando normalmente enquanto se mitigam fontes suspeitas de ataques.

Estratégia de whitelisting para reduzir impacto sem interromper operação legítima.

