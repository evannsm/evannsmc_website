#!/bin/bash
# Strip /index.html from project listing card hrefs so links are clean directory URLs.
TARGET="${QUARTO_PROJECT_OUTPUT_DIR:-docs}/projects/index.html"
if [ -f "$TARGET" ]; then
    sed -i 's|href="\.\./projects/\([^/"]*\)/index\.html"|href="../projects/\1/"|g' "$TARGET"
fi
