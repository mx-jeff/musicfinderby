# Musicfinderby

Programa que extrai videos para transforma-los em MP3

## Requisitos

- [Python](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe)
- [FFMpeg](http://ffmpeg.org/download.html)
## instalação 

    Abra o cmd/prompt, e execute esses comandos no terminal

    Crie o ambiente virtual com:
```python
    python -m venv venv    
```
    Com FFMpeg baixado, extraia os arquivos, copie os arquivos da pasta /Bin para dentro da pasta venv/scripts, que esta
    localizada dentro do seu diretório
    
```python
    pip install -r requirements.txt
 ```

## Execução
 - Após relizada instalação, execute esse comandos no prompt/terminal 

 ```python
    python index.py
 ```

- acesse este [link](https://musicfinderby.herokuapp.com/) para demonstração  

### Rotas

  - /search: busca o vídeo com base no nome e estrai o link para a rota '/download'
  ```link
   https://musicfinderby.herokuapp.com/search/michael-jackson   
```
  - /download: baixa o video com base no link
  ```link
   https://musicfinderby.herokuapp.com/search/michael-jackson
```