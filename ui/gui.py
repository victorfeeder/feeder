import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from feeds.rss_reader import RSSReader
from player.audio_player import AudioPlayer

FEED_DIOCAST = "https://anchor.fm/s/4c177cd4/podcast/rss"

class FeederUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Feeder - sempre coma feeds RSS")
        self.root.geometry("650x600")

        self.player = AudioPlayer()
        self.reader = None
        self.logo_img = None

        # --- IMAGEM DA LORI LOUD ---
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            IMAGE_PATH = os.path.join(BASE_DIR, "lori_loud.webp")
            image = Image.open(IMAGE_PATH)
            image = image.resize((200, 200))
            self.logo_img = ImageTk.PhotoImage(image)
            self.logo_label = tk.Label(self.root, image=self.logo_img)
            self.logo_label.pack(pady=10)
        except Exception as e:
            print("Não foi possível carregar a imagem:", e)

        # --- INPUT RSS ---
        self.feed_entry = tk.Entry(self.root, width=50)
        self.feed_entry.pack(pady=5)
        self.feed_entry.insert(0, "Cole aqui o link do feed RSS")

        self.load_btn = tk.Button(self.root, text="Carregar Feed", command=self.load_feed)
        self.load_btn.pack(pady=5)

        # --- LISTA DE EPISÓDIOS ---
        self.episode_list = tk.Listbox(self.root, width=80)
        self.episode_list.pack(pady=10)
        self.episode_list.bind('<Double-1>', self.play_selected_episode)

        # --- BOTÃO PARAR ---
        self.stop_btn = tk.Button(self.root, text="Parar", command=self.player.stop)
        self.stop_btn.pack(pady=5)

    def load_feed(self):
        input_text = self.feed_entry.get().strip()
        url = input_text if input_text else FEED_DIOCAST

        if not url:
            messagebox.showwarning("Aviso", "Digite um link válido")
            return
        try:
            self.reader = RSSReader(url)
            self.episode_list.delete(0, tk.END)
            for ep in self.reader.get_episodes():
                self.episode_list.insert(tk.END, f"{ep['title']} ({ep['published']})")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar feed: {e}")

    def play_selected_episode(self, event):
        idx = self.episode_list.curselection()
        if not idx:
            return
        episode = self.reader.get_episodes()[idx[0]]
        if episode['audio_url']:
            self.player.play(episode['audio_url'])
        else:
            messagebox.showinfo("Info", "Esse episódio não possui link de áudio")

    def run(self):
        self.root.mainloop()
