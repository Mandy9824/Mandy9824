#!/bin/bash
# Maakt robotmaaierkompas-child.zip om te uploaden via Weergave > Thema's > Nieuw thema > Thema uploaden.
# Vereist: hoofdthema Twenty Twenty-Five is geïnstalleerd (standaard in WordPress).
set -e
cd "$(dirname "$0")/../wp-content/themes"
OUT="$(cd ../.. && pwd)/robotmaaierkompas-child.zip"
rm -f "$OUT"
zip -qr "$OUT" robotmaaierkompas-child -x '*.DS_Store' 'robotmaaierkompas-child/robotmaaierkompas/patterns-bron/*'
echo "Gemaakt: $OUT ($(du -h "$OUT" | cut -f1))"
