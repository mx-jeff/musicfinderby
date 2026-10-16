# musicfinderby

API Flask que localiza um vídeo no YouTube e converte o áudio para MP3.

## Executar com Docker Compose

Requisitos: Docker Engine e Docker Compose v2.

```bash
docker compose up --build -d
```

A API ficará disponível em `http://localhost:5000`.

Para acompanhar os logs:

```bash
docker compose logs -f musicfinderby
```

Para parar o serviço:

```bash
docker compose down
```

Os arquivos MP3 e o `log.txt` são persistidos no diretório local `./downloads`.

## Endpoints

- `GET /` — mensagem de boas-vindas.
- `GET /search/<nome-da-musica>` — pesquisa no YouTube e inicia o download.
- `GET /download/?url=<url-do-youtube>` — inicia o download direto a partir de uma URL.
- `GET /music` — aguarda/retorna o MP3 gerado.

Exemplo:

```bash
curl -L "http://localhost:5000/search/lofi%20hip%20hop" -o musica.mp3
```

## Observações

- A imagem instala **FFmpeg**, **Chromium** e **Chromedriver**.
- O serviço usa um único worker do Gunicorn porque o processamento assíncrono usa estado em memória (`Flask-Executor`).
- O Chromedriver do sistema é usado automaticamente pela aplicação por meio de `CHROMEDRIVER_PATH`.
- O projeto original usa `youtube-dl==2021.6.6`, que pode apresentar limitações com mudanças recentes do YouTube. Se isso ocorrer, considere migrar para `yt-dlp` em uma etapa posterior.
