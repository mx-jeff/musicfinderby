# musicfinderby

API Flask que localiza um vídeo no YouTube e converte o áudio para MP3, acompanhada de um frontend web simples servido por Nginx.

## Arquitetura

| Serviço | Container | Porta padrão | Função |
|---|---|---|---|
| `musicfinderby` | `musicfinderby` | 5000 | API Flask + Gunicorn (FFmpeg, Chromium, Chromedriver) |
| `frontend` | `musicfinderby-frontend` | 8080 | Nginx: serve `./public` e faz proxy de `/search`, `/download`, `/music` e `/api` para a API |

O frontend usa caminhos relativos (`BASE_LINK = ""`), então todas as chamadas passam pelo Nginx.

## Executar com Docker Compose

Requisitos: Docker Engine e Docker Compose v2.

1. (Opcional) Crie o arquivo de ambiente a partir do exemplo:

```bash
cp .env.example .env
```

2. Suba os serviços:

```bash
docker compose up --build -d
```

3. Verifique se estão de pé:

```bash
docker compose ps
```

O serviço `frontend` deve aparecer como `Up`, com `0.0.0.0:8080->80/tcp`.

Acompanhar os logs:

```bash
docker compose logs -f musicfinderby
```

Parar os serviços:

```bash
docker compose down
```

## Como acessar

### Frontend (interface web)

| Onde você está | Endereço |
|---|---|
| Na mesma máquina que roda o Docker | `http://localhost:8080` |
| Outro dispositivo na mesma rede (celular, outro PC) | `http://<IP-da-máquina>:8080` |
| Servidor/VPS na nuvem | `http://<IP-público-ou-domínio>:8080` |

Ao abrir, a página mostra "Iniciando site..." e libera o campo de busca quando a rota `/api` responde. Esse é o sinal de que o frontend e a API estão se comunicando.

Para descobrir o IP da máquina:

```bash
hostname -I               # Linux
ipconfig getifaddr en0    # macOS
ipconfig                  # Windows (veja "Endereço IPv4")
```

### API direta

`http://localhost:5000/api`

A rota `/` não existe na API (retorna 404). A raiz só responde no frontend, na porta 8080.

### Se não abrir de outro dispositivo

- Libere a porta 8080 no firewall (`sudo ufw allow 8080` no Ubuntu) ou no security group, se estiver na nuvem. Libere a 5000 apenas se quiser expor a API diretamente.
- Confirme que os containers estão rodando com `docker compose ps`.
- O Nginx usa `server_name _`, então responde para qualquer host ou IP; não é necessário configurar domínio.
- Os nomes `musicfinderby` e `frontend` só resolvem dentro da rede do Docker (é assim que o Nginx encontra a API). Do navegador, use `localhost`, o IP ou o domínio.

## Variáveis de ambiente (`.env`)

O projeto não usa segredos. As variáveis abaixo são opcionais e controlam apenas as portas expostas no host:

| Variável | Padrão | Descrição |
|---|---|---|
| `API_PORT` | `5000` | Porta do host exposta para a API |
| `FRONTEND_PORT` | `8080` | Porta do host exposta para o frontend |

Exemplo de `.env.example`:

```env
API_PORT=5000
FRONTEND_PORT=8080
```

Para que o compose use essas variáveis, os blocos `ports` do `docker-compose.yml` ficam assim:

```yaml
services:
  musicfinderby:
    ports:
      - "${API_PORT:-5000}:5000"

  frontend:
    ports:
      - "${FRONTEND_PORT:-8080}:80"
```

Se alterar `FRONTEND_PORT`, use a nova porta no lugar do 8080 ao acessar o frontend.

Já definidas no `docker-compose.yml`/`Dockerfile` (não precisam ir para o `.env`):

| Variável | Valor | Descrição |
|---|---|---|
| `PYTHONUNBUFFERED` | `1` | Logs sem buffer |
| `CHROMEDRIVER_PATH` | `/usr/bin/chromedriver` | Caminho do Chromedriver do sistema |

Boas práticas: commite o `.env.example` e adicione `.env` ao `.gitignore`.

## Endpoints

| Rota | Descrição | Respostas |
|---|---|---|
| `GET /api` | Mensagem de boas-vindas; o frontend usa para saber se a API subiu | `200` |
| `GET /search/<nome-da-musica>` | Pesquisa no YouTube | `200` `{"url": "<link do vídeo>"}`; `500` `{"error": ...}` |
| `GET /download/?url=<url-do-youtube>` | Inicia download e conversão para MP3 em segundo plano | `202` `{"status": "started"}`; `400` se faltar `url`; `500` em erro |
| `GET /music` | Consulta o andamento e baixa o MP3 | `202` `{"status": "running"}` enquanto processa; `200` com o arquivo `audio/mpeg`; `404` se não houver download em andamento ou a música não estiver disponível; `500` em erro |

Fluxo completo via `curl`:

```bash
# 1. buscar a URL do vídeo
curl "http://localhost:5000/search/lofi%20hip%20hop"

# 2. iniciar o download (use a URL retornada acima)
curl "http://localhost:5000/download/?url=<url-do-youtube>"

# 3. repetir até deixar de retornar 202, então salvar o MP3
curl -OJ "http://localhost:5000/music"
```

## Persistência

Os arquivos MP3 e o `log.txt` são mantidos no diretório local `./downloads`, montado como volume em `/app/downloads`.

## Deploy em VPS

O fluxo é o mesmo do ambiente local, com ajustes de segurança e infraestrutura.

### 1. Preparar a VPS

```bash
# Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER   # depois faça logout/login

# projeto
git clone <seu-repo> musicfinderby && cd musicfinderby
cp .env.example .env
```

Recursos recomendados: pelo menos 1 a 2 GB de RAM (Chromium + FFmpeg).

### 2. Permissão da pasta `downloads`

O container roda como `appuser` (UID 10001). Se `./downloads` for criada pelo root, a aplicação não consegue gravar:

```bash
mkdir -p downloads && sudo chown -R 10001:10001 downloads
```

### 3. Portas e firewall

- Para acessar direto por IP, defina `FRONTEND_PORT=80` no `.env` e abra apenas essa porta (e a 22 do SSH).
- A API (5000) não precisa ficar pública: o Nginx já faz o proxy pela rede interna do Docker. Publique-a apenas no localhost:

```yaml
services:
  musicfinderby:
    ports:
      - "127.0.0.1:${API_PORT:-5000}:5000"
```

- O Docker ignora o `ufw` para portas publicadas, então `ufw deny 5000` não basta. Restringir o bind a `127.0.0.1` é o que realmente fecha a porta.

### 4. Subir

```bash
docker compose up --build -d
docker compose ps
```

Acesse em `http://<IP-da-VPS>` (ou `http://<IP-da-VPS>:8080`, se mantiver a porta padrão).

### 5. Domínio e HTTPS (recomendado)

1. Crie um registro DNS `A` apontando o domínio para o IP da VPS.
2. Publique o frontend apenas no localhost, no `docker-compose.yml`:

```yaml
  frontend:
    ports:
      - "127.0.0.1:${FRONTEND_PORT:-8080}:80"
```

3. Instale o [Caddy](https://caddyserver.com/docs/install) no host e use este `Caddyfile`:

```
musica.seudominio.com {
    reverse_proxy localhost:8080
}
```

O Caddy emite e renova o certificado automaticamente. Mantenha o `proxy_read_timeout 300s` do Nginx. Como `/music` responde `202` e é consultado por polling, o limite de tempo por requisição de proxies como o Cloudflare normalmente não é problema.

### 6. Atualizar a aplicação

```bash
git pull && docker compose up --build -d
```

O `restart: unless-stopped` já sobe os containers novamente após o reboot da VPS.

### Pontos de atenção

- **Sem autenticação:** qualquer pessoa com o endereço pode usar a VPS para baixar e converter vídeos. Considere basic auth no Nginx/Caddy ou restrição por IP.
- **Bloqueio do YouTube:** IPs de datacenter costumam receber verificação anti-bot. Combinado com o `youtube-dl` de 2021, é provável que falhe na VPS mesmo funcionando localmente. Migrar para `yt-dlp` ajuda; em alguns casos é necessário fornecer cookies.
- **Disco:** a pasta `downloads` só remove o MP3 anterior a cada novo download, e o `log.txt` cresce com o tempo. Considere rotacionar o log.

## Limitações

- Existe apenas um slot de download por vez: um novo `/download/` remove o MP3 anterior, e o resultado de `/music` é consumido na primeira leitura bem-sucedida. A API não é adequada para uso simultâneo por vários usuários.
- O serviço usa um único worker do Gunicorn porque o processamento assíncrono depende de estado em memória (`Flask-Executor`).
- A API libera CORS e expõe o header `Content-Disposition`, então também pode ser consumida de outra origem.

## Observações

- A imagem instala **FFmpeg**, **Chromium**, **Chromedriver** e **Deno**.
- O Nginx usa timeouts de 300s para acomodar downloads longos.
- O Chromedriver do sistema é usado automaticamente pela aplicação por meio de `CHROMEDRIVER_PATH`.
- O projeto usa `youtube-dl==2021.6.6`, que pode apresentar limitações com mudanças recentes do YouTube. Se isso ocorrer, considere migrar para `yt-dlp`.