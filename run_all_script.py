#!/usr/bin/env python3
"""
Script para executar todos os downloads de vídeos
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name):
    """Executa um script Python e captura o resultado"""
    print(f"\n{'='*60}")
    print(f"Executando: {script_name}")
    print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Avisos:", result.stderr)
        print(f"✅ {script_name} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script_name}:")
        print(f"Código de saída: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Arquivo {script_name} não encontrado!")
        return False

def main():
    """Função principal"""
    scripts = [
        "download_choke1.py",
        "download_choke2.py",
        "download_street.py",
        "download_sidewalk.py",
        "download_bengal.py",
        "download_terminal1.py",
        "download_terminal2.py",
        "download_terminal3.py",
        "download_terminal4.py",
        "download_shibuya.py"
    ]
    
    print("🎬 Iniciando download e processamento de todos os vídeos...")
    print(f"Total de scripts: {len(scripts)}")
    print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar se todos os scripts existem
    missing_scripts = [script for script in scripts if not os.path.exists(script)]
    if missing_scripts:
        print(f"❌ Scripts não encontrados: {missing_scripts}")
        return
    
    # Verificar se video_utils.py existe
    if not os.path.exists("video_utils.py"):
        print("❌ Arquivo video_utils.py não encontrado!")
        return
    
    successful = 0
    failed = 0
    
    for script in scripts:
        if run_script(script):
            successful += 1
        else:
            failed += 1
            print(f"⚠️  Continuando com os próximos scripts...")
    
    print(f"\n{'='*60}")
    print("📊 RELATÓRIO FINAL")
    print(f"{'='*60}")
    print(f"Scripts executados: {len(scripts)}")
    print(f"✅ Sucessos: {successful}")
    print(f"❌ Falhas: {failed}")
    print(f"Concluído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed > 0:
        print(f"\n⚠️  {failed} script(s) falharam. Verifique os logs acima.")
    else:
        print(f"\n🎉 Todos os scripts foram executados com sucesso!")

if __name__ == "__main__":
    main()