# Projeto de Rede 1: IoT
## Sistema de Controle de Ventilação e Temperatura para uma Estufa

# Descrição
Este software simula um dispositivo equipado com um sensor de temperatura que controla uma janela de ventilação em um ambiente de estufa. Ele opera por meio de uma arquitetura de broker-client, onde o dispositivo simulado se comunica com um broker. O cliente, por sua vez, interage com a janela de ventilação, via broker, gerenciando suas operações com base nas leituras de temperatura recebidas do dispositivo. Além disso, o sistema fornece dados de temperatura em tempo real em Celsius (°C) para monitorar efetivamente o ambiente da estufa. O dispositivo se comunica com o broker via TCP/IP usando sockets, enquanto o broker se comunica com o cliente via RESTFUL. O dispositivo oscila entre 17ºC e 32°C a uma taxa de 0,1°C/s. Quando a janela está "Fechada", a temperatura começa a subir a uma taxa de 0,1°C/s e quando a janela está "Aberta", ocorre o oposto.

# Tabela de Conteúdos

1. [Descrição](#descrição)
2. [Requisitos](#requisitos)
3. [Instalação do Docker](#instalação-do-docker)
    - [Instalação do Docker no Linux](#instalação-do-docker-no-linux)
    - [Instalação do Docker no Windows](#instalação-do-docker-no-windows)
    - [Instalação do Docker no macOS](#instalação-do-docker-no-macos)
4. [Como configurar](#como-configurar)
   - [Como configurar o servidor usando Docker](#como-configurar-o-servidor-usando-docker)
   - [Como configurar o dispositivo usando Docker](#como-configurar-o-dispositivo-usando-docker)
   - [Como configurar o cliente usando Docker](#como-configurar-o-cliente-usando-docker)
5. [Como Excecutar o Aplicativo](#como-executar-o-aplicativo) 
   - [Como executar o cliente](#como-executar-o-cliente)
   - [Como configurar o cliente para se conectar ao servidor](#como-configurar-o-cliente-para-se-conectar-ao-servidor)
6. [Imagens](#imagens)
   - [Imagem do Servidor em uso](#imagem-do-servidor-em-uso)
   - [Imagem do Dispositivo em uso](#imagem-do-dispositivo-em-uso)
   - [Imagem da GUI do Cliente em uso](#imagem-da-gui-do-cliente-em-uso)
8. [Análise Final](#análise-final)
9. [Material de pesquisa adicional usado neste projeto](#material-de-pesquisa-adicional-usado-neste-projeto)



## Requisitos
  * Docker instalado

# Instalação do Docker

Este guia fornece instruções sobre como instalar o Docker em diferentes sistemas operacionais.

## Instalação do Docker no Linux
   #### Ubuntu/Debian:
    1. Abra um terminal.
    2. Execute os seguintes comandos:
       ```bash
       sudo apt-get update
       sudo apt-get install docker.io
       sudo systemctl start docker
       sudo systemctl enable docker

   #### Para verificar se a instalação foi bem-sucedida, execute:
    docker --version 
### [Site Oficial do Docker](https://docs.docker.com/desktop/install/windows-install/)    
## Instalação do Docker no Windows
    1. Baixe o instalador do Docker Desktop para Windows no Site Oficial do Docker: Docker Desktop for Windows
    2. Execute o instalador baixado e siga as instruções na tela.
    3. Após a instalação, o Docker Desktop será iniciado automaticamente. Aguarde até que o Docker Desktop seja totalmente inicializado.
    4. Verifique se a instalação foi bem-sucedida abrindo o PowerShell ou CMD e executando:
   #### bash:
     docker --version

## Instalação do Docker no macOS
    1. Baixe o instalador do Docker Desktop para macOS no Site Oficial do Docker: Docker Desktop for Mac
    2. Abra o arquivo .dmg baixado.
    3. Arraste o ícone do Docker para a pasta Aplicativos.
    4. Abra o Docker a partir do Launchpad ou Finder.
    5. O Docker será iniciado e estará disponível na barra de menus. Aguarde até que o Docker seja totalmente inicializado.
    6. Verifique se a instalação foi bem-sucedida abrindo o terminal e executando:
   #### bash:
     docker --version

# Como configurar
Este guia fornece instruções sobre como configurar o servidor, o dispositivo e o cliente. Isso deve ser feito nesta ordem.
## Como configurar o servidor usando Docker
   #### No terminal, digite:
    1. git clone https://github.com/alexsami-lopes/Networking-Project-1.git
    2. cd Networking-Project-1/server
    3. docker build -t server .
    4. docker container run -it --network host server

## Como configurar o dispositivo usando Docker
   #### No terminal, digite:
    1. git clone https://github.com/alexsami-lopes/Networking-Project-1.git
    2. cd Networking-Project-1/device
    3. docker build -t device .
    4. docker container run -it --network host device

## Como configurar o cliente usando Docker
   #### No terminal, digite:
    1. git clone https://github.com/alexsami-lopes/Networking-Project-1.git
    2. cd Networking-Project-1/client
    3. docker build -t meu-nginx .
    4. docker run -d -p 8080:80 meu-nginx
    
# Como executar o Aplicativo
Este guia fornece instruções sobre como executar o aplicativo para recuperar dados do dispositivo através do servidor.
## Como executar o cliente
   #### Na url do navegador, digite:
    1. http://localhost:8080/client.html
    
## Como configurar o cliente para se conectar ao servidor
   #### Na caixa "Endereço IP e Porta do Servidor (IP:Porta)", copie e cole o endereço do servidor Flask fornecido a você no terminal do servidor (na porta 9000), conforme visto na [Imagem do Servidor em uso](#imagem-do-servidor-em-uso), exemplo:
    1. 172.16.103.8:9000

   #### Na caixa "IP do Dispositivo (IPv4)", copie e cole o endereço do dispositivo fornecido a você no terminal do dispositivo (sem porta), conforme visto na [Imagem do Dispositivo em uso](#imagem-do-dispositivo-em-uso), exemplo:
    1. 172.16.103.9

### Clique em "Solicitar Temperatura" e em outros botões e aguarde alguns segundos para receber dados do dispositivo
[Imagem da GUI do Cliente em uso](#imagem-da-gui-do-cliente-em-uso)

# Imagens
Imagens mostrando o servidor, o dispositivo e o cliente sendo utilizados.
## Imagem do Servidor em uso
<img src="images/image-server-in-use.jpg" alt="Server" width="1671" height="846">

## Imagem do Dispositivo em uso
<img src="images/image-device-in-use.jpg" alt="Device" width="1671" height="446">

## Imagem da GUI do Cliente em uso
<img src="images/image-client-in-use.jpg" alt="Client-GUI" width="969" height="645">


# Análise Final
 O objetivo deste projeto foi alcançado! Aprendi a usar sockets para comunicar usando conexões TCP e UDP, além de usar o Flask para fazer uma comunicação RESTFUL entre um cliente e um servidor e como criar uma arquitetura de broker-client.

# Material de pesquisa adicional usado neste projeto
 [![Python Socket Programming Tutorial](https://raw.githubusercontent.com/alexsami-lopes/Networking-Project-1/main/images/Python%20Socket%20Programming%20Tutorial%20-%20Image.png)](https://www.youtube.com/watch?v=3QiPPX-KeSc)

 - [Retornar para a Tabela de Conteúdos](#tabela-de-conteúdos)
