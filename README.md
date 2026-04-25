<div align="center">
  <img src="https://github.com/cariiot35/tcc-dashboard-iiot/blob/8f55a6b040ba20e2c24a13e980de1e76af37c7d8/CARIIoT/frontend/img/logo.png" alt="CARIIOT" width="600">
</div>

## Sobre CARIIoT 
<div align="justify">
O CARIIoT (Controle e Análise de Redes de Internet Industrial das Coisas) é um projeto de TCC desenvolvido na ETEC de Embu das Artes. O foco é a criação de um ambiente controlado para simulação de ataques em redes industriais (IIoT), permitindo o estudo de vulnerabilidades e a visualização de dados em tempo real.

## Descrição
Este repositório contém todos os artefatos necessários para reproduzir o ambiente virtual criado para **simulação de ataques em redes IIoT (Industrial Internet of Things)**. Inclui contêineres Docker, gêmeo digital, fluxos Node-RED, comandos utilizados nas simulações e documentação completa de execução.

## Visualização de Dados (Dashboard)
Este repositório é responsável pela geração e processamento dos dados. Para visualizar o monitoramento em tempo real, os alertas de segurança e a interface web do projeto, acesse o repositório do Dashboard: [**tcc-dashboard-iiot**](https://github.com/cariiot35/tcc-dashboard-iiot)

> **Aplicação Online:** [https://cariiot.web.app](https://cariiot.web.app)

## Tecnologias e Ferramentas
 - Linguagem: Python (Scripts de simulação e Gêmeo Digital).
 - Containerização: Docker & Docker Compose (Isolamento do ambiente).
 - Fluxos de Dados: Node-RED (Integração e automação).
 - Cloud/Hosting: Firebase (Hospedagem do dashboard).
 - Desenvolvimento: GitHub Codespaces.

## Estrutura do Repositório
 - `/docker`: Arquivos de configuração dos contêineres e orquestração.
 - `/node-red`: Fluxos configurados para coleta e processamento de dados.
 - `/digital-twin`: Implementação do gêmeo digital para espelhamento de processos.
 - `/scripts`: Scripts Python para testes de segurança e simulação de ataques.

## Como Executar o Ambiente
Como o projeto utiliza Docker, a inicialização é simplificada:

Clonar o repositório:
``` bash
git clone https://github.com/SEU-USUARIO/tcc-ambiente-iiot.git
```
Subir os serviços:
```bash
docker-compose up -d
```
Acessar as interfaces:

 - Node-RED: `http://localhost:1880`
 - API/Gêmeo Digital: `http://localhost:5000`

## Segurança e Ética
Este ambiente foi desenvolvido estritamente para fins educacionais e de pesquisa. As simulações de ataque (como DoS e Flood) devem ser executadas apenas em redes isoladas e controladas.

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).

## Autores
**Projeto desenvolvido por:** 
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
- [Docker Documentation](https://docs.docker.com/) - Referência técnica para a criação e orquestração dos contêineres do ambiente.
- [Node-RED Documentation](https://nodered.org/docs/) - Documentação utilizada para a automação dos fluxos de dados e integração de dispositivos.
- [OWASP IoT Security Testing Guide](https://owasp.org/www-project-iot-security-testing-guide/) - Metodologia base para os testes de invasão e análise de vulnerabilidades em dispositivos IoT.
- [ISA/IEC 62443 Standards](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) - Norma internacional utilizada como diretriz para a segurança cibernética de sistemas de controle e automação industrial.

**Última atualização:** 2026-04-23


> ⭐ Se este repositório foi útil, considere deixar uma estrela! ⭐
</div>
