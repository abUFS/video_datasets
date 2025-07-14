#!/usr/bin/env python3
"""
Script para baixar e processar Choke2
"""

import os
import tempfile
from video_utils import *

def main():
    # Configurações
    url = "https://zenodo.org/record/815657/files/P2L_S5.tar.xz"
    output_dir = "IJCB Videos"
    final_name = "Choke2.mkv"
    
    # Criar diretório de saída
    create_directory(output_dir)
    
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        # Baixar arquivo
        tar_file = os.path.join(temp_dir, "P2L_S5.tar.xz")
        download_file(url, tar_file)
        
        # Extrair arquivo
        extract_tar_xz(tar_file, temp_dir)
        
        # Encontrar arquivos extraídos
        video_files = [
            os.path.join(temp_dir, "P2L_S5_C1.2"),
            os.path.join(temp_dir, "P2L_S5_C1.1"),
            os.path.join(temp_dir, "P2L_S5_C1.3")
        ]
        
        # Verificar se os arquivos existem
        for video in video_files:
            if not os.path.exists(video):
                print(f"Erro: Arquivo não encontrado: {video}")
                return
        
        # Concatenar vídeos
        temp_concat = os.path.join(temp_dir, "concatenated.mkv")
        concatenate_videos(video_files, temp_concat)
        
        # Converter para H.264 MKV
        final_path = os.path.join(output_dir, final_name)
        convert_to_h264_mkv(temp_concat, final_path)
        
        print(f"Processo concluído! Arquivo salvo em: {final_path}")

if __name__ == "__main__":
    main()