# CONTINUAR — editor de Reels (estado em 2026-11-24)

Branch: `claude/beautiful-dirac-r8ximd` (tudo commitado e enviado). Abra uma conversa nova: as skills carregam no início.

## Pronto
- **Skill `reels-edit`** em `.claude/skills/reels-edit/` (adaptada da `youtube-edit` do kit WeAreNoCode):
  - Saída 1080x1920, 30 fps, H.264 + AAC, BT.709, entrega em `renders/<projeto>.mp4`.
  - Português do Brasil: transcrição `--engine parakeet --language pt`; o corte de retakes entende "corta isso", "de novo" etc.
  - Área segura x 60–940, y 220–1500, conferida por `scripts/safe-area.mjs`.
  - `verify-render.py` confere tamanho, fps, codecs, cor, capa (quadro 0, exporta `capa.png`) e movimento nos 3 primeiros s.
  - Montagem com as skills do HyperFrames (`compose.py` removido; ele só fazia 1920x1080).
  - Música e efeitos só grátis (biblioteca do HyperFrames, Pixabay, YouTube Audio Library).
  - **React com pausa**: `react-plan.py` (linha do tempo e regras), `react-compose.py` (composição), `sync-tracks.py`
    (sincroniza a sua reação com o original; sinal do offset corrigido). Testado com vídeo sintético até o MP4.
  - Seção "Economia de processo" no `SKILL.md`.
  - **Modo horizontal** (1920x1080, fps da gravação até 60, área x 96–1824 / y 54–950) quando pedido ou quando a gravação é horizontal: `formato.py`.
  - 37 testes passando: `cd .claude/skills/reels-edit/scripts && python3 -m unittest tests`.
- **`DIRECAO.md`** em `.claude/skills/reels-edit/DIRECAO.md`: direção criativa e processo em 4 etapas com aprovação (vale para todo vídeo).
- **`ESTILO.md`** em `.claude/skills/reels-edit/ESTILO.md`: fonte única do estilo (vence qualquer regra). Tem posicionamento,
  princípios, cores, fontes, título, legenda, câmera, ritmo, som, formatos com receita (4.0 React é o carro-chefe),
  ganchos de exemplo, lista do "nunca" e a seção Notas.
- **Fontes**: Montserrat (OFL) em `assets/fonts/`, com acentos. A DM Sans do kit **não tem acentos**: não usar.
- **Instalado no container**: HyperFrames 0.9.89 (projeto), 6 skills do HyperFrames, auto-editor, yt-dlp, GSAP local.
  Num container novo, reinstale: `npm install` e `pip install auto-editor yt-dlp fonttools brotli`.

## Decisões tomadas
- Perfil **pessoal** (aproveitar o público atual).
- Tema: relacionamento homem/mulher, polêmico; ângulo **"verdade incômoda para os dois lados"**.
- Critica comportamento, nunca o grupo (regra da Meta); nunca expor anônimo ou menor de idade.
- React: **começa em tela dividida** (você em cima com moldura amarela `#FCCD02`, original embaixo), **pausa** (congela,
  escurece, ícone, clique) e **você em tela cheia**; crédito "@autor · vídeo original" sempre na tela; trecho ≤ 12 s;
  sua fala ≥ 60%; 2 a 4 pausas; 45 a 90 s.
- Usa **palavrão** na fala; na legenda vai mascarado com `#` (padrão; ainda a confirmar).
- Economia: não reler arquivos, não repetir testes/renders à toa, imagens pequenas, respostas curtas, sem baixar qualidade.

## Falta (em ordem)
1. **Instalar o Parakeet** (`npx hyperframes models install parakeet`). Aqui falha porque o host `huggingface.co` está
   bloqueado na rede do ambiente: libere o host nas configurações do ambiente, ou rode na sua máquina. Sem ele não há legenda automática.
2. **Confirmar pendências do `ESTILO.md`** (seção 7): palavrão mascarado na legenda; amarelo `#FCCD02` como destaque;
   zoom de 8% na frase de impacto; usa música em algum formato?; exemplos de História e Lista.
3. **Primeiro react real**: mandar `original.mp4`, `reacao.mp4` (você assistindo, som do original numa caixa de som),
   `fala-1.mp4 … fala-N.mp4` e os pontos de pausa (ex.: 0:09, 0:21, 0:30).
4. Revisar o primeiro react (ponto A: `REACT-PLAN.md` + quadros de pausa; ponto B: snapshots) e salvar as notas no `ESTILO.md`.
5. Primeiro vídeo solo (formato 4.1 ou 4.2).
6. Opcional: atualizar `docs/WeAreNoCode-YouTube-Editor/` (ainda fala de YouTube); abrir PR quando quiser juntar ao `main`.

## Próximo passo
Na aba nova: **"Continua do CONTINUAR.md"**. Depois, resolva o item 1 (Parakeet) e mande os arquivos do primeiro react (item 3).
