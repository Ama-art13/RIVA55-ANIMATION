#!/usr/bin/env bash
# Unisce le clip 4:5 di video/ in video verticali 9:16 (1080x1920) per le storie IG.
# Sopra e sotto prolunga la carta del video stesso, così non si vede la giunta.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p video/storia
mk(){ out=$1; shift; args=(); fc=""; n=0
  for i in "$@"; do args+=(-i "video/crivel-0$i.mp4"); fc+="[$n:v]"; n=$((n+1)); done
  ffmpeg -y -v error "${args[@]}" -filter_complex "${fc}concat=n=$n:v=1:a=0[c];[c]split=3[m][a][b];[a]crop=1080:58:0:0,split=5[a1][a2][a3][a4][a5];[a1][a2][a3][a4][a5]vstack=5[top];[b]crop=1080:56:0:1294,split=5[b1][b2][b3][b4][b5];[b1][b2][b3][b4][b5]vstack=5[bot];[top][m][bot]vstack=3,format=yuv420p[v]" \
    -map "[v]" -c:v libx264 -preset slow -crf 17 -r 30 -movflags +faststart "$out"
  echo "$out"; }
mk video/storia/crivel-storia.mp4 1 2 3 4 5 6 7 8 9
mk video/storia/crivel-storia-parte1.mp4 1 2 3 4 5
mk video/storia/crivel-storia-parte2.mp4 6 7 8 9
