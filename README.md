# Scripts de Download e Processamento de Vídeos

Este conjunto de scripts Python automatiza o download e processamento de vídeos conforme especificações fornecidas.

## 📋 Pré-requisitos

### Software Necessário
- **Python 3.7+**
- **FFmpeg** (para processamento de vídeo)

### Instalação do FFmpeg

#### Windows
1. Baixe o FFmpeg de: https://ffmpeg.org/download.html
2. Extraia e adicione ao PATH do sistema

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install ffmpeg
```

#### CentOS/RHEL
```bash
sudo yum install ffmpeg
```

## 🚀 Instalação e Uso

### Usando UV (Recomendado)

#### 1. Executar Todos os Scripts
```bash
uv run run_all.py
```

#### 2. Executar Scripts Individuais
```bash
uv run download_choke1.py
uv run download_choke2.py
uv run download_street.py
uv run download_sidewalk.py
uv run download_bengal.py
uv run download_terminal1.py
uv run download_terminal2.py
uv run download_terminal3.py
uv run download_terminal4.py
uv run download_shibuya.py
```

### Usando Python tradicional

#### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

#### 2. Executar Scripts
```bash
python run_all.py
python download_choke1.py  # Para scripts individuais
```

## 📁 Estrutura de Arquivos

```
├── video_utils.py          # Funções utilitárias
├── run_all.py              # Script para executar todos
├── download_choke1.py      # Script para Choke1
├── download_choke2.py      # Script para Choke2
├── download_street.py      # Script para Street
├── download_sidewalk.py    # Script para Sidewalk
├── download_bengal.py      # Script para Bengal
├── download_terminal1.py   # Script para Terminal1
├── download_terminal2.py   # Script para Terminal2
├── download_terminal3.py   # Script para Terminal3
├── download_terminal4.py   # Script para Terminal4
├── download_shibuya.py     # Script para Shibuya
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🎯 Vídeos Processados

### Pasta "IJCB Videos"
- **Choke1.mkv** - Concatenação de P2E_S5_C1.2, P2E_S5_C1.1, P2E_S5_C1.3
- **Choke2.mkv** - Concatenação de P2L_S5_C1.2, P2L_S5_C1.1, P2L_S5_C1.3
- **Street.mkv** - YouTube (30 FPS, frames 0-2041)
- **Sidewalk.mkv** - YouTube (24 FPS, frames 140-1436, apenas frames pares)
- **Bengal.mkv** - YouTube (25 FPS, frames 8475-9474)
- **Shibuya.mkv** - YouTube (25 FPS, 4K, 00:04:50-00:05:20)

### Pasta "T-BIOM Videos"
- **Terminal1.mkv** - YouTube (30 FPS, frames 2400-4740)
- **Terminal2.mkv** - YouTube (30 FPS, 00:23:37-00:24:52)
- **Terminal3.mkv** - YouTube (30 FPS, 00:19:49-00:20:15)
- **Terminal4.mkv** - YouTube (30 FPS, 00:06:45-00:07:21)

## 🔧 Funcionalidades

### video_utils.py
- **create_directory()** - Cria diretórios necessários
- **download_file()** - Download de arquivos com progresso
- **extract_tar_xz()** - Extração de arquivos compactados
- **concatenate_videos()** - Concatenação de múltiplos vídeos
- **convert_to_h264_mkv()** - Conversão para H.264 MKV
- **download_youtube_video()** - Download de vídeos do YouTube
- **cut_video_by_frames()** - Corte por número de frames
- **cut_video_by_time()** - Corte por tempo
- **keep_even_frames()** - Mantém apenas frames pares
- **cleanup_temp_files()** - Limpeza de arquivos temporários

## 📊 Características dos Scripts

### Downloads do Zenodo (Choke1 e Choke2)
- Download automático de arquivos .tar.xz
- Extração automática
- Concatenação na ordem específica
- Conversão para H.264 MKV

### Downloads do YouTube
- Resolução automática (1080p ou melhor disponível)
- Controle de FPS específico
- Corte por frames ou tempo
- Filtros especiais (frames pares para Sidewalk)

### Processamento de Vídeo
- Codec H.264 para compatibilidade
- Container MKV
- Qualidade otimizada (CRF 23)
- Áudio AAC quando necessário

## 🛠️ Solução de Problemas

### Erro "FFmpeg não encontrado"
- Certifique-se de que o FFmpeg está instalado e no PATH

### Erro de download do YouTube
- Verifique sua conexão com a internet
- Alguns vídeos podem ter restrições geográficas

### Erro de espaço em disco
- Certifique-se de ter espaço suficiente (vários GB)
- Os arquivos temporários são limpos automaticamente

### Erro de permissão
- Execute com permissões adequadas
- No Linux/macOS: `chmod +x *.py`

## 📝 Notas Importantes

1. **Espaço em Disco**: Os processos requerem espaço significativo para arquivos temporários
2. **Tempo de Processamento**: Dependendo da velocidade da internet e CPU, pode levar várias horas
3. **Qualidade**: Todos os vídeos são processados com qualidade otimizada
4. **Limpeza**: Arquivos temporários são automaticamente removidos após processamento

## 🤝 Suporte

Se encontrar problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que o FFmpeg está funcionando: `ffmpeg -version`
3. Execute os scripts individualmente para identificar problemas específicos
4. Verifique os logs de erro para mais detalhes