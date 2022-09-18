# Render farm em python com suporte a socket e threads

Desenvolvedores:

Gustavo Lopes (eu : D)

[Rafael Amauri](https://github.com/RafaelAmauri)


### ⚠️ Aviso
O programa foi feito para ser utilizado no Linux. Embora alguns testes mostraram que ele roda sem problemas no Windows,
o grupo não teve interesse nem incentivo para dar suporte à versão Windows. É fortemente recomendado utilizar no Linux!

### 🚀 Como utilizar ?

Instale as dependências necessárias com o gerenciador de pacotes pip.
```
pip3 install -r requirements.txt
```

Para executar o programa como cliente, execute:

```
python3 client.py
```

Para executar o programa como servidor, execute:

```
python3 server.py
```
Enquanto servidor, apenas mande o nome do arquivo da imagem, para que a mesma seja enviada 
para os clientes.

Ou digite "!enumerate" para ver as threads criadas no lado do servidor.
