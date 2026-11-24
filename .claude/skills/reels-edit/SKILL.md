---
name: reels-edit
description: Edita Reels do Instagram de ponta a ponta no Claude Code, em português do Brasil. Pega um clipe bruto (com retakes) ou um corte já pronto, corta, monta a versão vertical 1080x1920 a 30 fps com o HyperFrames (legendas, títulos, B-roll, música e efeitos grátis) e entrega um MP4 H.264/AAC BT.709 em renders/<nome do projeto>.mp4. Também monta React com pausa (tela dividida com o vídeo original e você reagindo, pausa, você em tela cheia), com crédito e limite de trecho. Use quando o usuário pedir "edita esse reel", "faz o react desse vídeo", "reage a esse vídeo", "corta esse vídeo", "faz o reel", "legenda esse vídeo", "monta o vertical", "edita esse clipe pro Instagram" ou citar um arquivo de vídeo para editar. ANTES de qualquer edição, lê o ESTILO.md que fica dentro desta skill (.claude/skills/reels-edit/ESTILO.md): ele é a fonte única do estilo e vence qualquer outra regra.
---

# Editor de Reels

Transforma um clipe bruto ou um corte já pronto em um Reel pronto para postar: o corte, o texto na tela, a legenda,
o B-roll, o som e um MP4 vertical. Tudo roda na máquina (HyperFrames = Chrome + FFmpeg), sem custo por render.

## Regra zero: ler o ESTILO.md

**Antes de qualquer edição, leia `.claude/skills/reels-edit/ESTILO.md`** (`$SK/ESTILO.md`). É a **fonte única do estilo**: cores, fontes, título, legenda, câmera, ritmo, som, formatos e a lista do que nunca se faz. Este SKILL.md cuida só da técnica.

- **Ele vence qualquer outra regra**: este SKILL.md, os scripts, as skills do HyperFrames. Se o ESTILO.md diz uma coisa e
  este arquivo diz outra, vale o ESTILO.md. Quando o conflito mudar o resultado, avise em uma linha qual regra foi vencida.
- **Se o arquivo não existir**, pare e avise o usuário. Não invente um estilo.
- **Valores marcados `[confirmar]`** no ESTILO.md: use e diga na entrega que foi um palpite.
- **Escolha o formato** da seção 4 do ESTILO.md (opinião, resposta a pergunta, tutorial com B-roll, história, lista) e siga a receita; se o pedido não deixar claro, pergunte.
- Releia o arquivo a cada edição nova: o usuário pode ter mudado.

## O que sai (especificação)

| Item | Valor |
|---|---|
| Tela | em pé, **1080x1920** (9:16). Nada de 4K, nada de 16:9 |
| Quadros | **30 fps** constante |
| Vídeo / áudio | **H.264** (yuv420p) + **AAC** 48 kHz |
| Cor | **BT.709** (primárias, transferência e matriz marcadas) |
| Idioma | **português do Brasil** em tudo: transcrição, texto na tela, legenda, títulos |
| Área segura | todo texto e legenda dentro de **x 60 a 940 e y 220 a 1500** |
| Abertura | algo acontece em **1 a 3 s**; o **primeiro quadro é uma imagem com sentido** (ele vira a capa) |
| Montagem | composição escrita com as **skills do HyperFrames** (não existe `compose.py` aqui) |
| Música e efeitos | **só grátis**: biblioteca do HyperFrames, Pixabay, YouTube Audio Library |
| Entrega | `renders/<nome do projeto>.mp4` |

Variáveis usadas nos comandos, a partir da raiz do projeto: `SK=".claude/skills/reels-edit"` e `W="videos/<projeto>"`
(uma pasta de trabalho por vídeo). `<projeto>` é um nome curto, sem espaço, sem acento (ex.: `reel-dicas-vendas`).

## Verificação do ambiente (primeiro uso e depois de atualizar)

| Precisa | Como checar | Se faltar |
|---|---|---|
| Node.js 22+ | `node -v` | nodejs.org, `brew install node` ou o gerenciador de pacotes |
| HyperFrames | `npx hyperframes --version` e `npx hyperframes doctor` | `npm i -D hyperframes`; skills: `npx hyperframes skills update media-use` |
| FFmpeg e ffprobe | `ffmpeg -version` | `brew install ffmpeg`, `winget install ffmpeg` ou o gerenciador de pacotes |
| Python 3 com numpy | `python3 -c "import numpy"` | `python3 -m pip install numpy` |
| auto-editor | `auto-editor --version` | `pip install auto-editor` |
| Parakeet (transcrição) | `npx hyperframes models list` | `npx hyperframes models install parakeet` (baixa de huggingface.co) |
| Google Chrome | `doctor` mostra `Chrome ✓` | google.com/chrome |
| GSAP local | `$SK/assets/vendor/gsap.min.js` existe | `npm pack gsap@3.14.2` e copie `package/dist/gsap.min.js` para lá |
| yt-dlp (opcional) | `yt-dlp --version` | `pip install yt-dlp` |

Depois, **da pasta de scripts** (não de dentro de `tests/`): `cd "$SK/scripts" && python3 -m unittest tests`. Tem que terminar
em `OK`. Rode de novo ao mexer em qualquer script.

- **Parakeet é obrigatório** (`--engine parakeet --language pt`). Se não estiver instalado ou o download falhar, **pare e diga**.
  Não troque de motor por conta própria.
- O `doctor` pode marcar `whisper-cpp`, `Kokoro`, `MusicGen` e `Docker` como ausentes. Nenhum é necessário aqui.
- O aviso "loudness só comparável no FFmpeg 8.0.1" do `doctor` é só informativo.

## Rotas

| Entrada | Rota |
|---|---|
| **React com pausa** (o original + você reagindo + suas falas) | a rota React (abaixo) |
| Um clipe bruto (retakes e tudo) | Etapa de corte → Montagem vertical → Checagens → Render → Entrega |
| Vários clipes brutos de um mesmo reel | `ingest.py` junta em `source.mp4` → mesma rota |
| Um corte já pronto (sem zoom, legenda ou transição gravados) | pula a etapa de corte; vai direto ao "Corte plano para vertical" |
| Gravação de tela e rosto em arquivos separados | grave os dois com o mesmo microfone; o rosto vira o vídeo principal e a tela entra como cutaway em tela cheia |

**Dois pontos de parada com o usuário por vídeo; o resto roda sozinho.**
**A, o corte:** `PAPER-CUT.md` (o que sai e por quê); o usuário responde em palavras simples ("mantém a primeira versão da frase do preço").
**B, o plano:** a lista de momentos (`plano.md`) e a folha de quadros `snaps/` com cada momento de texto como imagem. Só então render.

**Portão da abertura** (em todo reel, no ponto B):
- Algo acontece entre **1 e 3 s**: o texto-gancho entra, o corte muda, o zoom empurra. Escreva no plano qual é.
- **O quadro 0 é uma imagem com sentido** (rosto, resultado, ou o título já na tela). Nunca preto, nunca logo, nunca câmera
  assentando. Ele vira a capa: `verify-render.py` exporta `capa.png`.
- Funciona **sem som**: o primeiro texto diz a promessa sozinho. A primeira palavra falada não é atropelada por efeito sonoro.
- A promessa tem hora de entrega (payoff) dentro do reel. Feche antes de qualquer chamada para ação.

## Como gravar para o corte funcionar

- Grave em vertical a 30 fps (a fonte pode ser 4K; a saída é sempre 1080x1920), cor padrão, plano reto (sem zoom, legenda ou transição gravados), microfone em todo arquivo,
  um segundo de silêncio no começo e no fim. Se gravar na horizontal, o `apply-cut.py --size` recorta o centro: deixe o rosto
  centralizado.
- **Errou a frase? Pare uns 2 segundos e recomece a frase inteira do começo.** A última tomada vence. Se errou número, nome
  ou preço, refaça a frase toda. "Corta isso" ou "começa de novo" descarta o trecho.
- Sem lousa falada nem recado para você mesmo (viram fala e são mantidos); bata palma. Diga listas como listas, fale o nome
  das ferramentas e diga dinheiro por extenso ("mil reais por mês", não "1k").

## Scripts (`scripts/`)

| Script | Faz | Opções |
|---|---|---|
| `ingest.py` | junta vários clipes em um `source.mp4` e mapeia o tempo de volta | `--raw --out [--concat] [--order A,B] [--only A,B] [--name]` |
| `paper-cut.py` | o que remover de um clipe bruto: recomeços, "corta isso", retakes (mantém o último), falsos começos, pausas longas; entende português | `--transcript --duration --out-dir --speech`; escreve `cut-list.json` + `PAPER-CUT.md` |
| `hand-cut.py` | refaz o `cut-list.json` a partir das linhas que você mantém | `--keep A-B` (`A-B!` mantém inteiro) `--transcript --speech --duration --out-dir` |
| `tighten-cut.py` | apara entradas, finais e pausas internas pelo som | `--audio --cut-list --out [--lead 0.07] [--tail 0.11] [--maxgap 0.30]` |
| `sliver.py` | o que o edge-audit deixa passar: respiração isolada, resto de palavra cortada, pontas curtas | `--cut-list --audio [--fix]` |
| `edge-audit.py` | cada emenda conferida pelo áudio: começa ou termina no meio do som | `--audio --cut-list --transcript [--keeps FILE] [--fix] [--threshold 300]` |
| `apply-cut.py` | **um** re-encode com precisão de quadro, **já em 1080x1920** (`--size`), 30 fps, BT.709; escreve `cut-map.json` | `--input --cut-list --out --size 1080x1920 [--crop-x 0.5] [--fps 30] [--crf 16]` |
| `dead-air.py` | toda pausa acima de 0,40 s no fim de frase (0,45 s no meio), pelo áudio | `W [--plan] [--keep T] [--max 0.45] [--max-sentence 0.40] [--target 0.30]` |
| `patch-cut.py` | ajustes pequenos no cut-list | `--cut-list` com `--add A-B`, `--drop T` ou `--drop-flat A-B` |
| `stutter-scan.py` | gagueiras e retakes no texto do corte plano, segunda opinião | `--transcript --out-dir` |
| `cutlist-to-edl.py` | o cut-list como EDL para a página de revisão (`node build-edl-review.mjs`) | `--cut-list --out` |
| `phrase-times.py` | onde uma frase é dita (início da 1ª palavra, fim da última) | `--transcript "frase" ... [--after T]` |
| `sync-tracks.py` | onde o original começa dentro da sua gravação de reação (correlação de áudio) | `--a reacao.mp4 --b original.mp4 [--window 180]`; `offset_b_after_a` = `reacao_offset` |
| `react-plan.py` | linha do tempo do react (trecho → pausa → fala) e as regras: crédito, trecho ≤ 12 s, sua fala ≥ 60%, 2–4 pausas, 45–90 s; congela os quadros de pausa | `--spec react.json --public DIR [--max-trecho 12] [--min-share 0.6]`; exit 1 = corrija |
| `react-compose.py` | `react-plan.json` → `public/index.html` no layout do react (dividida em cima/embaixo → pausa → você em tela cheia) | `--plan --public [--orig-pos "50% 30%"] [--react-pos "50% 40%"]` |
| `broll-conform.py` | clipe de banco de imagens, clipe seu ou foto → cutaway **1080x1920**, 30 fps, sem áudio, BT.709 | `--in --out [--start] [--dur] [--push 1.08] [--grade] [--crop-x] [--vf FILTROS]` |
| `safe-area.mjs` | **área segura**: abre a composição no Chrome e confere que todo texto visível está em x 60–940, y 220–1500 | `--index [--step 0.25] [--at T,..] [--x0 --x1 --y0 --y1] [--json]`; sai com 1 se algo passar |
| `verify-render.py` | confere o **arquivo** renderizado: tamanho, 30 fps, H.264/AAC, BT.709, capa, abertura, preto, duração, A/V, palavras cortadas | `--render [--index] [--res 1080x1920] [--fps 30] [--words --kept] [--out]`; sai com 1 em FAIL |

## Etapa de corte (clipe bruto → corte plano vertical)

```bash
mkdir -p "$W/raw" "$W/public" "$W/snaps" renders && cp "<pasta>/<clipe>.MP4" "$W/raw/"
ffmpeg -y -v error -i "$W/raw/<clipe>.MP4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio-raw.wav"
npx hyperframes transcribe "$W/audio-raw.wav" -d "$W" --engine parakeet --language pt --json && mv "$W/transcript.json" "$W/transcript-raw.json"
auto-editor "$W/raw/<clipe>.MP4" --edit audio:-30dB --margin 0.12s,0.35s --export v1 -o "$W/speech.v1"
python3 "$SK/scripts/paper-cut.py" --transcript "$W/transcript-raw.json" --duration <segundos> --out-dir "$W" --speech "$W/speech.v1"
#   leia o PAPER-CUT.md (ponto A); corrija leituras erradas com hand-cut.py
python3 "$SK/scripts/tighten-cut.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --out "$W/cut-list.json"
python3 "$SK/scripts/sliver.py" --cut-list "$W/cut-list.json" --audio "$W/audio-raw.wav" --fix
python3 "$SK/scripts/edge-audit.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --transcript "$W/transcript-raw.json" --fix
python3 "$SK/scripts/edge-audit.py" --audio "$W/audio-raw.wav" --cut-list "$W/cut-list.json" --transcript "$W/transcript-raw.json"   # 0 problemas
python3 "$SK/scripts/apply-cut.py" --input "$W/raw/<clipe>.MP4" --cut-list "$W/cut-list.json" --out "$W/public/input-video.mp4" --size 1080x1920
ffmpeg -y -v error -i "$W/public/input-video.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio.wav"
npx hyperframes transcribe "$W/audio.wav" -d "$W" --engine parakeet --language pt --json    # transcript.json, no tempo do corte plano
python3 "$SK/scripts/dead-air.py" "$W" --plan
#   para cada faixa proposta: patch-cut.py --drop-flat A-B, edge-audit até 0, apply-cut, transcrever de novo,
#   e dead-air outra vez até imprimir 0 pausas
```

`<segundos>` vem de `ffprobe -v error -show_entries format=duration -of csv=p=0 <clipe>`.
Ordem em cada clipe: paper cut → ajustes à mão → tighten-cut → sliver → edge-audit até 0 → apply-cut → transcrever →
dead-air → patch-cut `--drop-flat` → edge-audit → apply-cut → transcrever → dead-air imprime 0.
`apply-cut.py --size 1080x1920` preenche o quadro vertical (escala até cobrir, depois recorta; nunca barras pretas). Fonte
horizontal: `--crop-x` escolhe a janela (0 esquerda, 0.5 centro, 1 direita). Se aparecer a linha `DRIFT`, não vista esse arquivo.

**Onde o paper-cut erra (corrija com hand-cut.py):** lista lida como recomeço ("velas, sabão, camisetas"); lousa falada; retake
com número errado; a mesma frase retomada várias vezes sem pausa (o Parakeet funde as tomadas: use `--keep` na última limpa);
mesma abertura com final diferente. Depois de cada apply, procure no texto plano a mesma sequência de 3 a 4 palavras duas
vezes em 7 s.

**Emendas:**
- Início de frase vem do Parakeet; **fim vem do áudio** (o Parakeet estica a última palavra para dentro da pausa).
- Confira toda emenda pelo áudio, sempre. Um resto de tomada descartada some do texto e toca como "certo. [to] Uma hora atrás".
- Um corte no vale de silêncio antes da última palavra de uma frase apaga essa palavra, e o edge-audit deixa passar. Depois
  de cada apply, compare a última palavra de cada trecho com a transcrição nova.
- Arquivos brutos acima de ~3 min: o Parakeet pode perder frases inteiras. Transcreva janelas de ~25 s cortadas nos
  silêncios do auto-editor, desloque os tempos de cada janela e junte.
- `cut-map.json` lista cada corte seco: ponha B-roll ou um empurrão de câmera nos cortes e vista no máximo um ou dois dos outros.

## Corte plano para vertical (quando já veio um corte pronto)

```bash
VIDEO="/caminho/corte.mp4"; mkdir -p "$W/public" "$W/snaps" renders
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,color_transfer -show_entries format=duration -of json "$VIDEO" > "$W/metadata.json"
ffmpeg -y -v error -i "$VIDEO" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio.wav"
npx hyperframes transcribe "$W/audio.wav" -d "$W" --engine parakeet --language pt --json
# re-encode em 1080x1920, 30 fps, quadro-chave a cada 30 (sem isso o render trava ao buscar), BT.709, AAC
ffmpeg -y -v error -i "$VIDEO" -map 0:v:0 -map 0:a:0 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1" -r 30 \
  -c:v libx264 -crf 16 -preset fast -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -movflags +faststart -c:a aac -b:a 256k -ar 48000 "$W/public/input-video.mp4"
```

## Rota React com pausa (formato 4.0 do ESTILO.md)

O que o usuário entrega: o vídeo original, a gravação de reação (ele assistindo, com o som do original no ar), **um arquivo
de fala por pausa** e os tempos das pausas. Se faltar a reação, peça; não improvise a caixa de cima.

```bash
mkdir -p "$W/raw" "$W/public" renders     # raw/original.mp4, raw/reacao.mp4, raw/fala-1.mp4 ... raw/fala-N.mp4
# 1. o original e a reação em 30 fps com quadro-chave denso (o original fica no tamanho dele; o layout recorta)
for f in original reacao; do ffmpeg -y -v error -i "$W/raw/$f.mp4" -r 30 -c:v libx264 -crf 16 -preset fast -g 30 -keyint_min 30 \
  -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -ar 48000 "$W/public/$f.mp4"; done
# 2. onde o original começa dentro da reação
python3 "$SK/scripts/sync-tracks.py" --a "$W/public/reacao.mp4" --b "$W/public/original.mp4"    # offset_b_after_a -> reacao_offset
# 3. cada fala passa pela Etapa de corte, com --size 1080x1920, saindo em public/fala-N.mp4
#    (transcrição com --engine parakeet --language pt; o paper-cut limpa retakes)
# 4. o original transcrito (para escolher as pausas e, se ele não tiver legenda própria, legendar a fala dele)
ffmpeg -y -v error -i "$W/public/original.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$W/audio-original.wav"
npx hyperframes transcribe "$W/audio-original.wav" -d "$W/original-tx" --engine parakeet --language pt --json
# 5. o plano (escreva react.json; veja o formato no topo de react-plan.py) e as regras
python3 "$SK/scripts/react-plan.py" --spec "$W/react.json" --public "$W/public"       # FAIL = corrija antes de seguir
# 6. a composição, depois as legendas da sua fala (legenda de destaque do ESTILO.md, palavra por palavra do transcript de cada fala,
#    deslocado pelo início da fala no plano), a legenda do original se ele não tiver, e o clique de pausa já vem pronto
python3 "$SK/scripts/react-compose.py" --plan "$W/react-plan.json" --public "$W/public"
# 7. daí em diante: Checagens, snapshots e render (abaixo), iguais a qualquer reel
```

- **Ponto A do react:** mostre `REACT-PLAN.md` (trechos, pausas, sua parte em %) e os quadros `pausa-N.png` antes de compor.
  Escolha as pausas no **final de uma frase** do original (pelo transcript), nunca no meio de uma palavra.
- **Ajuste de enquadramento:** `--orig-pos` move o original na metade de baixo (ex.: `"50% 20%"` sobe o rosto);
  `--react-pos` move você na caixa de cima: deixe **espaço acima da sua cabeça** para o título (y 236–370).
- **Normalize o volume** do original e das falas para a mesma altura (≈ −14 LUFS cada, `npx hyperframes normalize-audio`
  ou `loudnorm`) antes de compor: o original baixado costuma vir mais alto ou mais baixo que a sua voz.
- **Regras que o `react-plan.py` aplica** vêm do ESTILO.md 4.0: crédito na tela, trecho ≤ 12 s, sua fala ≥ 60%, 2 a 4
  pausas, 45 a 90 s. Não passe por cima de um FAIL: encurte o trecho ou fale mais.
- **No HyperFrames, todo `<video>` fica no nível de cima** da composição (nunca dentro de um `<div>` com `data-start`):
  o `react-compose.py` já faz assim e desenha a moldura como camada separada.
- Render de 33 s levou ~2 min aqui (CPU, sem GPU). Conte com ~3 a 6 min para um react de 60 a 90 s.

## Montagem vertical com o HyperFrames (sem `compose.py`)

O `compose.py` da versão do YouTube só trabalha em 1920x1080 e foi **removido**. A composição é escrita à mão em HTML, seguindo
as skills do HyperFrames. **Leia nesta ordem antes de escrever a primeira linha:**

1. `.claude/skills/hyperframes/SKILL.md` (contrato de render, ciclo de trabalho)
2. `.claude/skills/hyperframes/references/types/vertical.md` (9:16, primeiro segundo, ritmo)
3. `.claude/skills/hyperframes/references/captions.md` (legendas) e `overlays.md` (títulos e cartões)
4. `.claude/skills/hyperframes-registry/SKILL.md`: blocos prontos (legenda, transição, título animado) antes de construir à mão
5. `.claude/skills/media-use/SKILL.md`: **só o caminho grátis** (ver "Som")

Esqueleto (em `$W/public/index.html`; copie `$SK/assets/vendor/gsap.min.js` e `$SK/assets/fonts/*.woff2` para `public/`):

```html
<meta name="viewport" content="width=1080, height=1920">
<script src="gsap.min.js"></script>
<div id="stage" data-composition-id="<projeto>" data-start="0" data-duration="D"
     data-fps="30" data-width="1080" data-height="1920">
  <video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true"
         data-start="0" data-duration="D" data-track-index="1"></video>
  <div id="t01" class="clip" data-start="0.3" data-duration="2.8" data-track-index="3">Título em português</div>
  <audio id="musica" src="audio/trilha.mp3" data-start="0" data-duration="D" data-track-index="10" data-volume="0.12"></audio>
</div>
<script>window.__timelines = window.__timelines || {}; const tl = gsap.timeline({ paused: true });
  /* animações */ window.__timelines["<projeto>"] = tl;</script>
```

`<video>` dentro do `#stage` com tamanho 1080x1920. GSAP **local** (`gsap.min.js` na pasta `public/`), não pelo CDN: o primeiro
render não deve depender de internet. Todo `<audio>` precisa de `id`, ou fica mudo no render e toca no preview.

### Regras do texto e da legenda

O *visual* (cores, fonte, tamanho, posição, quantas palavras, animação, câmera, ritmo) vem **só do ESTILO.md**. Aqui ficam
os limites técnicos que valem sempre:

- **Tudo em português do Brasil**, com acento e cedilha corretos, `R$ 1.200,50`, `12%`, vírgula decimal. Nada de inglês na
  tela, exceto nome de marca ou ferramenta como se escreve.
- **Legenda palavra por palavra a partir de `transcript.json`** (tempos exatos), só nas palavras mantidas. Confira a
  ortografia contra o que foi dito; o ASR erra nome próprio.
- **Área segura (obrigatória): x 60 a 940, y 220 a 1500**, para todo *texto*: títulos, legendas, números, selos. Fica fora
  dela só textura e decoração, e marque com `data-safe-ignore`. Largura útil de um bloco de texto: **880 px**. Se o ESTILO.md
  trouxer outros quatro números, passe-os a `safe-area.mjs` (`--x0 --x1 --y0 --y1`).
- **Nada de texto menor que 28 px.** Corte palavras, não encolha a fonte.
- **Fontes só as de `assets/fonts/` que tenham os glifos do português** (Montserrat). **A DM Sans que veio do kit antigo não tem
  acentos nem `%`, `$`, `?`, `!`: não use.** Copie os `.woff2` para `public/fonts/` e declare com `@font-face`; nunca pelo CDN.
- Texto sobre vídeo claro precisa de contraste (o `check` reprova abaixo de 3:1): sombra, painel ou gradiente conforme o ESTILO.md.
  O rosto nunca fica debaixo de um texto ou cartão.
- Entradas e saídas: sem quique, sem giro 3D, desfoque não anima; durações e eases conforme o ESTILO.md.

### B-roll

Gravações suas são o melhor cutaway. Banco de imagens **gratuito** (Pexels ou Pixabay; confira a licença da página de cada
clipe). Passe tudo por `broll-conform.py --in clipe --out "$W/public/broll/x.mp4" --dur 2.5`: sai em 1080x1920, 30 fps, sem
áudio. Corte para o B-roll **na frase**, 1 a 3 s por plano. Registre no `plano.md` de onde veio cada clipe e a licença.
Nada de logo ou marca registrada de terceiros sem permissão do usuário.

## Som (só grátis)

**Quanto e onde pôr som, e em que volume, está no ESTILO.md (seção 3.7).** Aqui ficam só as fontes e a técnica de mixagem.
Um efeito sonoro só entra se um objeto na tela fizer aquele barulho.

**Fontes permitidas, e só estas:**
1. **Biblioteca do HyperFrames**: `npx hyperframes skills update media-use` instala 19 efeitos em `.claude/skills/media-use/audio/assets/sfx/`
   (typing, click, pop, ping, notification, chime e outros; licença Pixabay Content License, sem atribuição).
2. **Pixabay** (pixabay.com/music e /sound-effects): Pixabay Content License. Baixe o arquivo e guarde o link da página.
3. **YouTube Audio Library** (YouTube Studio): baixa-se manualmente pelo usuário; **confira em cada faixa se exige
   atribuição** e, se exigir, ponha o crédito na legenda do post (anote no `plano.md`).

**Nunca** use Epidemic Sound, Artlist, HeyGen/geração paga de áudio, nem música de artista, nem trilha de outro vídeo. Se o usuário
pedir uma faixa que não é grátis, avise e ofereça a alternativa. Guarde em `$W/public/audio/` e liste fonte, link e licença no `plano.md`.

**Mixagem:** normalize cada arquivo de efeito para -3 dBFS de pico (leia `max_volume` com `ffmpeg -i x.mp3 -af volumedetect -f null -`)
e use `data-volume` só para a mistura. Alinhe o pico audível, não o início do arquivo.
**Música** (só se o ESTILO.md permitir): nível e tipo conforme o ESTILO.md, com fade de entrada e saída. Voz em torno de
**-14 LUFS**, pico real abaixo de -1 dBTP (confira com `ebur128`). Para abaixar
a música quando a voz fala, num master pronto (mantenha uma cópia sem música):

```bash
ffmpeg -i master.mp4 -stream_loop -1 -i trilha.mp3 -filter_complex \
 "[0:a]asplit=2[voice][sc];[1:a]volume=-16dB,afade=t=in:d=1[bed];[bed][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest master-musica.mp4
```

## Checagens, snapshots e render

```bash
# 1. conferir a composição (a trava de área segura do HyperFrames é mais estreita: desligue-a e use a nossa)
npx hyperframes check "$W/public" --safe-zone off
node "$SK/scripts/safe-area.mjs" --index "$W/public/index.html"          # x 60–940, y 220–1500; exit 1 = corrija
# 2. Ponto B: uma imagem por momento de texto, e leia os PNGs
npx hyperframes snapshot "$W/public" --at 0,0.5,1,2,3,<tempos dos momentos>      # opções: npx hyperframes snapshot --help
# 3. render vertical, 30 fps, CRF 16 (H.264 + AAC)
NODE_OPTIONS=--max-old-space-size=8192 npx hyperframes render "$W/public" --resolution portrait --fps 30 --crf 16 -o "$W/raw-render.mp4"
# 4. etiquetas BT.709 completas (o render sai "unknown" e o QuickTime/Instagram mostram a cor errada). Sem perda.
ffmpeg -y -v error -i "$W/raw-render.mp4" -c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -color_range tv -movflags +write_colr+faststart "renders/<projeto>.mp4"
# 5. conferir o ARQUIVO (exit 1 = não entregue)
python3 "$SK/scripts/verify-render.py" --render "renders/<projeto>.mp4" --index "$W/public/index.html" --out "$W/check/VERIFY.md"
```

- `--resolution portrait` renderiza 1080x1920 sem escalar uma composição que já é 1080x1920. Se a composição tiver outro
  tamanho, **corrija a composição**, não o render.
- Se o render pintar trechos de preto, repita com `--workers 1`.
- `verify-render.py` escreve `VERIFY.md`, `render-sheet.png` e **`capa.png`** em `$W/check/`. Olhe `capa.png` e `render-sheet.png`
  (primeiro quadro, segundos 1 a 3, cada momento de texto, último quadro) antes de entregar. **Palavras cortadas:** transcreva o
  áudio do render (`--language pt`) e passe `--words <esse.json> --kept "$W/transcript.json"`.
- Movimento em quadros contíguos: `ffmpeg -i renders/<projeto>.mp4 -vf "select='between(n,A,B)',scale=270:480,tile=6x4" -frames:v 1 tira.png`
  em cada janela de transição; procure salto-e-arrasto, parada seca ou um quadro que "pula".
- Sincronia labial em corte longo: um quadro plano bate com a fonte perto de `src_start + x` dentro de um quadro.

## Entrega

- **O MP4 final é `renders/<nome do projeto>.mp4`** (na raiz do projeto, pasta `renders/`). Só ele vai para lá; `VERIFY.md`,
  `capa.png`, `plano.md` e `PAPER-CUT.md` ficam em `$W/`.
- Confira com `md5sum` que o arquivo entregue é o renderizado + remux; não o passe por download de chat (um ida e volta
  hospedado pode alterar o arquivo).
- **Relate** o caminho, o que foi adicionado e onde, e **suas próprias dúvidas** (um texto parado tempo demais, uma palavra
  perdida na camiseta, um corte escondido sob o B-roll, uma regra do ESTILO.md que venceu uma regra daqui). Versões seguem
  numeradas (`<projeto>-v2.mp4` só se o usuário pedir para manter as duas). Notas voltam em palavras simples; nada é travado.
- Retemporizar um desenho aprovado para um corte novo do mesmo conteúdo é a edição mais barata: copie a `public/`, transcreva
  de novo, mova cada `data-start` e tempo da timeline para as palavras novas, tire snapshots, renderize.

## Armadilhas que fazem perder um render

- **Parakeet ausente** (`models install parakeet` falha por rede): pare e avise; não troque de motor sem o usuário pedir.
- **CDN bloqueado**: use sempre o `gsap.min.js` local; fontes pelo `@font-face` apontando para `fonts/*.woff2` copiados.
- **`check` reprova contraste** em texto sobre vídeo claro (abaixo de 3:1): ponha painel escuro translúcido atrás do texto.
- **Texto em português some acento**: confirme que a fonte tem os glifos (ã õ ç é ê á í ó ú) olhando o snapshot.
- **O render sai com etiquetas de cor "unknown"**: sempre o remux BT.709 do passo 4.
- **Vídeo congela ao buscar**: o arquivo de entrada precisa de quadro-chave a cada 30 quadros (os dois caminhos acima já fazem).
- **`<audio>` sem `id`** fica mudo no render.
- **Duração**: `data-duration` da composição = duração do vídeo de entrada; `verify-render.py` reprova diferença acima de um quadro.

## Mantendo a skill sua

- **"Salva isso na skill":** escreva a nota como uma regra simples na seção a que pertence. Se ela muda o *visual ou o
  tom*, a casa certa é o **`ESTILO.md`** (que vence tudo), não este arquivo. Quando uma regra nova contradiz uma antiga,
  troque a antiga; nunca deixe as duas.
- Depois de cada entrega: nota em palavras simples → ajuste o momento (um número) ou a regra → rebuild → snapshot → render.
- Um resultado de que o usuário gostou vira um bloco reutilizável: guarde o HTML em `$SK/assets/blocos/` e descreva em uma linha.
- Rotina de passada cabe num modelo médio; um formato novo, ou algo que este arquivo não cobre, merece o modelo mais forte.
  Os tokens vão para snapshots e saída de ferramentas: um snapshot por momento, scripts em vez de redigitar.
