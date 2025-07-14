#!/usr/bin/env python3
"""
Script para baixar e processar Choke1
"""

import os
import tempfile
from video_utils import *


def main():
    # Configurações
    url = "https://zenodo.org/record/815657/files/P2E_S5.tar.xz"
    file_name = url.split("/")[-1]
    output_dir = "IJCB Videos"
    final_name = "Choke1.mkv"
    video_fps = 30

    create_directory(output_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Diretório temporário criado: {temp_dir}")
        tar_file_main = os.path.join(temp_dir, file_name)
        # download_file(url, tar_file_main)
        print(f"Conteúdo de {temp_dir} após download: {os.listdir(temp_dir)}")

        print(f"Extraindo arquivo principal: {tar_file_main} para {temp_dir}")
        extract_tar_xz(tar_file_main, temp_dir)
        print(f"Conteúdo de {temp_dir} após 1ª extração: {os.listdir(temp_dir)}")

        nested_tar_files = []
        for item in os.listdir(temp_dir):
            if item.endswith(".tar.xz") and item != file_name:
                nested_tar_files.append(os.path.join(temp_dir, item))

        if not nested_tar_files:
            print(f"Erro: Nenhum arquivo 'P2E_S5_C#.tar.xz' aninhado encontrado em {temp_dir}.")
            return

        temp_video_parts = []

        nested_tar_files.sort()
        print(f"Arquivos .tar.xz aninhados encontrados (e ordenados): {nested_tar_files}")

        for nested_tar_path in nested_tar_files:

            old_list_dir = os.listdir(temp_dir)

            extract_tar_xz(nested_tar_path, temp_dir)

            folder = [y for y in os.listdir(temp_dir) if y not in old_list_dir][0]

            if folder is None:
                print("Erro: pasta não extraída corretamente")
                return

            final_image_folder_path = os.path.join(temp_dir, folder)
            part_index = len(temp_video_parts) + 1
            temp_part_video_name = f"choke1pt{part_index}.mkv"
            temp_part_video_path = os.path.join(temp_dir, temp_part_video_name)

            # Converte as imagens desta parte para um vídeo temporário
            print(f"Convertendo imagens de {final_image_folder_path} para vídeo temporário: {temp_part_video_path}")
            frames_list = os.path.join(final_image_folder_path, "all_file.txt")
            if images_to_video(input_folder=final_image_folder_path,
                               output_path=temp_part_video_path,
                               fps=video_fps,
                               pattern="%8d.jpg"):
                temp_video_parts.append(temp_part_video_path)
                print(f"Vídeo temporário criado: {temp_part_video_path}")
            else:
                print(f"Não foi possível criar vídeo. Pulando esta parte.")

        if not temp_video_parts or len(temp_video_parts) != len(nested_tar_files):
            print("Erro: Nem todas as partes de vídeo temporárias foram criadas com sucesso.")
            print(f"Esperado {len(nested_tar_files)} partes, encontrado {len(temp_video_parts)}.")
            return

        print(f"Conteúdo de {temp_dir} após criação dos vídeos temporários: {os.listdir(temp_dir)}")
        print(f"Partes de vídeo temporárias para concatenação (ordenadas): {temp_video_parts}")

        # 7. Juntar as 3 partes dos vídeos em um único arquivo final
        # A lista `temp_video_parts` já está na ordem correta devido ao `nested_tar_files.sort()`
        # e a adição sequencial.
        final_concatenated_temp_video = os.path.join(temp_dir, "concatenated_raw.mkv")
        concatenate_videos(temp_video_parts, final_concatenated_temp_video)
        print(f"Conteúdo de {temp_dir} após concatenação: {os.listdir(temp_dir)}")

        # 8. Converter para H.264 MKV (se necessário, ou para garantir o formato final)
        # Se os vídeos temporários já são H.264 MKV, esta etapa pode ser otimizada
        # mas mantê-la garante o formato final desejado.
        final_output_path = os.path.join(output_dir, final_name)
        convert_to_h264_mkv(final_concatenated_temp_video, final_output_path)
        print(f"Processo concluído! Arquivo salvo em: {final_output_path}")

        # O `tempfile.TemporaryDirectory()` já cuida da limpeza automática no final
        # Não é necessário chamar `cleanup_temp_files` explicitamente para o temp_dir
        # No entanto, se você tivesse outros arquivos temporários criados fora de temp_dir, usaria.


if __name__ == "__main__":
    main()