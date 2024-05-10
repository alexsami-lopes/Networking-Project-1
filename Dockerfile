# Use a Python base image
FROM python:3.9-slim

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Instale as dependências do seu aplicativo
RUN pip install flask flask-cors

# Copie os arquivos do aplicativo para o contêiner
COPY . /app

# Expor as portas TCP 8061, UDP 8062 e 9000
EXPOSE 8061 8062 9000

# Defina o comando de inicialização do seu aplicativo
CMD ["python", "server.py"]
