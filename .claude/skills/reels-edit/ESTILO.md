# ESTILO.md — o meu estilo para os Reels

> **Fonte única do meu estilo.** A skill `reels-edit` lê este arquivo **antes de qualquer edição**, e o que está aqui
> **vence qualquer outra regra** (SKILL.md, scripts, skills do HyperFrames). O SKILL.md cuida da *técnica* (corte, render,
> checagens); tudo que é *gosto* mora só aqui.
>
> **De onde saiu este rascunho:** de 4 vídeos de referência que você mandou (R1 a R4, descritos na seção 8). Foi medido
> o que dá para medir em pixels e em áudio; o resto foi lido a olho. Regras marcadas **[em 4 de 4]** ou **[em 3 de 4]**
> aparecem na maioria das referências; **[em 1 de 4]** é opção, não regra. Tudo que está marcado **[confirmar]** é
> minha inferência: corrija ao ler. Onde uma frase diz "minha leitura" é interpretação, não fato.

---

## 1. O meu estilo em uma frase

**Eu falo direto para a câmera, num lugar real, sem cortes bonitos: a pessoa é o vídeo, e o texto na tela é uma única
ideia simples, limpa e fora do meu rosto.**

---

## 2. Princípios (o porquê de cada regra)

1. **A pessoa é o conteúdo.** Rosto e voz seguram o vídeo; o resto só ajuda. *Porquê:* em 3 das 4 referências não há corte
   nenhum em 31 a 70 s: quem assiste fica pela pessoa, não pela edição.
2. **Uma ideia por vídeo, dita já no primeiro quadro.** O título entra com o vídeo, não depois. *Porquê:* o quadro 0 vira a
   capa e é a decisão de ficar ou deslizar; nas referências R1 e R2 o texto já está na tela no quadro 0.
3. **O texto nunca cobre o rosto.** Título e cartão ficam acima da cabeça, legenda fica no peito/abaixo do queixo.
   *Porquê:* tapar o rosto tira a única coisa que prende. [em 4 de 4]
4. **Simples parece de verdade.** Letra sem caixa, sem contorno pesado, sem efeito (R1, R3), ou um elemento que imita o
   próprio Instagram (R2) ou um selo amarelo único (R4). *Porquê:* quanto menos "produzido", mais confiança.
5. **Lugar real, luz natural.** Piscina, varanda, sala. Nada de fundo de estúdio ou tela verde. *Porquê:* contexto conta
   a história sem texto. [em 4 de 4, minha leitura]
6. **Funciona sem som.** O texto de abertura diz a promessa sozinho; a legenda acompanha a fala. *Porquê:* muita gente assiste mudo.
7. **Silêncio é o padrão no som.** Voz limpa e alta; música e efeitos só se merecerem lugar. *Porquê:* nenhuma
   referência tem efeito sonoro audível na análise; a voz carrega tudo [confirmar: não consegui ouvir, só medir].
8. **Português do Brasil coloquial, escrito como se fala.** "Tudo pra você é sobre dinheiro?", não "Tudo para você
   consiste em dinheiro?". *Porquê:* é a voz de quem fala; a legenda tem que ser a mesma voz.
9. **Um ritmo só por vídeo.** Ou é take contínuo (sem cortes), ou é cortado com B-roll a cada poucos segundos (R4). Nunca
   um meio-termo de cortes aleatórios. *Porquê:* mudar de ritmo no meio parece erro.
10. **O que a plataforma esconde, eu não uso.** Tudo dentro da área segura (x 60–940, y 220–1500). *Porquê:* botões, nome e
    legenda do post cobrem o resto.

---

## 3. O visual

### 3.1 Cores (com o código)

Amostradas dos pixels das referências. Três cores, e só.

| Papel | Código | De onde veio |
|---|---|---|
| Texto principal (título e legenda) | **`#FFFFFF`** branco puro | R1, R3, R4 |
| Destaque / selo / moldura | **`#FCCD02`** amarelo | R4 (moldura e selo medidos em `#FBCD01`–`#FCCD02`) |
| Painel escuro (cabeçalho de cartão, fundo de selo) | **`#21272D`** | R2 (cabeçalho do cartão de pergunta, medido) |
| Cartão claro | **`#FFFFFF`** com texto `#21272D` | R2 |

Regras: o texto é branco, **o amarelo é a única cor de destaque**, e vale só para **uma palavra-chave por legenda** ou
para o selo/moldura (R4). Nada de gradiente, neon ou mais de uma cor de destaque no mesmo vídeo.
Sobre fundo claro (céu, parede branca), o texto branco precisa de **sombra suave** (`0 2px 12px rgba(0,0,0,.35)`) ou de
um painel `#21272D` atrás, para passar de 3:1 de contraste.

### 3.2 Fontes livres

Tudo aqui é licença SIL OFL (livre, uso comercial permitido) e **os arquivos já estão em `assets/fonts/`**, funcionam
offline e têm acento e cedilha:

| Uso | Fonte | Arquivo |
|---|---|---|
| Título de abertura e legenda (padrão) | **Montserrat** 800, caixa alta no título | `montserrat-latin-800-normal.woff2` |
| Título mais forte (opcional) | Montserrat 900 | `montserrat-latin-900-normal.woff2` |
| Legenda estilo R4 (itálico pesado) | Montserrat 800/900 itálico | `montserrat-latin-800-italic.woff2`, `...-900-italic.woff2` |
| Texto corrido de cartão | Montserrat 700 | `montserrat-latin-700-normal.woff2` |

**Não use DM Sans** (veio no kit do YouTube): o arquivo incluído **não tem acentos nem `%`, `$`, `?`, `!`**. Verificado.
Uma família só por vídeo. Se quiser outra fonte, ela precisa ter os glifos `ã õ ç é ê á í ó ú à â ô` e `R$ %` conferidos.

### 3.3 Título de abertura

- **Onde:** acima da cabeça, centrado, **duas linhas** no máximo. Eixo vertical: **centro em y ≈ 460** (R1 mediu 24% da altura;
  em 1080x1920 isso dá y 393–528). Largura: **~68% da tela (≈ 730 px)**, ou seja, `x 170–900`; nunca passa de 880 px.
- **Quanto:** **até 5 palavras por linha, 2 linhas, ~30 caracteres no total.** (R1: "NEM TODA AMIZADE / VALE À PENA"; 2 linhas de 16 e 13 caracteres.)
- **Tamanho:** **60 px** (de 56 a 66), Montserrat 800, **caixa alta**, entrelinha 1.15, centralizado. Branco `#FFFFFF`, **sem
  caixa e sem contorno**; sombra suave só se o fundo for claro.
- **Quando:** **já no quadro 0** e **fica o vídeo inteiro** (R1: 70 s com o mesmo título; R2: 31 s com o mesmo cartão). Sem
  animação de saída. Se animar, só uma entrada de 0,4 s (`opacity` + `y` de 40 px, `power2.out`) nos primeiros 0,3 s.
- **O que diz:** a ideia do vídeo como afirmação ou pergunta, no tom de fala. Não é título de capa de YouTube.

### 3.4 Legenda

Duas famílias nas referências; escolha **uma por vídeo**:

| | **Legenda limpa** (R3) [em 1 de 4, padrão para opinião/conselho] | **Legenda de destaque** (R4) [em 1 de 4, para tutorial/humor] |
|---|---|---|
| Palavras por vez | **1 a 3** (média ~2; frases quebram em "dela." / "seguir quem" / "ela quiser,") | **2 a 4** |
| Caixa | **sentence case**, com pontuação, igual à fala | **CAIXA ALTA** |
| Fonte | Montserrat 800, **58 px** | Montserrat 900 itálico, **60 px**, contorno preto 4 px |
| Cor | branco `#FFFFFF` | branco `#FFFFFF`, **uma palavra em amarelo `#FCCD02`** |
| Posição | **centro em y ≈ 1170** (R3: 61% da altura), sobre o peito/tronco, **abaixo do queixo** | **centro em y ≈ 1350**, sobre o B-roll |
| Limites | `x 60–940` (largura útil 880 px), 1 linha | idem, 1 linha, nunca 2 |
| Sincronia | palavra por palavra a partir da transcrição, trocas rápidas | idem |

- **Sempre dentro da área segura:** `x 60–940`, `y 220–1500`. A referência R4 põe a legenda a ~78% da altura (≈ y 1500 em
  1080x1920), no limite: **eu subo para y ≈ 1350** para ficar dentro da área.
- **Nunca mais de 4 palavras** por vez, nunca duas linhas, nunca menos de 28 px.
- **Acento e pontuação corretos.** Nome próprio e marca como se escrevem. Palavrão: **mascarado com `#`** como em R4
  (`F#DA-SE`) [confirmar se você usa palavrão].
- **Marca d'água:** só um @ pequeno e discreto (R3: handle cinza claro a ~40% de opacidade sobre a roupa); nunca logo grande.

### 3.5 Câmera e enquadramento

- **Vertical 9:16, câmera na mão ou tripé; a pessoa olha para a lente.** [em 4 de 4]
- **Rosto no terço superior-médio**, olhos entre **25% e 40%** da altura; deixa espaço em cima para o título. Cabeça nunca cortada.
- **Plano fechado a médio** (do peito para cima, ou meio corpo sentado). Mão na frente da câmera é ok (R1 apoia as mãos na
  borda da piscina).
- **Movimento é o da mão.** Sem zoom digital animado, sem balanço falso. Zoom só por necessidade de enquadrar e **no máximo 8%** [confirmar].
- **Gravar em vertical, com luz natural.** A fonte pode ser 4K; a saída é 1080x1920.

### 3.6 Ritmo

- **Take contínuo (padrão):** **zero cortes visíveis** em 3 de 4 referências (31, 64 e 70 s). Só se cortam retakes,
  respirações longas e pausas acima de **0,40 s** (o `dead-air.py` já faz isso) e **sem pulo de enquadramento**.
- **Com B-roll (R4):** troca de plano a **cada 3 a 5 s**, sempre **na frase** que o plano ilustra; o apresentador fica fixo
  no terço de cima.
- **Duração:** de **30 a 70 s** para fala direta (R1 70 s, R2 31 s, R3 64 s); até **~110 s** para tutorial com B-roll (R4).
  Gancho nos primeiros **1 a 3 s**: ou o título já na tela, ou a pessoa entrando em quadro (R1 abre com ele chegando à
  borda da piscina).
- **Fala:** ritmo de conversa, com pausa curta antes da frase de impacto. Pausa longa fica no corte final.

### 3.7 Som

- **Voz sempre limpa, em ~ −14 LUFS** (as 4 referências ficam entre **−14,1 e −14,9 LUFS**), pico real abaixo de −1 dBTP
  (a R3 estoura, +0,6 dBFS: evite).
- **Sem música por padrão.** Em R3 o chão de ruído é praticamente digital (−82 dB entre falas): sem trilha. Nas outras, a
  análise mede só ambiente de sala (−47 a −52 dB nos trechos mais quietos); **não consegui ouvir**, então "sem música" é
  leitura dos números [confirmar ouvindo].
- Se usar música: **instrumental, baixa**, entre −18 e −20 dB abaixo da voz, de fontes **grátis** (HyperFrames, Pixabay,
  YouTube Audio Library; veja o SKILL.md).
- **Efeito sonoro só se um objeto na tela fizer aquele barulho** (digitar, clicar, ping de notificação). Nunca whoosh em texto.
- **Sem eco, sem voz robótica.** Corta respiração alta e estalo de boca.

---

## 4. Os formatos de vídeo e a receita de cada um

Os quatro primeiros saem diretamente das referências; **História** e **Lista** não aparecem nelas: são o mesmo estilo
aplicado a outro conteúdo, e ficam **[a confirmar]** até você mandar um exemplo.

### 4.1 Opinião / conselho (fala direta com título fixo): R1 e R3
**Quando:** uma ideia forte dita direto, sem demonstrar nada. 30 a 70 s.
1. **Título fixo** de 2 linhas acima da cabeça, no quadro 0 (3.3). (R3 usa legenda palavra a palavra no lugar do título.)
2. **Take contínuo**, sem B-roll. Legenda limpa (3.4) se o som tiver que funcionar mudo.
3. **Estrutura da fala:** frase-promessa (o próprio título) → o porquê em 2 a 3 frases → uma frase de fechamento curta.
4. **Cortes:** só retake, pausa > 0,4 s e gagueira. Nenhum corte de pulo.
5. **Sem música.** Fecha na última palavra, com um respiro de 0,3 s no fim.

### 4.2 Resposta a pergunta (cartão no topo): R2
**Quando:** responder uma pergunta de seguidor. 25 a 45 s.
1. **Cartão de pergunta** no topo, estilo caixa de perguntas do Instagram: cabeçalho `#21272D` com "O QUE VOCÊ QUER SABER?"
   (caixa alta, pequeno, branco) e corpo branco com a pergunta em `#21272D`. Medido em R2: largura ~**710 px** (65%), `x 185–895`;
   **posicione com `y ≥ 220`** (R2 começa em y ≈ 205, fora da área segura). Cantos arredondados de 14 px.
2. **Fica na tela o vídeo todo.** Rosto abaixo do cartão, olhando para a lente, câmera na mão.
3. **A fala** repete o ponto da pergunta na primeira frase ("Tudo pra você é sobre dinheiro? Não.") e responde em 2 a 4 ideias.
4. **Sem legenda** quando o cartão já traz a pergunta e o áudio é claro; com legenda limpa se for gravar em lugar barulhento.
5. **Sem música.**

### 4.3 Tutorial / receita / reação com B-roll: R4
**Quando:** mostrar como se faz algo, ou reagir a um vídeo. 60 a 110 s.
1. **Apresentador em cima**, ocupando **~1/3 da altura** (≈ 640 px em 1080x1920), com **moldura amarela `#FCCD02` de 8 px** (12 px em 1080 de largura).
2. **Selo amarelo** (pílula `#FCCD02` com texto escuro, 28 a 32 px) sobre a borda inferior da moldura, com o @ do perfil. Texto: "Siga ... nas redes sociais".
3. **Abaixo**, o **B-roll em tela cheia vertical** (receita, demonstração, reação), com **legenda de destaque** (3.4) em cima.
4. **Plano muda a cada 3 a 5 s**, sempre na frase que ele ilustra. O apresentador continua reagindo no quadro de cima.
5. **Dentro da área segura:** a moldura amarela é decoração e pode encostar na borda; o *texto* (selo e legenda) fica em `y 220–1500` (R4 deixa o selo em y ≈ 410 de 1280, ou ≈ 615 em 1920; confira).
6. **Música:** só se for tutorial calmo (instrumental, baixa). Humor/reação: só voz.

### 4.4 História (relato pessoal) [a confirmar]
Mesmo molde de 4.1: take contínuo, título de 2 linhas com o **desfecho ou a pergunta** ("Eu quase perdi tudo aos 25"),
legenda limpa, sem B-roll; **a promessa do título é paga antes do fim**. Se tiver foto ou vídeo de apoio, entra como
B-roll de 1 a 3 s na frase, nunca cobrindo o rosto por mais de 3 s.

### 4.5 Lista (n dicas) [a confirmar]
Mesmo molde de 4.1 com o número no título ("3 ERROS QUE EU COMETI AO VENDER"). **Cada item entra com uma palavra-chave
de destaque** (legenda de destaque, 3.4, só nessa palavra). Itens de 8 a 15 s, sempre na mesma ordem e no mesmo lugar;
**nunca mais de 5 itens**. Sem lista animada com ícones.

---

## 5. O que eu NUNCA faço

Cada item vem de algo que **não aparece em nenhuma** das 4 referências ou que as quatro evitam [confirmar os marcados com ✱].

1. **Nunca texto sobre o rosto.**
2. **Nunca texto fora da área segura** (`x 60–940`, `y 220–1500`) nem menor que 28 px.
3. **Nunca mais de 4 palavras** de legenda por vez, nunca legenda de 2 linhas.
4. **Nunca mais de uma cor de destaque** por vídeo (o amarelo `#FCCD02`), nunca neon, gradiente ou contorno colorido.
5. **Nunca emoji** na tela (não há nenhum nas referências) ✱.
6. **Nunca transição vistosa**: sem giro, glitch, whoosh, zoom-twirl, wipe. Corte seco ou nada.
7. **Nunca efeito sonoro em texto**; nunca trilha que atrapalha a voz; nunca música com direitos (só as fontes grátis).
8. **Nunca 4K, nunca horizontal, nunca barras pretas laterais** (o B-roll preenche o quadro 9:16; R4 tem barras: **eu não deixo**) ✱.
9. **Nunca inglês na tela** (exceto marca/ferramenta como se escreve).
10. **Nunca corte de pulo no take contínuo**: ou o vídeo é contínuo, ou é montado com B-roll (princípio 9).
11. **Nunca logo ou marca d'água grande**; no máximo um @ discreto ✱.
12. **Nunca fundo de estúdio ou tela verde** ✱.
13. **Nunca começar com tela preta, logo ou câmera assentando**: o quadro 0 é uma imagem com sentido (a capa).
14. **Nunca título que entra depois dos 3 primeiros segundos.**
15. **Nunca palavrão sem máscara** (`F#DA-SE`) ✱ [confirmar se você usa].
16. **Nunca texto de um vídeo diferente do que foi dito** (legenda com a palavra errada); a legenda é conferida contra o áudio.

---

## 6. Como a skill usa este arquivo

- **Lê tudo antes de editar.** Se um valor daqui conflita com o SKILL.md, vale o valor daqui.
- **Escolha de formato:** a skill pergunta (ou deduz do pedido) qual formato da seção 4 vale e **segue a receita**.
- **Valores numéricos** (px, cores, palavras por legenda) vêm das seções 3.1 a 3.7. Se um valor estiver como **[confirmar]**, a skill
  usa e **avisa na entrega** que foi um palpite.
- **Área segura:** `x 60–940`, `y 220–1500`, conferida por `scripts/safe-area.mjs` em todo render.

---

## 7. Notas (cresce a cada vídeo)

> **Como escrever uma nota:** depois de cada vídeo, uma linha: data, nome do projeto, o que você pediu para mudar ou o que
> funcionou, e a regra resultante. Quando uma nota vira regra, mova-a para a seção certa (3, 4 ou 5) e **apague a antiga**;
> nunca deixe duas regras que se contradizem. Diga "salva isso no ESTILO" e a skill escreve aqui.

| Data | Vídeo | Nota | Virou regra em |
|---|---|---|---|
| 2026-11-24 | (criação) | Rascunho feito a partir de 4 referências (R1–R4). Fonte DM Sans do kit antigo não tem acentos: trocada por Montserrat (OFL). | 3.2 |
| 2026-11-24 | (criação) | R4 deixa barras pretas nas laterais do B-roll e legenda em y≈1500; no meu estilo o B-roll preenche e a legenda sobe para y≈1350. | 3.4, 5 |
| | | | |

**Pendências para confirmar com você:**
- [ ] O estilo é mesmo "fala direta, sem corte" ou você também quer o modelo com B-roll (R4)?
- [ ] Usa palavrão? Se sim, mascara com `#` como R4?
- [ ] Usa música em algum formato? Qual?
- [ ] Formatos **História** e **Lista**: manda um exemplo de cada.
- [ ] Amarelo `#FCCD02` como cor de destaque é seu, ou prefere outra?
- [ ] Zoom: pode empurrar 8% na frase de impacto?

---

## 8. Referências usadas (para não perder o rastro)

Quatro vídeos 720x1280 (baixados do Instagram, então a resolução e o bitrate **não** dizem nada sobre o original).

| | O que é | Duração | Texto na tela | Cortes | Loudness |
|---|---|---|---|---|---|
| **R1** | Homem na piscina, fala direta, câmera na mão | 70 s | título fixo, 2 linhas, branco, caixa alta, y 262–352 de 1280 | 0 | −14,2 LUFS |
| **R2** | Homem de óculos escuros na varanda, responde pergunta | 31 s | cartão de pergunta do Instagram, fixo, `#21272D` e branco | 0 | −14,2 LUFS |
| **R3** | Homem sentado no sofá com um cachorro, câmera fixa | 64 s | legenda palavra a palavra, branco, 1 a 3 palavras, y≈61% | 0 | −14,9 LUFS |
| **R4** | Apresentador com fone reage a uma receita em B-roll | 108 s | moldura e selo amarelos, legenda em caixa alta com palavra em amarelo, y≈78% | B-roll a cada 3–5 s | −14,1 LUFS |

O que **não** foi medido: fala por minuto (o Parakeet não está instalado aqui), nome exato das fontes (identificadas a olho:
sans geométrica bold) e o conteúdo de música (a análise só vê níveis, não ouve).
