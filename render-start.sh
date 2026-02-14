#!/usr/bin/env bash
# Hata oluşursa betiği durdur
set -o errexit

# ComfyUI'yi CPU modunda, dışarıya açık ve Render'ın atadığı portta başlat
python main.py --cpu --listen 0.0.0.0 --port ${PORT:-10000}
