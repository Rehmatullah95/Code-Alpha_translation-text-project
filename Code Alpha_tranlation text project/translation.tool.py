import tkinter as tk
from tkinter import ttk, messagebox
import threading
from deep_translator import GoogleTranslator

# ── Language List ──
LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Turkish": "tr",
    "Italian": "it",
    "Portuguese": "pt",
    "Persian": "fa",
    "Bengali": "bn",
    "Dutch": "nl",
    "Polish": "pl",
    "Swedish": "sv",
    "Malay": "ms",
}

LANG_NAMES = list(LANGUAGES.keys())

# ── Main App ──
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 LinguaSwift — Language Translator")
        self.root.geometry("900x620")
        self.root.resizable(True, True)
        self.root.configure(bg="#0d0f14")

        self.history = []
        self.build_ui()

    def build_ui(self):
        BG       = "#0d0f14"
        SURFACE  = "#161a23"
        CARD     = "#1e2330"
        BORDER   = "#2a3040"
        ACCENT   = "#6c63ff"
        TEXT     = "#e8eaf0"
        MUTED    = "#7a8299"
        SUCCESS  = "#34d399"
        ERROR    = "#f87171"

        self.colors = {
            "bg": BG, "surface": SURFACE, "card": CARD,
            "border": BORDER, "accent": ACCENT, "text": TEXT,
            "muted": MUTED, "success": SUCCESS, "error": ERROR
        }

        # ── Header ──
        header = tk.Frame(self.root, bg=BG)
        header.pack(pady=(30, 10))

        tk.Label(header, text="🌐 LinguaSwift", font=("Segoe UI", 26, "bold"),
                 fg=ACCENT, bg=BG).pack()
        tk.Label(header, text="Instant translation across 20+ languages",
                 font=("Segoe UI", 10), fg=MUTED, bg=BG).pack()

        # ── Main Card ──
        card = tk.Frame(self.root, bg=SURFACE, bd=0, relief="flat")
        card.pack(padx=40, pady=10, fill="both", expand=True)
        card.configure(highlightbackground=BORDER, highlightthickness=1)

        # ── Language Row ──
        lang_frame = tk.Frame(card, bg=SURFACE)
        lang_frame.pack(padx=24, pady=(20, 10), fill="x")

        # Source Language
        src_frame = tk.Frame(lang_frame, bg=SURFACE)
        src_frame.pack(side="left", fill="x", expand=True)
        tk.Label(src_frame, text="FROM", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w")
        self.src_lang = ttk.Combobox(src_frame, values=LANG_NAMES,
                                      font=("Segoe UI", 10), state="readonly", width=22)
        self.src_lang.set("English")
        self.src_lang.pack(anchor="w", pady=(4, 0))

        # Swap Button
        swap_frame = tk.Frame(lang_frame, bg=SURFACE)
        swap_frame.pack(side="left", padx=16, pady=(14, 0))
        tk.Button(swap_frame, text="⇄", font=("Segoe UI", 14, "bold"),
                  fg=ACCENT, bg=CARD, bd=0, cursor="hand2",
                  activebackground=BORDER, activeforeground=ACCENT,
                  command=self.swap_languages, padx=10, pady=4).pack()

        # Target Language
        tgt_frame = tk.Frame(lang_frame, bg=SURFACE)
        tgt_frame.pack(side="left", fill="x", expand=True)
        tk.Label(tgt_frame, text="TO", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w")
        self.tgt_lang = ttk.Combobox(tgt_frame, values=LANG_NAMES,
                                      font=("Segoe UI", 10), state="readonly", width=22)
        self.tgt_lang.set("Urdu")
        self.tgt_lang.pack(anchor="w", pady=(4, 0))

        # ── Text Areas ──
        text_frame = tk.Frame(card, bg=SURFACE)
        text_frame.pack(padx=24, pady=10, fill="both", expand=True)

        # Source Text
        src_text_frame = tk.Frame(text_frame, bg=SURFACE)
        src_text_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(src_text_frame, text="SOURCE TEXT", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w")
        self.src_text = tk.Text(src_text_frame, height=10, font=("Segoe UI", 11),
                                 bg=CARD, fg=TEXT, bd=0, relief="flat",
                                 insertbackground=TEXT, wrap="word",
                                 padx=10, pady=10,
                                 highlightbackground=BORDER, highlightthickness=1)
        self.src_text.pack(fill="both", expand=True, pady=(6, 0))
        self.src_text.bind("<KeyRelease>", self.update_char_count)

        # char count
        self.char_label = tk.Label(src_text_frame, text="0 / 2000",
                                    font=("Segoe UI", 8), fg=MUTED, bg=SURFACE)
        self.char_label.pack(anchor="e")

        # Target Text
        tgt_text_frame = tk.Frame(text_frame, bg=SURFACE)
        tgt_text_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))
        tk.Label(tgt_text_frame, text="TRANSLATION", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w")
        self.tgt_text = tk.Text(tgt_text_frame, height=10, font=("Segoe UI", 11),
                                 bg="#181c27", fg=TEXT, bd=0, relief="flat",
                                 state="disabled", wrap="word",
                                 padx=10, pady=10,
                                 highlightbackground=BORDER, highlightthickness=1)
        self.tgt_text.pack(fill="both", expand=True, pady=(6, 0))

        self.tgt_char_label = tk.Label(tgt_text_frame, text="",
                                        font=("Segoe UI", 8), fg=MUTED, bg=SURFACE)
        self.tgt_char_label.pack(anchor="e")

        # ── Action Buttons ──
        btn_frame = tk.Frame(card, bg=SURFACE)
        btn_frame.pack(padx=24, pady=(8, 16), fill="x")

        tk.Button(btn_frame, text="  🌐  Translate  ", font=("Segoe UI", 11, "bold"),
                  fg="white", bg=ACCENT, bd=0, cursor="hand2",
                  activebackground="#5a52e0", activeforeground="white",
                  padx=10, pady=8, command=self.start_translate).pack(side="left")

        tk.Button(btn_frame, text="  🗑  Clear  ", font=("Segoe UI", 10),
                  fg=TEXT, bg=CARD, bd=0, cursor="hand2",
                  activebackground=BORDER, activeforeground=TEXT,
                  padx=10, pady=8, command=self.clear_all).pack(side="left", padx=(10, 0))

        tk.Button(btn_frame, text="  📋  Copy  ", font=("Segoe UI", 10),
                  fg=TEXT, bg=CARD, bd=0, cursor="hand2",
                  activebackground=BORDER, activeforeground=TEXT,
                  padx=10, pady=8, command=self.copy_translation).pack(side="right")

        tk.Button(btn_frame, text="  🔊  Speak  ", font=("Segoe UI", 10),
                  fg=TEXT, bg=CARD, bd=0, cursor="hand2",
                  activebackground=BORDER, activeforeground=TEXT,
                  padx=10, pady=8, command=self.speak_translation).pack(side="right", padx=(0, 10))

        # ── Status Bar ──
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self.root, textvariable=self.status_var,
                                      font=("Segoe UI", 9), fg=MUTED, bg=BG)
        self.status_label.pack(pady=(0, 6))

        # ── History Frame ──
        self.history_outer = tk.Frame(self.root, bg=BG)
        self.history_outer.pack(padx=40, pady=(0, 20), fill="x")

        self.history_title = tk.Label(self.history_outer, text="RECENT TRANSLATIONS",
                                       font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG)
        self.history_frame = tk.Frame(self.history_outer, bg=BG)

        # Style combobox
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                         fieldbackground=CARD, background=CARD,
                         foreground=TEXT, selectbackground=CARD,
                         selectforeground=TEXT, bordercolor=BORDER,
                         arrowcolor=MUTED, relief="flat")
        style.map("TCombobox", fieldbackground=[("readonly", CARD)],
                  foreground=[("readonly", TEXT)])

    # ── Methods ──

    def update_char_count(self, event=None):
        text = self.src_text.get("1.0", "end-1c")
        count = len(text)
        self.char_label.config(text=f"{count} / 2000")
        if count > 2000:
            self.src_text.delete("2000c", "end")

    def swap_languages(self):
        src = self.src_lang.get()
        tgt = self.tgt_lang.get()
        self.src_lang.set(tgt)
        self.tgt_lang.set(src)

        tgt_content = self.tgt_text.get("1.0", "end-1c")
        if tgt_content.strip():
            self.src_text.delete("1.0", "end")
            self.src_text.insert("1.0", tgt_content)
            self.set_translation("")
            self.update_char_count()

    def start_translate(self):
        # Run in thread so UI doesn't freeze
        t = threading.Thread(target=self.do_translate)
        t.daemon = True
        t.start()

    def do_translate(self):
        text = self.src_text.get("1.0", "end-1c").strip()
        src_name = self.src_lang.get()
        tgt_name = self.tgt_lang.get()

        if not text:
            self.set_status("⚠ Please enter some text.", "error")
            return
        if src_name == tgt_name:
            self.set_status("⚠ Source and target languages are the same.", "error")
            return

        src_code = LANGUAGES[src_name]
        tgt_code = LANGUAGES[tgt_name]

        self.set_status("⏳ Translating...", "spin")

        try:
            translator = GoogleTranslator(source=src_code, target=tgt_code)
            result = translator.translate(text)
            self.set_translation(result)
            self.tgt_char_label.config(text=f"{len(result)} chars")
            self.set_status("✓ Translation complete!", "success")
            self.add_history(text, result, src_name, tgt_name)
        except Exception as e:
            self.set_status(f"✗ Error: {str(e)}", "error")

    def set_translation(self, text):
        self.tgt_text.config(state="normal")
        self.tgt_text.delete("1.0", "end")
        self.tgt_text.insert("1.0", text)
        self.tgt_text.config(state="disabled")

    def set_status(self, msg, type_="normal"):
        colors = {"success": "#34d399", "error": "#f87171",
                  "spin": "#a78bfa", "normal": "#7a8299"}
        self.status_var.set(msg)
        self.status_label.config(fg=colors.get(type_, "#7a8299"))

    def clear_all(self):
        self.src_text.delete("1.0", "end")
        self.set_translation("")
        self.char_label.config(text="0 / 2000")
        self.tgt_char_label.config(text="")
        self.set_status("Ready", "normal")

    def copy_translation(self):
        text = self.tgt_text.get("1.0", "end-1c")
        if not text.strip():
            self.set_status("⚠ Nothing to copy yet.", "error")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.set_status("✓ Copied to clipboard!", "success")

    def speak_translation(self):
        text = self.tgt_text.get("1.0", "end-1c").strip()
        if not text:
            self.set_status("⚠ Nothing to speak yet.", "error")
            return
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            self.set_status("🔊 Speaking...", "spin")
            engine.runAndWait()
            self.set_status("✓ Done speaking.", "success")
        except ImportError:
            self.set_status("⚠ Install pyttsx3: pip install pyttsx3", "error")

    def add_history(self, src, tgt, src_name, tgt_name):
        self.history.insert(0, (src, tgt, src_name, tgt_name))
        if len(self.history) > 4:
            self.history.pop()
        self.render_history()

    def render_history(self):
        self.history_title.pack(anchor="w", pady=(0, 6))
        self.history_frame.pack(fill="x")

        for widget in self.history_frame.winfo_children():
            widget.destroy()

        BG = self.colors["bg"]
        SURFACE = self.colors["surface"]
        BORDER = self.colors["border"]
        TEXT = self.colors["text"]
        MUTED = self.colors["muted"]
        ACCENT = self.colors["accent"]

        for src, tgt, src_name, tgt_name in self.history:
            item = tk.Frame(self.history_frame, bg=SURFACE,
                            highlightbackground=BORDER, highlightthickness=1)
            item.pack(fill="x", pady=3)

            left = tk.Frame(item, bg=SURFACE)
            left.pack(side="left", fill="x", expand=True, padx=12, pady=8)

            src_short = src[:70] + "…" if len(src) > 70 else src
            tgt_short = tgt[:90] + "…" if len(tgt) > 90 else tgt

            tk.Label(left, text=src_short, font=("Segoe UI", 9),
                     fg=MUTED, bg=SURFACE, anchor="w").pack(anchor="w")
            tk.Label(left, text=tgt_short, font=("Segoe UI", 10),
                     fg=TEXT, bg=SURFACE, anchor="w").pack(anchor="w")

            badge = tk.Label(item, text=f"{src_name} → {tgt_name}",
                             font=("Segoe UI", 8), fg=ACCENT, bg=SURFACE,
                             padx=8, pady=4)
            badge.pack(side="right", padx=12)


# ── Run ──
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()