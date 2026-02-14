#!/usr/bin/env bash
set -o errexit

# Arka planda hızlıca bir port açarak Render'ın servisi kapatmasını engelleyelim
python -m http.server $PORT & 

# ComfyUI'ı başlat (Biraz gecikmeli başlayabilir, sorun değil)
python main.py --cpu --listen 0.0.0.0 --port 10001
