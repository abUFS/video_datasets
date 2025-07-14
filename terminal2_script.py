#!/usr/bin/env python3
"""
Script para baixar e processar Terminal2
"""

import os
import tempfile
from video_utils import *

def main():
    # Configurações
    url = "https://www.youtube.com/watch?v=SqZWZTu1veA"
    output_dir = "T-BIOM Videos"
    final_name = "Terminal2.mkv"
    start_time = "00:23:37"
    end_time = "00:24:52"
    
    # Criar diretório de saída
    create_directory(output_dir)
    
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        # Baixar vídeo do YouTube
        temp_video = os.path.join(temp_dir, "terminal2_temp.%(ext)s")
        download_youtube_video(url, temp_video, fps=30, resolution='1080p')
        
        # Encontrar arquivo baixado
        downloaded_file = get_video_extension(temp_video.replace('.%(ext)s', ''))
        
        # Cortar vídeo por tempo
        temp_cut = os.path.join(temp_dir, "terminal2_cut.mkv")
        cut_video_by_time(downloaded_file, temp_cut, start_time, end_time)
        
        # Converter para H.264 MKV
        final_path = os.path.join(output_dir, final_name)
        convert_to_h264_mkv(temp_cut, final_path)
        
        print(f"Processo concluído! Arquivo salvo em: {final_path}")

if __name__ == "__main__":
    main()