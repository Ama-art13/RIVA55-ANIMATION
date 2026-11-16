# Crivel · carosello Instagram animato

Storytelling animato dell'etichetta **Crivel** di Riva55: Massimo, viticoltore (e ingegnere), con l'imbuto in testa che ha la forma della sua riva più significativa, il Crivel. Vino bianco frizzante col fondo.

9 slide video, 1080×1350 (4:5), 30 fps.

| # | Slide |
|---|-------|
| 01 | Cosa ci fa un imbuto in testa a un viticoltore? |
| 02 | Massimo è un viticoltore. |
| 03 | E anche ingegnere. |
| 04 | Il vino è sempre nei suoi pensieri. |
| 05 | Quell'imbuto è il Crivel. |
| 06 | La vigna dà il nome al vino. |
| 07 | Rifermentato col fondo. |
| 08 | Verticale. Sapido. Fresco. |
| 09 | Un viticoltore, un territorio, una riva, un vino. |

## Struttura

- `sorgente/Crivel.ai`: etichetta originale (Illustrator).
- `livelli/`: livelli trasparenti ricavati dall'etichetta (scena, imbuto, lettering, descrizione, firma) in PNG ad alta risoluzione e WebP.
- `anteprima/src.html`: animazioni e testi di tutte le slide (sorgente da modificare).
- `anteprima/crivel-carosello.html`: anteprima navigabile autonoma, con le immagini incluse. Si apre in qualsiasi browser.
- `video/`: gli MP4 finali, da caricare in ordine su Instagram.
- `video/storia/`: versione verticale 9:16 (1080×1920) per le storie: tutto unito (66,5 s) e diviso in due parti sotto i 60 s.
- `script/`: strumenti per rigenerare tutto.

## Rigenerare

Servono Python 3 con Pillow e numpy, poppler-utils, Node con Playwright (Chromium) e ffmpeg.

```sh
# 1. etichetta → immagine ad alta risoluzione → livelli
mkdir -p build
pdftoppm -r 600 -png -x 1100 -y 2100 -W 2700 -H 2800 sorgente/Crivel.ai build/hi
python3 script/cut_livelli.py .

# 2. anteprima HTML con le immagini incluse
python3 script/build.py .

# 3. fotogrammi di controllo (slide indice 0–8, secondo)
node script/shots.js . '[[0,6.4],[8,7.9]]'

# 4. video finali in video/
node script/render.js .        # tutte le slide
node script/render.js . 8      # solo la slide 8 (anche "2,8")

# 5. versione storie 9:16 in video/storia/
script/storia.sh
```

I testi si cambiano in `anteprima/src.html`: ogni slide è un blocco `SLIDES.push({...})` con durata, costruzione e animazione. Dopo una modifica, rilanciare i passi 2 e 4.
