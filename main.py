import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from threading import Thread
from Class.VideoDownloader import VideoDownloader 
from Class.AudioDownloader import AudioDownloader  

def main():
    video_downloader = VideoDownloader()
    audio_downloader = AudioDownloader()
    waiting_window = None  # Variável para armazenar a janela "Aguarde"

    def show_waiting_window():
        nonlocal waiting_window
        waiting_window = Toplevel(root)
        waiting_window.title("Por favor, aguarde")
        waiting_window.geometry("250x100")
        waiting_window.resizable(False, False)
        Label(waiting_window, text="Aguarde, baixando...").pack(expand=True, pady=20)
        # Não é preciso lockar a janela por causa do uso de threads assim ele não trava a interface principal
        # Impede interação com a janela principal enquanto esta estiver aberta
        # waiting_window.transient(root)
        # waiting_window.grab_set()

    # Fecha a pagina de "Aguarde" quando terminar o download
    def close_waiting_window():
        nonlocal waiting_window
        if waiting_window and waiting_window.winfo_exists():
            waiting_window.destroy()
            waiting_window = None

    # Função que lida com o botão de download
    def handle_download():
        url = url_entry.get().strip()
        if not url: # Só para garantir que não esteja vazia a caixa de texto
            messagebox.showwarning("Aviso", "Por favor, insira uma URL.")
            return

        option = download_type.get() 
        show_waiting_window()
        thread = Thread(target=start_download, args=(option, url))
        thread.start()

    def start_download(option, url):
        try:
            if option == "Vídeo":
                video_downloader.download_video(url)
                result_message = "Vídeo baixado com sucesso!"
            elif option == "Playlist Video":
                video_downloader.download_playlist(url)
                result_message = "Playlist baixada com sucesso!"
            elif option == "Audio":
                audio_downloader.download_audio(url)
                result_message = "Áudio baixado com sucesso!"
            elif option == "Playlist Audio":
                audio_downloader.download_audio_playlist(url)
                result_message = "Playlist de áudio baixada com sucesso!"
            else:
                result_message = "Tipo de download inválido."
                root.after(0, lambda: messagebox.showwarning("Aviso", result_message))
                return

            root.after(0, lambda: messagebox.showinfo("Sucesso", result_message))
        except Exception as e:
            root.after(0, lambda err=e: messagebox.showerror("Erro", f"Ocorreu um erro: {err}"))
        finally:
            root.after(0, close_waiting_window)

    # Interface principal
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("400x200")

    tk.Label(root, text="Insira a URL do vídeo ou playlist:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack()

    download_type = tk.StringVar()
    download_type.set("Audio")

    tk.Label(root, text="Selecione o tipo de download:").pack(pady=5)
    dropdown = tk.OptionMenu(root, download_type, "Audio", "Vídeo", "Playlist Audio", "Playlist Video")
    dropdown.pack()

    tk.Button(root, text="Baixar", command=handle_download).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
