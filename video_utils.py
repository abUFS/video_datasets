import os
import subprocess
import requests
import tarfile
import tempfile
from pathlib import Path
import yt_dlp
from tqdm import tqdm
import re # Importa a biblioteca de expressões regulares

def _run_ffmpeg_command(cmd):
    """Função auxiliar para executar comandos FFmpeg com tratamento de erros."""
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando FFmpeg: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise # Re-lança a exceção para que o chamador possa tratá-la

def create_directory(path):
    """Cria diretório se não existir"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"Diretório criado/verificado: {path}")

def download_file(url, filename):
    """Baixa arquivo com barra de progresso"""
    print(f"Baixando {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

    print(f"Download concluído: {filename}")

def extract_tar_xz(tar_path, extract_to):
    """Extrai arquivo tar.xz"""
    print(f"Extraindo {tar_path}...")
    with tarfile.open(tar_path, 'r:xz') as tar:
        tar.extractall(path=extract_to)
    print(f"Extração concluída em: {extract_to}")

def concatenate_videos(video_files, output_file):
    """Concatena vídeos usando FFmpeg"""
    print(f"Concatenando vídeos: {video_files}")

    # Cria arquivo de lista temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for video in video_files:
            f.write(f"file '{os.path.abspath(video)}'\n")
        list_file = f.name

    try:
        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file,
            '-c', 'copy', output_file, '-y'
        ]
        _run_ffmpeg_command(cmd) # Usa a função auxiliar
        print(f"Concatenação concluída: {output_file}")
    finally:
        os.unlink(list_file)

def convert_to_h264_mkv(input_file, output_file):
    """Converte vídeo para H.264 MKV"""
    print(f"Convertendo {input_file} para H.264 MKV...")
    cmd = [
        'ffmpeg', '-i', input_file,
        '-c:v', 'libx264', '-c:a', 'aac',
        '-preset', 'medium', '-crf', '23',
        output_file, '-y'
    ]
    _run_ffmpeg_command(cmd) # Usa a função auxiliar
    print(f"Conversão concluída: {output_file}")

def download_youtube_video(url, output_path, fps=None, resolution=None):
    """Baixa vídeo do YouTube com configurações específicas"""
    print(f"Baixando vídeo do YouTube: {url}")

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }

    # Configurar filtros de formato baseado na resolução
    if resolution == '4K':
        ydl_opts['format'] = 'best[height<=2160]'
    elif resolution == '1080p':
        ydl_opts['format'] = 'best[height<=1080]/best[height<1080]'

    # Configurar FPS se especificado
    if fps:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Download do YouTube concluído")

def cut_video_by_frames(input_file, output_file, start_frame, end_frame, fps=30):
    """Corta vídeo por frames"""
    print(f"Cortando vídeo por frames: {start_frame} a {end_frame}")

    start_time = start_frame / fps
    end_time = end_frame / fps
    duration = end_time - start_time

    cmd = [
        'ffmpeg', '-i', input_file,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        output_file, '-y'
    ]
    _run_ffmpeg_command(cmd) # Usa a função auxiliar
    print(f"Corte por frames concluído: {output_file}")

def cut_video_by_time(input_file, output_file, start_time, end_time):
    """Corta vídeo por tempo"""
    print(f"Cortando vídeo por tempo: {start_time} a {end_time}")

    cmd = [
        'ffmpeg', '-i', input_file,
        '-ss', start_time,
        '-to', end_time,
        '-c', 'copy',
        output_file, '-y'
    ]
    _run_ffmpeg_command(cmd) # Usa a função auxiliar
    print(f"Corte por tempo concluído: {output_file}")

def keep_even_frames(input_file, output_file):
    """Mantém apenas frames pares"""
    print(f"Mantendo apenas frames pares...")

    cmd = [
        'ffmpeg', '-i', input_file,
        '-vf', 'select=not(mod(n\\,2))',
        '-c:v', 'libx264', '-c:a', 'aac',
        output_file, '-y'
    ]
    _run_ffmpeg_command(cmd) # Usa a função auxiliar
    print(f"Filtro de frames pares concluído: {output_file}")

def cleanup_temp_files(*files):
    """Remove arquivos temporários"""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Arquivo temporário removido: {file}")

def get_video_extension(filename):
    """Retorna a extensão do vídeo baixado"""
    possible_extensions = ['.mp4', '.mkv', '.webm', '.avi']
    base_name = os.path.splitext(filename)[0]

    for ext in possible_extensions:
        if os.path.exists(base_name + ext):
            return base_name + ext

    return filename  # Retorna o nome original se não encontrar


def images_to_video(input_folder, output_path, fps, pattern):
    """
    Converte uma sequência de imagens em um vídeo MKV com codificação H.264

    Args:
        input_folder (str): Caminho da pasta contendo as imagens
        output_path (str): Caminho de saída do arquivo MKV
        fps (int/float): Taxa de quadros por segundo
        pattern (str): Padrão dos nomes dos arquivos (ex: %08d.jpg, frame_%04d.png)

    Returns:
        bool: True se a conversão foi bem-sucedida, False caso contrário
    """

    # Verifica se a pasta de entrada existe
    if not os.path.exists(input_folder):
        print(f"Erro: A pasta '{input_folder}' não existe.")
        return False

    # Cria o diretório de saída se não existir
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Constrói o caminho completo do padrão
    input_pattern = os.path.join(input_folder, pattern)

    # Comando FFmpeg
    cmd = [
        'ffmpeg',
        '-y',  # Sobrescreve arquivo de saída se existir
        '-f', 'image2',  # Especifica o formato de entrada como image2
        '-r', str(fps),  # Taxa de quadros
        '-i', input_pattern,  # Padrão dos arquivos de entrada
        '-c:v', 'libx264',  # Codec de vídeo H.264
        '-pix_fmt', 'yuv420p',  # Formato de pixel para compatibilidade
        '-crf', '23',  # Qualidade (0-51, onde 23 é boa qualidade)
        '-preset', 'medium',  # Preset de velocidade/qualidade
        output_path
    ]

    try:
        print(f"Convertendo imagens de '{input_folder}' para '{output_path}'...")
        print(f"Padrão: {pattern}, FPS: {fps}")

        # Executa o comando FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        print("Conversão concluída com sucesso!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Erro durante a conversão:")
        print(f"Código de saída: {e.returncode}")
        print(f"Erro: {e.stderr}")
        return False

    except FileNotFoundError:
        print("Erro: FFmpeg não encontrado. Certifique-se de que está instalado e no PATH.")
        return False

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False