#!/bin/zsh
# Прави тапети от твоите снимки: изрязва до 1920x1080, затъмнява леко, намалява ярките цветове, добавя
# тъмно избледняване отдолу (за лентата с приложения) и лек вињет. Резултатът отива в my-theme/wallpapers/.
#
#   ./process-photos.sh                 # обработва всичко от my-photos/
#   ./process-photos.sh 0.62 0.9        # по-тъмно: яркост 62%, наситеност 90% (по подразбиране 70 и 92)
set -euo pipefail
cd "$(dirname "$0")"
BRIGHT=${1:-0.70}; SAT=${2:-0.92}
IN=my-photos; OUT=my-theme/wallpapers; TMP=$(mktemp -d)
mkdir -p "$OUT"
[ -f "$OUT/captions.txt" ] && grep -v "^50-photo-" "$OUT/captions.txt" > "$TMP/cap" && cp "$TMP/cap" "$OUT/captions.txt"
cat > "$TMP/overlay.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs>
<linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".30"/><stop offset=".30" stop-color="#000" stop-opacity="0"/>
<stop offset=".55" stop-color="#000" stop-opacity=".30"/><stop offset=".78" stop-color="#000" stop-opacity=".72"/><stop offset="1" stop-color="#000" stop-opacity=".95"/></linearGradient>
<radialGradient id="r" cx=".5" cy=".45" r=".8"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient></defs>
<rect width="1920" height="1080" fill="url(#r)"/><rect width="1920" height="1080" fill="url(#v)"/></svg>
SVG
rsvg-convert "$TMP/overlay.svg" -o "$TMP/overlay.png"
n=0
setopt null_glob
for f in "$IN"/*.{jpg,jpeg,png,heic,JPG,JPEG,PNG,HEIC}; do
  n=$((n+1)); base=$(basename "${f%.*}" | tr -c 'A-Za-z0-9\n' '-' | sed 's/--*/-/g;s/-$//')
  out="$OUT/50-photo-$base.jpg"
  magick "$f" -auto-orient -resize 1920x1080^ -gravity center -extent 1920x1080 \
    -modulate $(printf '%.0f,%.0f,100' $(echo "$BRIGHT*100" | bc) $(echo "$SAT*100" | bc)) \
    "$TMP/overlay.png" -compose over -composite -strip -sampling-factor 4:2:0 -interlace Plane "$TMP/x.png"
  for q in 86 82 78 74 70 66; do magick "$TMP/x.png" -quality $q "$out"; [ $(stat -f %z "$out") -lt 290000 ] && break; done
  echo "$(basename "$out")  $(( $(stat -f %z "$out") / 1024 )) KB"
done
rm -rf "$TMP"
echo "$n снимки обработени -> $OUT"
