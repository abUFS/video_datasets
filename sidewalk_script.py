#!/usr/bin/env python3
"""
Script para baixar e processar Sidewalk
"""

import os
import tempfile
from video_utils import *

def main():
    # Configurações
    url = "https://www.youtube.com/watch?v=UgUC_IY7rMw"
    output_dir = "IJCB Videos"
    final_name = "Sidewalk.mkv"
    fps = 24
    start_frame = 140
    end_frame = 1436
    
    # Criar diretório de saída
    create_directory(output_dir)
    
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        # Baixar vídeo do YouTube
        temp_video = os.path.join(temp_dir, "sidewalk_temp.%(ext)s")
        download_youtube_video(url, temp_video, fps=fps, resolution='1080p')
        
        # Encontrar arquivo baixado
        downloaded_file = get_video_extension(temp_video.replace('.%(ext)s', ''))
        
        # Cortar vídeo por frames
        temp_cut = os.path.join(temp_dir, "sidewalk_cut.mkv")
        cut_video_by_frames(downloaded_file, temp_cut, start_frame, end_frame, fps)
        
        # Manter apenas frames pares
        temp_even = os.path.join(temp_dir, "sidewalk_even.mkv")
        keep_even_frames(temp_cut, temp_even)
        
        # Converter para H.264 MKV
        final_path = os.path.join(output_dir, final_name)
        convert_to_h264_mkv(temp_even, final_path)
        
        print(f"Processo concluído! Arquivo salvo em: {final_path}")

if __name__ == "__main__":
    main()