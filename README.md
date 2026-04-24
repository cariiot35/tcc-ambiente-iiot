<div align="center">
  <img src="https://github.com/cariiot35/tcc-dashboard-iiot/blob/8f55a6b040ba20e2c24a13e980de1e76af37c7d8/CARIIoT/frontend/img/logo.png" alt="CARIIOT" width="750">
</div>

## Sobre CARIIoT 
<div align="justify">
CARIIoT (Controle e Análise de Redes de Internet Industrial das Coisas) trata-se de um projeto de Trabalho de Conclusão de Curso (TCC) voltado para o desenvolvimento de um ambiente de teste de ataques em   dispositivos IIoT.
</div>

## Descrição
[![Python](https://img.shields.io/badge/Python-98.8%25-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-1.2%25-informational)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE) <br>
Este repositório contém todos os artefatos necessários para reproduzir o ambiente virtual criado para **simulação de ataques em redes IIoT (Industrial Internet of Things)**. Inclui contêineres Docker, gêmeo digital, fluxos Node-RED, comandos utilizados nas simulações e documentação completa de execução.

## Objetivos

 - Reproduzir um ambiente IIoT realista e escalável;
 - Permitir simulação de cenários de ataque;
 - Facilitar testes de segurança em redes industriais;
 - Documentar todos os procedimentos e configurações;
 - Fornecer uma base para pesquisa e análise de vulnerabilidades.

## Estrutura do Repositório

```
tcc-ambiente-iiot/
├── docker/                    # Configurações e Dockerfiles
│   ├── docker-compose.yml    # Orquestração dos contêineres
│   └── Dockerfile            # Definições de imagens
├── node-red/                  # Fluxos Node-RED
│   └── flows.json            # Configurações dos fluxos
├── digital-twin/              # Implementação do Gêmeo Digital
│   └── [arquivos do gêmeo]
├── scripts/                   # Scripts de simulação
│   └── [scripts de ataque/teste]
├── docs/                      # Documentação adicional
│   ├── INSTALACAO.md
│   ├── CONFIGURACAO.md
│   └── GUIA_SIMULACOES.md
├── README.md                  # Este arquivo
└── requirements.txt           # Dependências Python
```

## Início Rápido

### Pré-requisitos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Python** 3.9+
- **Node-RED** (pode ser rodado em contêiner)
- Git

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cariiot35/tcc-ambiente-iiot.git
   cd tcc-ambiente-iiot
   ```

2. **Instale as dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie os contêineres Docker:**
   ```bash
   docker-compose up -d
   ```

4. **Configure os fluxos Node-RED:**
   - Acesse a interface Node-RED em `http://localhost:1880`
   - Importe os fluxos do diretório `node-red/`

5. **Inicialize o gêmeo digital:**
   ```bash
   python digital-twin/main.py
   ```

## Componentes Principais

### Docker & Contêineres
Os contêineres fornecem isolamento e reprodutibilidade do ambiente IIoT. Todos os serviços estão orquestrados via Docker Compose.

### Gêmeo Digital (Digital Twin)
Implementação de um gêmeo digital que espelha o comportamento dos sistemas industriais reais, permitindo simulações sem afetar a infraestrutura real.

### Node-RED
Plataforma de fluxos visuais para integração de dispositivos IoT e IIoT. Os fluxos estão pré-configurados para:
- Coleta de dados
- Processamento em tempo real
- Simulação de eventos
- Disparo de alertas

### Simulações de Ataque
Scripts Python para simular diferentes tipos de ataques em redes IIoT:
- DoS (Denial of Service)
- Man-in-the-Middle (MITM)
- Injeção de comandos
- Roubo de dados
- Outros cenários de ataque

## Configuração Detalhada

Para instruções de configuração avançada, consulte:
- [INSTALACAO.md](docs/INSTALACAO.md) - Guia de instalação passo a passo
- [CONFIGURACAO.md](docs/CONFIGURACAO.md) - Configurações de ambiente
- [GUIA_SIMULACOES.md](docs/GUIA_SIMULACOES.md) - Como executar as simulações

## Variáveis de Ambiente

Configure as seguintes variáveis antes de executar:

```bash
# Exemplo de .env
NODE_RED_PORT=1880
DIGITAL_TWIN_PORT=5000
DOCKER_NETWORK=iiot-network
DEBUG=false
```

## Segurança e Avisos

**AVISO IMPORTANTE:**
- Este ambiente é destinado **apenas para fins educacionais e de pesquisa**
- Use em ambientes **controlados e isolados**
- Nunca use em sistemas de produção ou redes reais sem autorização explícita
- Cumpra todas as leis e regulamentações de segurança cibernética

## Tecnologias Utilizadas

| Tecnologia | Descrição | Versão |
|-----------|-----------|---------|
| **Python** | Linguagem principal para scripts | 3.9+ |
| **Docker** | Containerização | 20.10+ |
| **Node-RED** | Automação de fluxos IIoT | Última |
| **Docker Compose** | Orquestração de contêineres | 2.0+ |

## Como Usar

### Executar o Ambiente Completo

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar os serviços
docker-compose down
```

### Executar uma Simulação Específica

```bash
# Exemplo: executar simulação de DoS
python scripts/dos_attack.py --target localhost --duration 60

# Com mais opções
python scripts/dos_attack.py --help
```

### Acessar Serviços

- **Node-RED**: http://localhost:1880
- **Gêmeo Digital**: http://localhost:5000
- **API IIoT**: http://localhost:8000

## Testes e Validação

Execute os testes unitários:

```bash
python -m pytest tests/ -v
```

Valide a configuração:

```bash
python scripts/validate_environment.py
```

## Troubleshooting

### Problema: Contêineres não iniciam
```bash
# Verifique se Docker está rodando
docker ps

# Limpe imagens antigas
docker system prune -a

# Reconstrua as imagens
docker-compose build --no-cache
```

### Problema: Porta já em uso
```bash
# Encontre o processo usando a porta
lsof -i :1880

# Altere a porta no docker-compose.yml
```

Para mais informações, consulte [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Suporte e Contribuições

### Relatando Problemas
Se encontrar um bug ou problema:
1. Verifique as [Issues](https://github.com/cariiot35/tcc-ambiente-iiot/issues) existentes
2. Crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Logs e mensagens de erro
   - Ambiente (SO, versões)

### Contribuindo
Contribuições são bem-vindas! Para contribuir:
1. Faça um Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Autores

**Desenvolvido por:** 
 - Laís de Sá Santos;
 - Lázaro Levy Fragoso de Souza; 
 - Lucas Silva Matos;
 - Maria Clara Jardim Oliveira;
 - Marina de Jesus Carneiro;
 - Nicoly Karoline Matzembacher;
 - Rafaela Oliveira Correia;
 - Vitor Marçal Moreira.

**Instituição:** Etec de Embu

**Ano:** 2025

## Agradecimentos

Agradecimentos especiais a:
- Orientador(a) do TCC;
- Comunidade open-source;
- Ferramentas utilizadas (Docker, Python, Node-RED).

## Referências

- [Docker Documentation](https://docs.docker.com/)
- [Node-RED Documentation](https://nodered.org/docs/)
- [OWASP IoT Security](https://owasp.org/www-project-iot-security/)
- [IEC 62443 - Industrial Automation and Control Systems Security](https://webstore.iec.ch/publication/26425)

**Última atualização:** 2026-04-23

> ⭐ Se este repositório foi útil, considere deixar uma estrela! ⭐
