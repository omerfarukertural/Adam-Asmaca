import tkinter as tk
from tkinter import messagebox
import random
import string
import os
import json
from tkinter import simpledialog
import threading
import pygame
from tkinter import font as tkfont

# Modern renk paleti ve fontlar
themes = {
    'dark': {
        'bg': '#22223b',
        'fg': '#f2e9e4',
        'accent': '#9a8c98',
        'button_bg': '#4a4e69',
        'button_fg': '#f2e9e4',
        'word_bg': '#c9ada7',
        'word_fg': '#22223b',
        'font': ('Segoe UI', 16, 'bold'),
        'button_font': ('Segoe UI', 12, 'bold'),
        'title_font': ('Segoe UI', 24, 'bold'),
    },
    'light': {
        'bg': '#f2e9e4',
        'fg': '#22223b',
        'accent': '#4a4e69',
        'button_bg': '#c9ada7',
        'button_fg': '#22223b',
        'word_bg': '#9a8c98',
        'word_fg': '#f2e9e4',
        'font': ('Segoe UI', 16, 'bold'),
        'button_font': ('Segoe UI', 12, 'bold'),
        'title_font': ('Segoe UI', 24, 'bold'),
    },
}

theme = themes['dark']

LANGUAGES = {
    'tr': {
        'name': 'Türkçe',
        'words_easy': ['ELMA', 'ARABA', 'KEDİ', 'KAPI', 'MASA', 'KÖPEK', 'BULUT', 'SU', 'YAZ', 'GÜL'],
        'words_medium': ['BILGISAYAR', 'PROGRAM', 'KÜTÜPHANE', 'TELEFON', 'KAMERA', 'KUMANDA', 'KARTAL', 'KİTAPLIK', 'KALORİFER', 'DOLAP'],
        'words_hard': ['ALGORITMA', 'GELISTIRICI', 'YAZILIM', 'VERITABANI', 'YAPAYZEKA', 'PROGRAMLAMA', 'KONSERVATUVAR', 'MÜHENDİSLİK', 'PSİKOLOJİ', 'FİLOZOFLUK'],
        'labels': {
            'title': 'Adam Asmaca',
            'select_difficulty': 'Zorluk Seçin:',
            'easy': 'Kolay',
            'medium': 'Orta',
            'hard': 'Zor',
            'score': 'Skor',
            'time': 'Süre',
            'hint': 'İpucu',
            'theme': 'Tema',
            'dark': 'Koyu',
            'light': 'Açık',
            'highscores': 'En İyi Skorlar',
            'congrats': 'Tebrikler!',
            'enter_name': 'Yüksek skor! İsminizi girin:',
            'game_over': 'Kaybettiniz',
            'word': 'Kelime',
            'time_up': 'Süre Doldu',
        }
    },
    'en': {
        'name': 'English',
        'words_easy': ['APPLE', 'CAR', 'CAT', 'DOOR', 'TABLE', 'DOG', 'CLOUD', 'WATER', 'SUMMER', 'ROSE'],
        'words_medium': ['COMPUTER', 'PROGRAM', 'LIBRARY', 'PHONE', 'CAMERA', 'REMOTE', 'EAGLE', 'BOOKCASE', 'RADIATOR', 'CUPBOARD'],
        'words_hard': ['ALGORITHM', 'DEVELOPER', 'SOFTWARE', 'DATABASE', 'AI', 'PROGRAMMING', 'CONSERVATORY', 'ENGINEERING', 'PSYCHOLOGY', 'PHILOSOPHER'],
        'labels': {
            'title': 'Hangman',
            'select_difficulty': 'Select Difficulty:',
            'easy': 'Easy',
            'medium': 'Medium',
            'hard': 'Hard',
            'score': 'Score',
            'time': 'Time',
            'hint': 'Hint',
            'theme': 'Theme',
            'dark': 'Dark',
            'light': 'Light',
            'highscores': 'High Scores',
            'congrats': 'Congratulations!',
            'enter_name': 'High score! Enter your name:',
            'game_over': 'Game Over',
            'word': 'Word',
            'time_up': 'Time Up',
        }
    }
}

HIGHSCORE_FILE = 'highscores.json'
STATS_FILE = 'stats.json'

# Türkçe karakterler dahil harfler
LETTERS = list('ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ')

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.theme_name = 'dark'
        self.language = 'tr'
        global theme
        theme = themes[self.theme_name]
        self.root.title(self.labels('title'))
        self.root.geometry('800x600')
        self.root.minsize(800, 600)
        self.score = 0
        self.difficulty = None
        self.section_time_limit = 300  # Varsayılan, zorlukla değişecek
        self.time_left = 300
        self.max_attempts = 6
        self.timer = None
        self.word = ''
        self.guessed = set()
        self.attempts = 0
        self.hint_limit = 2
        self.hints_used = 0
        self.stats = self.load_stats()
        self.words_list = []
        self.current_word_index = 0
        self.total_score = 0
        self.custom_fonts()
        self.init_sounds()
        self.show_language_selection()

    def init_sounds(self):
        pygame.mixer.init()
        self.snd_correct = pygame.mixer.Sound('snd_correct.wav')
        self.snd_wrong = pygame.mixer.Sound('snd_wrong.wav')
        self.snd_win = pygame.mixer.Sound('snd_win.wav')
        self.snd_lose = pygame.mixer.Sound('snd_lose.wav')
        try:
            pygame.mixer.music.load('bg_music.mp3')
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def labels(self, key):
        return LANGUAGES[self.language]['labels'][key]

    def show_language_selection(self):
        self.clear_window()
        global theme
        theme = themes[self.theme_name]
        self.root.configure(bg=theme['bg'])
        self.title = tk.Label(self.root, text='Adam Asmaca / Hangman', bg=theme['bg'], fg=theme['accent'], font=theme['title_font'])
        self.title.pack(pady=10)
        self.lang_frame = tk.Frame(self.root, bg=theme['bg'])
        self.lang_frame.pack(pady=10)
        for code, lang in LANGUAGES.items():
            tk.Button(self.lang_frame, text=lang['name'], font=theme['button_font'], bg=theme['button_bg'], fg=theme['button_fg'], command=lambda c=code: self.set_language(c)).pack(side='left', padx=10)

    def set_language(self, code):
        self.language = code
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        self.clear_window()
        global theme
        theme = themes[self.theme_name]
        self.root.configure(bg=theme['bg'])
        self.title = tk.Label(self.root, text=self.labels('title'), bg=theme['bg'], fg=theme['accent'], font=theme['title_font'])
        self.title.pack(pady=10)
        self.show_highscores()
        self.show_stats()
        self.diff_label = tk.Label(self.root, text=self.labels('select_difficulty'), bg=theme['bg'], fg=theme['fg'], font=theme['font'])
        self.diff_label.pack(pady=10)
        self.diff_frame = tk.Frame(self.root, bg=theme['bg'])
        self.diff_frame.pack(pady=10)
        tk.Button(self.diff_frame, text=self.labels('easy'), width=10, font=theme['button_font'], bg='#8ecae6', fg=theme['word_fg'], command=lambda: self.start_game('easy')).pack(side='left', padx=10)
        tk.Button(self.diff_frame, text=self.labels('medium'), width=10, font=theme['button_font'], bg='#ffb703', fg=theme['word_fg'], command=lambda: self.start_game('medium')).pack(side='left', padx=10)
        tk.Button(self.diff_frame, text=self.labels('hard'), width=10, font=theme['button_font'], bg='#d90429', fg=theme['word_fg'], command=lambda: self.start_game('hard')).pack(side='left', padx=10)
        self.theme_frame = tk.Frame(self.root, bg=theme['bg'])
        self.theme_frame.pack(pady=10)
        tk.Label(self.theme_frame, text=self.labels('theme')+':', bg=theme['bg'], fg=theme['fg'], font=theme['font']).pack(side='left', padx=5)
        tk.Button(self.theme_frame, text=self.labels('dark'), font=theme['button_font'], bg='#22223b', fg='#f2e9e4', command=lambda: self.change_theme('dark')).pack(side='left', padx=5)
        tk.Button(self.theme_frame, text=self.labels('light'), font=theme['button_font'], bg='#f2e9e4', fg='#22223b', command=lambda: self.change_theme('light')).pack(side='left', padx=5)

    def show_highscores(self):
        scores = self.load_highscores()
        frame = tk.Frame(self.root, bg=theme['bg'])
        frame.pack(pady=5)
        tk.Label(frame, text=self.labels('highscores'), bg=theme['bg'], fg=theme['accent'], font=self.status_font).pack()
        for i, s in enumerate(scores[:5]):
            tk.Label(frame, text=f"{i+1}. {s['name']} - {s['score']}", bg=theme['bg'], fg=theme['fg'], font=self.button_font).pack()
        # Skor tablosunu silme butonu
        tk.Button(frame, text="Skor Tablosunu Sıfırla", font=self.button_font, bg='#d90429', fg='white', command=self.reset_highscores).pack(pady=5)

    def load_highscores(self):
        if not os.path.exists(HIGHSCORE_FILE):
            return []
        with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_highscore(self, name, score):
        scores = self.load_highscores()
        scores.append({'name': name, 'score': score})
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
        with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)

    def ask_highscore(self):
        name = simpledialog.askstring(self.labels('congrats'), self.labels('enter_name'))
        if name:
            self.save_highscore(name, self.score)

    def load_stats(self):
        if not os.path.exists(STATS_FILE):
            return {'played': 0, 'won': 0, 'lost': 0, 'total_score': 0}
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_stats(self):
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)

    def show_stats(self):
        frame = tk.Frame(self.root, bg=theme['bg'])
        frame.pack(pady=5)
        tk.Label(frame, text='İstatistikler', bg=theme['bg'], fg=theme['accent'], font=self.status_font).pack()
        tk.Label(frame, text=f"Oynanan: {self.stats['played']}", bg=theme['bg'], fg=theme['fg'], font=self.button_font).pack()
        tk.Label(frame, text=f"Kazandı: {self.stats['won']}", bg=theme['bg'], fg=theme['fg'], font=self.button_font).pack()
        tk.Label(frame, text=f"Kaybetti: {self.stats['lost']}", bg=theme['bg'], fg=theme['fg'], font=self.button_font).pack()
        tk.Label(frame, text=f"Toplam Skor: {self.stats['total_score']}", bg=theme['bg'], fg=theme['fg'], font=self.button_font).pack()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        lang = LANGUAGES[self.language]
        if difficulty == 'easy':
            self.words_list = random.sample(lang['words_easy'], min(10, len(lang['words_easy'])))
            self.section_time_limit = 300  # 5 dakika
            self.max_attempts = 8
            self.hint_limit = 3
        elif difficulty == 'medium':
            self.words_list = random.sample(lang['words_medium'], min(10, len(lang['words_medium'])))
            self.section_time_limit = 240  # 4 dakika
            self.max_attempts = 6
            self.hint_limit = 2
        else:
            self.words_list = random.sample(lang['words_hard'], min(10, len(lang['words_hard'])))
            self.section_time_limit = 180  # 3 dakika
            self.max_attempts = 5
            self.hint_limit = 1
        self.current_word_index = 0
        self.total_score = 0
        self.time_left = self.section_time_limit
        self.start_next_word()
        self.start_section_timer()

    def start_section_timer(self):
        self.update_section_timer()

    def update_section_timer(self):
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.time_label['text'] = f"{self.labels('time')}: {mins:02d}:{secs:02d}"
        if self.time_left > 0 and self.current_word_index < len(self.words_list):
            self.time_left -= 1
            self.timer = self.root.after(1000, self.update_section_timer)
        elif self.time_left == 0:
            self.show_section_result(time_out=True)

    def start_next_word(self):
        if self.current_word_index >= len(self.words_list):
            self.show_section_result()
            return
        self.word = self.words_list[self.current_word_index]
        self.guessed = set()
        self.attempts = 0
        self.hints_used = 0
        self.clear_window()
        self.create_widgets()
        self.give_initial_hint()
        self.update_word_display()
        # self.start_timer() kaldırıldı

    def give_initial_hint(self):
        remaining = [c for c in set(self.word)]
        if remaining:
            letter = random.choice(remaining)
            self.guessed.add(letter)
            # İpucu hakkı düşmesin diye hints_used artırılmıyor
            for btn in self.letter_buttons.values():
                if btn['text'] == letter:
                    btn['state'] = 'disabled'

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def custom_fonts(self):
        # Modern fontlar ve başlık için büyük font
        self.title_font = tkfont.Font(family='Arial', size=32, weight='bold')
        self.word_font = tkfont.Font(family='Arial', size=22, weight='bold')
        self.button_font = tkfont.Font(family='Arial', size=14, weight='bold')
        self.status_font = tkfont.Font(family='Arial', size=16, weight='normal')

    def create_widgets(self):
        # Sabit arka plan rengi
        self.root.configure(bg='#e0e7ff')
        # Üst menü çubuğu
        self.topbar = tk.Frame(self.root, bg='#e0e7ff', highlightthickness=0, bd=0)
        self.topbar.pack(fill='x', pady=(5,0))
        self.menu_btn = tk.Button(self.topbar, text='⏪ Ana Menü', font=self.button_font, bg='#e0e7ff', fg='#111', command=self.menu_confirm, relief='flat', bd=0, activebackground='#d6e0f0', highlightthickness=0)
        self.menu_btn.pack(side='right', padx=10)
        # Başlık ve ikon
        self.title_frame = tk.Frame(self.root, bg='#e0e7ff', highlightthickness=0, bd=0)
        self.title_frame.pack(pady=10)
        self.icon_label = tk.Label(self.title_frame, text='🕹️', bg='#e0e7ff', fg='#111', font=('Arial', 32, 'bold'), highlightthickness=0, bd=0)
        self.icon_label.pack(side='left', padx=5)
        self.title = tk.Label(self.title_frame, text=self.labels('title'), bg='#e0e7ff', fg='#111', font=self.title_font, highlightthickness=0, bd=0)
        self.title.pack(side='left', padx=5)
        # Bilgi çubuğu
        self.info_frame = tk.Frame(self.root, bg='#e0e7ff', highlightthickness=0, bd=0)
        self.info_frame.pack(pady=5)
        self.score_label = tk.Label(self.info_frame, text=f"{self.labels('score')}: {self.score}", bg='#e0e7ff', fg='#111', font=self.status_font, highlightthickness=0, bd=0)
        self.score_label.pack(side='left', padx=30)
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.time_label = tk.Label(self.info_frame, text=f"{self.labels('time')}: {mins:02d}:{secs:02d}", bg='#e0e7ff', fg='#111', font=self.status_font, highlightthickness=0, bd=0)
        self.time_label.pack(side='left', padx=30)
        self.hint_label = tk.Label(self.info_frame, text=f"{self.labels('hint')}: {self.hint_limit - self.hints_used}", bg='#e0e7ff', fg='#111', font=self.status_font, highlightthickness=0, bd=0)
        self.hint_label.pack(side='left', padx=30)
        self.hint_button = tk.Button(self.info_frame, text=self.labels('hint'), bg='#e0e7ff', fg='#111', font=self.button_font, command=self.use_hint, relief='flat', bd=0, activebackground='#d6e0f0', highlightthickness=0)
        self.hint_button.pack(side='left', padx=10)
        # Kelime kutucukları
        self.word_frame = tk.Frame(self.root, bg='#e0e7ff', highlightthickness=0, bd=0)
        self.word_frame.pack(pady=30)
        self.word_labels = []
        for _ in self.word:
            lbl = tk.Label(
                self.word_frame,
                text='_',
                width=3,
                bg='#e0e7ff',
                fg='#111',
                font=self.word_font,
                relief='flat',
                bd=0,
                padx=0,
                pady=0,
                highlightthickness=0
            )
            lbl.pack(side='left', padx=8)
            self.word_labels.append(lbl)
        # Harf butonları
        self.letters_frame = tk.Frame(self.root, bg='#e0e7ff', highlightthickness=0, bd=0)
        self.letters_frame.pack(pady=20)
        self.letter_buttons = {}
        for i, letter in enumerate(LETTERS):
            btn = tk.Button(self.letters_frame, text=letter, width=4, bg='#e0e7ff', fg='#111', font=self.button_font,
                            command=lambda l=letter: self.guess_letter(l), relief='flat', bd=0, activebackground='#d6e0f0', highlightthickness=0)
            btn.grid(row=i//11, column=i%11, padx=6, pady=6)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#d6e0f0'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#e0e7ff'))
            self.letter_buttons[letter] = btn
        # Durum etiketi
        self.status_label = tk.Label(self.root, text=f"{self.labels('score')}: {self.max_attempts - self.attempts}", bg='#e0e7ff', fg='#111', font=self.status_font, highlightthickness=0, bd=0)
        self.status_label.pack(pady=20)

    def update_word_display(self):
        for i, c in enumerate(self.word):
            if c in self.guessed:
                self.word_labels[i]['text'] = c
            else:
                self.word_labels[i]['text'] = '_'
        self.status_label['text'] = f"{self.labels('score')}: {self.max_attempts - self.attempts}"
        self.score_label['text'] = f"{self.labels('score')}: {self.score}"
        self.hint_label['text'] = f"{self.labels('hint')}: {self.hint_limit - self.hints_used}"
        if self.hints_used >= self.hint_limit:
            self.hint_button['state'] = 'disabled'
        else:
            self.hint_button['state'] = 'normal'
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.time_label['text'] = f"{self.labels('time')}: {mins:02d}:{secs:02d}"

    def animate_letter(self, idx, color):
        lbl = self.word_labels[idx]
        orig_bg = lbl['bg']
        lbl['bg'] = color
        self.root.after(300, lambda: lbl.config(bg=orig_bg))

    def guess_letter(self, letter):
        self.letter_buttons[letter]['state'] = 'disabled'
        if letter in self.word:
            self.guessed.add(letter)
            for i, c in enumerate(self.word):
                if c == letter:
                    self.animate_letter(i, '#38b000')  # yeşil
            self.snd_correct.play()
            self.score += 5
            self.update_word_display()
            if all(c in self.guessed for c in self.word):
                self.score += 20
                self.animate_reveal_word(success=True)
                self.stats['played'] += 1
                self.stats['won'] += 1
                self.stats['total_score'] += self.score
                self.save_stats()
                self.total_score += self.score
                self.current_word_index += 1
                self.root.after(1200, self.start_next_word)
        else:
            self.attempts += 1
            for i, c in enumerate(self.word):
                if c not in self.guessed:
                    self.animate_letter(i, '#d90429')  # kırmızı
            self.snd_wrong.play()
            self.score = max(0, self.score - 2)
            self.update_word_display()
            if self.attempts >= self.max_attempts:
                self.animate_reveal_word(success=False)
                self.snd_lose.play()
                self.stats['played'] += 1
                self.stats['lost'] += 1
                self.stats['total_score'] += self.score
                self.save_stats()
                self.current_word_index += 1
                self.root.after(1200, self.start_next_word)

    def use_hint(self):
        if self.hints_used < self.hint_limit:
            remaining = [c for c in set(self.word) if c not in self.guessed]
            if remaining:
                letter = random.choice(remaining)
                self.guessed.add(letter)
                self.hints_used += 1
                self.update_word_display()
                for btn in self.letter_buttons.values():
                    if btn['text'] == letter:
                        btn['state'] = 'disabled'
                if all(c in self.guessed for c in self.word):
                    self.score += 20
                    self.animate_reveal_word(success=True)
                    self.root.after(1000, self.start_next_word)

    def start_timer(self):
        self.time_left = self.time_limit
        self.update_timer()

    def update_timer(self):
        self.time_label['text'] = f'Süre: {self.time_left}'
        if self.time_left > 0 and not all(c in self.guessed for c in self.word) and self.attempts < self.max_attempts:
            self.time_left -= 1
            self.timer = self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            messagebox.showerror('Süre Doldu', f'Kelime: {self.word}')
            self.root.after(1000, self.start_next_word)

    def reset_game(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self.show_difficulty_selection() # Reset to difficulty selection

    def change_theme(self, theme_name):
        self.theme_name = theme_name
        global theme
        theme = themes[self.theme_name]
        self.show_difficulty_selection()

    def check_and_save_highscore(self):
        scores = self.load_highscores()
        if len(scores) < 10 or self.score > min([s['score'] for s in scores] or [0]):
            self.ask_highscore()

    def animate_reveal_word(self, success):
        def reveal():
            for i, c in enumerate(self.word):
                self.word_labels[i]['text'] = c
                self.word_labels[i]['bg'] = '#38b000' if success else '#d90429'
                self.root.update()
                threading.Event().wait(0.1)
            self.root.after(500, lambda: [self.word_labels[i].config(bg=theme['word_bg']) for i in range(len(self.word))])
        threading.Thread(target=reveal).start()

    def show_section_result(self, time_out=False):
        self.clear_window()
        tk.Label(self.root, text=self.labels('title'), bg=theme['bg'], fg=theme['accent'], font=self.title_font).pack(pady=30)
        if time_out:
            tk.Label(self.root, text="Süre doldu!", bg=theme['bg'], fg='#d90429', font=self.word_font).pack(pady=10)
        # Süre bonusu
        time_bonus = int(self.time_left * 0.5)
        self.total_score += time_bonus
        if time_bonus > 0:
            tk.Label(self.root, text=f"Süre Bonusu: +{time_bonus}", bg=theme['bg'], fg='#38b000', font=self.word_font).pack(pady=5)
        if self.total_score < 0:
            self.total_score = 0
        tk.Label(self.root, text=f"Bölüm Bitti! Toplam Skor: {self.total_score}", bg=theme['bg'], fg=theme['fg'], font=self.word_font).pack(pady=10)
        # Bölüm sonunda kazanma sesi
        if not time_out:
            self.snd_win.play()
        self.check_and_save_highscore_section()
        tk.Button(self.root, text="Ana Menü", font=self.button_font, bg=theme['button_bg'], fg=theme['button_fg'], command=self.show_difficulty_selection).pack(pady=20)

    def check_and_save_highscore_section(self):
        scores = self.load_highscores()
        if len(scores) < 10 or self.total_score > min([s['score'] for s in scores] or [0]):
            name = self.ask_highscore_section()
            if name:
                self.save_highscore(name, self.total_score)

    def ask_highscore_section(self):
        return simpledialog.askstring(self.labels('congrats'), self.labels('enter_name'))

    def reset_highscores(self):
        if os.path.exists(HIGHSCORE_FILE):
            os.remove(HIGHSCORE_FILE)
        messagebox.showinfo("Bilgi", "Skor tablosu sıfırlandı!")
        self.show_difficulty_selection()

    def menu_confirm(self):
        if messagebox.askyesno('Ana Menü', 'Bölümden çıkmak istediğine emin misin?'):
            if self.timer:
                self.root.after_cancel(self.timer)
            self.show_difficulty_selection()

def main():
    root = tk.Tk()
    root.geometry('600x400')
    HangmanGame(root)
    root.mainloop()

if __name__ == '__main__':
    main() 