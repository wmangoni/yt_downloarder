# 🎥 YouTube Downloader GUI

Uma aplicação de desktop simples e intuitiva construída com Python e Tkinter para baixar vídeos, áudios e legendas do YouTube. Este downloader foca na simplicidade de uso, permitindo que você obtenha rapidamente o conteúdo desejado do YouTube em seu formato favorito.

## ✨ Funcionalidades

* **Interface Gráfica (GUI):** Fácil de usar, baseada em Tkinter.
* **Download de Vídeo:** Baixa vídeos do YouTube na menor resolução disponível (ótimo para visualização rápida ou conversão posterior).
* **Extração de Áudio:** Converte automaticamente o áudio do vídeo baixado para o formato MP3.
* **Download de Legendas:** Baixa legendas disponíveis em Português (Brasil) e Inglês (se houver) como arquivos de texto simples.
* **Seleção de Pasta de Destino:** Escolha facilmente onde salvar seus downloads.
* **Barra de Progresso:** Acompanhe o progresso do download e da conversão em tempo real.
* **Processamento em Segundo Plano:** O download e a conversão são executados em uma thread separada para manter a interface responsiva.

## 🚀 Como Usar

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema.

Você precisará instalar as seguintes bibliotecas Python:

```bash
pip install pytubefix moviepy
```

### Observação para moviepy:

A biblioteca moviepy utiliza o ffmpeg para manipulação de áudio e vídeo. Você precisará ter o ffmpeg instalado em seu sistema e acessível no PATH.

No Windows: Baixe a versão mais recente do ffmpeg em ffmpeg.org e adicione o diretório bin ao seu PATH do sistema.
No macOS (com Homebrew): brew install ffmpeg
No Linux (Ubuntu/Debian): sudo apt update && sudo apt install ffmpeg
Executando a Aplicação
Clone o repositório (ou baixe o arquivo main.py):

Bash

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git) # Altere para o seu link
cd seu-repositorio # Altere para o nome da sua pasta
```
Se você apenas baixou o arquivo, navegue até a pasta onde ele está salvo.

Execute o script Python:

Bash

```bash
python main.py
```

### Guia Rápido da Interface
**URL do Vídeo:** Cole a URL do vídeo do YouTube que você deseja baixar.
Salvar em: Clique em "Escolher Pasta..." para selecionar o diretório onde o vídeo, áudio e legendas serão salvos. Por padrão, será criada uma pasta downloads no diretório do script.
**Baixar Conteúdo:** Clique neste botão para iniciar o processo de download e conversão.
**Progresso:** A barra e o texto de progresso mostrarão o status atual da operação.
**Status:** Mensagens informativas sobre o que a aplicação está fazendo no momento.

### 📂 Estrutura de Saída

Quando você baixa um vídeo, a aplicação criará a seguinte estrutura de pastas no diretório de saída que você escolher:
```
seu_diretorio_de_saida/
├── videos/
│   └── Nome Do Video.mp4
├── audios/
│   └── Nome Do Video.mp3
└── captions/
    ├── Nome Do Video_pt_caption.txt (ou .srt se alterado)
    └── Nome Do Video_en_caption.txt (ou .srt se alterado)
```

### ⚠️ Tratamento de Erros

A aplicação possui tratamento básico de erros para problemas comuns como URLs inválidas ou falhas de conexão. Se ocorrer um erro, uma mensagem de aviso aparecerá e o status será atualizado.

### 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver ideias para melhorias, novas funcionalidades ou encontrar bugs, sinta-se à vontade para:

Abrir uma Issue para relatar um bug ou sugerir uma funcionalidade.
Criar um Pull Request com suas alterações.
