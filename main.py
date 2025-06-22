import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pytubefix import YouTube
from moviepy import VideoFileClip

class YouTubeDownloaderApp:
    """
    Uma aplicação com interface gráfica (GUI) para baixar vídeos,
    áudios e legendas do YouTube.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Estilo para os widgets
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Helvetica', 11))
        self.style.configure('TButton', font=('Helvetica', 11, 'bold'), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 11))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Status.TLabel', font=('Helvetica', 10, 'italic'))

        # Variáveis
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        
        self.create_widgets()

    def create_widgets(self):
        """Cria e posiciona todos os widgets na janela principal."""
        
        main_frame = ttk.Frame(self.root, padding="15 15 15 15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Seção de URL ---
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)

        ttk.Label(url_frame, text="URL do Vídeo:").pack(side=tk.LEFT, padx=(0, 10))
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var)
        self.url_entry.pack(fill=tk.X, expand=True)

        # --- Seção do Caminho de Saída ---
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=10)

        ttk.Label(path_frame, text="Salvar em:").pack(side=tk.LEFT, padx=(0, 10))
        path_entry = ttk.Entry(path_frame, textvariable=self.output_path_var, state='readonly')
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.browse_button = ttk.Button(path_frame, text="Escolher Pasta...", command=self.select_output_path)
        self.browse_button.pack(side=tk.LEFT)

        # --- Botão de Download ---
        self.download_button = ttk.Button(main_frame, text="Baixar Conteúdo", command=self.start_download_thread)
        self.download_button.pack(fill=tk.X, pady=15, ipady=5)

        # --- Seção de Status e Progresso ---
        status_frame = ttk.Frame(main_frame, padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        status_frame.config(style='Card.TFrame', relief='solid', borderwidth=1)
        
        ttk.Label(status_frame, text="Progresso:", font=('Helvetica', 11, 'bold')).pack(anchor='w')

        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(status_frame, text="0%", font=('Helvetica', 10))
        self.progress_label.pack(anchor='center')

        self.status_label = ttk.Label(status_frame, text="Aguardando URL...", style='Status.TLabel', wraplength=550)
        self.status_label.pack(anchor='w', pady=(15, 0))

    def select_output_path(self):
        """Abre uma caixa de diálogo para selecionar a pasta de destino."""
        path = filedialog.askdirectory(title="Selecione a pasta para salvar os arquivos")
        if path:
            self.output_path_var.set(path)
            self.update_status(f"Arquivos serão salvos em: {path}")

    def start_download_thread(self):
        """Inicia o processo de download em uma thread separada para não travar a GUI."""
        url = self.url_var.get()
        if not url:
            messagebox.showwarning("URL Vazia", "Por favor, insira uma URL do YouTube.")
            return

        # Desabilita o botão para evitar cliques múltiplos
        self.download_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.progress_label['text'] = "0%"

        # Inicia a thread
        download_thread = threading.Thread(target=self.download_logic, args=(url,))
        download_thread.daemon = True
        download_thread.start()

    def download_logic(self, url):
        """
        Contém a lógica de download do pytubefix e conversão do moviepy.
        Executado em uma thread separada.
        """
        try:
            base_output_path = self.output_path_var.get()

            # Cria as subpastas se não existirem
            video_output_path = os.path.join(base_output_path, "videos")
            audio_output_path = os.path.join(base_output_path, "audios")
            captions_output_path = os.path.join(base_output_path, "captions")
            os.makedirs(video_output_path, exist_ok=True)
            os.makedirs(audio_output_path, exist_ok=True)
            os.makedirs(captions_output_path, exist_ok=True)

            self.update_status("Conectando ao YouTube...")
            yt = YouTube(url, on_progress_callback=self.on_progress)
            
            # Sanitiza o título para criar um nome de arquivo válido
            safe_title = "".join(c for c in yt.title if c.isalnum() or c in (' ', '-', '_')).rstrip()

            # 1. Baixar o vídeo de menor resolução
            self.update_status(f"Baixando vídeo: {yt.title}...")
            video_stream = yt.streams.get_lowest_resolution()
            video_path = video_stream.download(output_path=video_output_path, filename=f"{safe_title}.mp4")
            
            # 2. Baixar as legendas
            if hasattr(yt, 'captions'):
                self.update_status("Procurando legendas...")
                for lang_code in ['a.pt', 'a.en']: # Português e Inglês
                    if lang_code in yt.captions:
                        caption_lang = 'pt' if 'pt' in lang_code else 'en'
                        self.update_status(f"Baixando legenda em {caption_lang.upper()}...")
                        caption = yt.captions[lang_code]
                        caption.download(
                            title=f"{safe_title}_{caption_lang}_caption", 
                            output_path=captions_output_path,
                            srt=False # Salva como .txt (formato simples)
                        )
            
            # 3. Extrair áudio para MP3
            self.update_status("Extraindo áudio para MP3...")
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(os.path.join(audio_output_path, f"{safe_title}.mp3"), logger=None) # logger=None para um output mais limpo
            video_clip.close()
            audio_clip.close()
            
            self.update_status(f"Sucesso! Download e conversão concluídos.\nVerifique a pasta: {base_output_path}")

        except Exception as e:
            self.update_status(f"Ocorreu um erro: {e}")
            messagebox.showerror("Erro no Download", f"Não foi possível concluir a operação.\nDetalhes: {e}")
        finally:
            # Reabilita os botões após a conclusão ou erro
            self.download_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)

    def on_progress(self, stream, chunk, bytes_remaining):
        """
        Callback para atualizar a barra de progresso durante o download.
        """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        # Atualiza a GUI a partir da thread principal
        self.root.after(0, self.update_progress_bar, percentage)

    def update_progress_bar(self, percentage):
        """Atualiza a barra e o texto de progresso na GUI."""
        self.progress_bar['value'] = percentage
        self.progress_label['text'] = f"{percentage:.1f}%"

    def update_status(self, message):
        """Atualiza o rótulo de status na GUI."""
        self.root.after(0, self.status_label.config, {'text': message})


if __name__ == "__main__":
    # Verifica se as dependências estão instaladas antes de iniciar a GUI
    try:
        import pytubefix
        import moviepy
    except ImportError:
        # O erro já foi mostrado na caixa de mensagem no início
        pass
    else:
        root = tk.Tk()
        app = YouTubeDownloaderApp(root)
        root.mainloop()
