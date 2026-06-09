import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import math

# ── Language Dictionary ──────────────────────────────────────────────────────
languages = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de",
    "Spanish": "es", "Japanese": "ja", "Chinese": "zh-CN",
    "Marathi": "mr", "Gujarati": "gu", "Tamil": "ta",
    "Telugu": "te", "Punjabi": "pa"
}

# ── Palette ──────────────────────────────────────────────────────────────────
BG         = "#F0F4FF"
CARD       = "#FFFFFF"
ACCENT1    = "#7C6FCD"   # soft indigo
ACCENT2    = "#F472B6"   # bubblegum pink
ACCENT3    = "#34D399"   # mint green
TEXT_DARK  = "#2D2B55"
TEXT_MID   = "#6B6B8A"
BORDER     = "#DDD9F7"

# ── Floating bubble colours ──────────────────────────────────────────────────
BUBBLES = ["#C4B8F7", "#F9A8D4", "#A7F3D0", "#FDE68A", "#BAE6FD"]

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Language Translator")
        self.root.geometry("860x680")
        self.root.resizable(False, False)
        self.root.config(bg=BG)

        # ── Animated background canvas ──
        self.bg_canvas = tk.Canvas(root, width=860, height=680,
                                   bg=BG, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)

        # Bubble state
        self.bubbles = []
        self._init_bubbles()
        self._animate_bubbles()

        # ── UI on top ──
        self._build_ui()

        # ── Entrance animation ──
        self.card_y_start = 720
        self.card_y_end   = 90
        self._slide_in()

    # ────────────────────────── background bubbles ───────────────────────────
    def _init_bubbles(self):
        import random
        random.seed(42)
        for i in range(12):
            x  = random.randint(20, 840)
            y  = random.randint(20, 660)
            r  = random.randint(12, 36)
            dx = random.choice([-1, 1]) * random.uniform(0.3, 0.8)
            dy = random.choice([-1, 1]) * random.uniform(0.2, 0.6)
            col = BUBBLES[i % len(BUBBLES)]
            oid = self.bg_canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill=col, outline="", stipple=""
            )
            self.bg_canvas.itemconfig(oid, state="normal")
            self.bubbles.append([oid, x, y, r, dx, dy])

    def _animate_bubbles(self):
        for b in self.bubbles:
            oid, x, y, r, dx, dy = b
            x += dx; y += dy
            if x - r < 0 or x + r > 860: dx = -dx; x += dx * 2
            if y - r < 0 or y + r > 680: dy = -dy; y += dy * 2
            b[1], b[2], b[4], b[5] = x, y, dx, dy
            self.bg_canvas.coords(oid, x-r, y-r, x+r, y+r)
        self.root.after(30, self._animate_bubbles)

    # ────────────────────────── slide-in entrance ────────────────────────────
    def _slide_in(self):
        self._slide_step(self.card_y_start, self.card_y_end, 0)

    def _slide_step(self, current, target, step):
        ease = 1 - math.exp(-step * 0.18)
        y = current + (target - current) * ease
        self.card_frame.place(x=40, y=int(y))
        if abs(y - target) > 1:
            self.root.after(16, lambda: self._slide_step(current, target, step + 1))
        else:
            self.card_frame.place(x=40, y=target)

    # ────────────────────────── main UI ──────────────────────────────────────
    def _build_ui(self):
        # ── Heading label (fixed, above card) ──
        tk.Label(self.root,
                 text="✨ TalkAcross- A language Translator ",
                 font=("Segoe UI", 22, "bold"),
                 fg=ACCENT1, bg=BG
                 ).place(x=40, y=28)

        tk.Label(self.root,
                 text="Translate between 12 languages instantly",
                 font=("Segoe UI", 10),
                 fg=TEXT_MID, bg=BG
                 ).place(x=40, y=64)

        # ── Rounded card frame ──
        self.card_frame = tk.Frame(self.root, bg=CARD,
                                   bd=0, relief="flat")
        self.card_frame.place(x=40, y=90, width=780, height=560)
        self._round_shadow(self.card_frame)

        # ── Input section ──
        tk.Label(self.card_frame, text="📝  Enter Text",
                 font=("Segoe UI", 11, "bold"),
                 fg=TEXT_DARK, bg=CARD).place(x=24, y=18)

        self.input_text = tk.Text(
            self.card_frame, height=6, width=88,
            font=("Segoe UI", 11), relief="flat",
            bg="#F7F5FF", fg=TEXT_DARK,
            insertbackground=ACCENT1,
            padx=10, pady=8,
            wrap="word"
        )
        self.input_text.place(x=24, y=50, width=732, height=130)
        self._bind_focus_glow(self.input_text)

        # ── Language selectors row ──
        lang_row = tk.Frame(self.card_frame, bg=CARD)
        lang_row.place(x=24, y=198, width=732, height=70)

        # Source
        tk.Label(lang_row, text="From", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=CARD).grid(row=0, column=0, sticky="w")
        self.source_lang = tk.StringVar(value="English")
        src_cb = self._styled_combo(lang_row, self.source_lang)
        src_cb.grid(row=1, column=0, padx=(0, 0))

        # Swap button (animated)
        self.swap_btn = tk.Label(lang_row, text="⇄",
                                 font=("Segoe UI", 20, "bold"),
                                 fg=ACCENT1, bg=CARD, cursor="hand2")
        self.swap_btn.grid(row=0, column=1, rowspan=2, padx=30, pady=4)
        self.swap_btn.bind("<Button-1>", self._swap_langs)
        self.swap_btn.bind("<Enter>",
            lambda e: self.swap_btn.config(fg=ACCENT2))
        self.swap_btn.bind("<Leave>",
            lambda e: self.swap_btn.config(fg=ACCENT1))

        # Target
        tk.Label(lang_row, text="To", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=CARD).grid(row=0, column=2, sticky="w")
        self.target_lang = tk.StringVar(value="Hindi")
        tgt_cb = self._styled_combo(lang_row, self.target_lang)
        tgt_cb.grid(row=1, column=2)

        # ── Translate button ──
        self.trans_btn = tk.Canvas(self.card_frame, width=200, height=44,
                                   bg=CARD, highlightthickness=0, cursor="hand2")
        self.trans_btn.place(x=290, y=280)
        self._draw_pill_btn(self.trans_btn, "Translate  →", ACCENT1)
        self.trans_btn.bind("<Button-1>", lambda e: self._on_translate_click())
        self.trans_btn.bind("<Enter>",
            lambda e: self._draw_pill_btn(self.trans_btn, "Translate  →", ACCENT2))
        self.trans_btn.bind("<Leave>",
            lambda e: self._draw_pill_btn(self.trans_btn, "Translate  →", ACCENT1))

        # ── Divider ──
        self.card_frame.update_idletasks()
        tk.Frame(self.card_frame, bg=BORDER, height=1
                 ).place(x=24, y=342, width=732)

        # ── Output section ──
        self.out_label = tk.Label(self.card_frame, text="🌐  Translation",
                                  font=("Segoe UI", 11, "bold"),
                                  fg=TEXT_DARK, bg=CARD)
        self.out_label.place(x=24, y=354)

        # Copy button
        copy_btn = tk.Label(self.card_frame, text="⎘ Copy",
                            font=("Segoe UI", 9), fg=ACCENT1, bg=CARD,
                            cursor="hand2")
        copy_btn.place(x=680, y=358)
        copy_btn.bind("<Button-1>", self._copy_output)

        self.output_text = tk.Text(
            self.card_frame, height=6, width=88,
            font=("Segoe UI", 11), relief="flat",
            bg="#F0FDF8", fg=TEXT_DARK,
            padx=10, pady=8, wrap="word", state="disabled"
        )
        self.output_text.place(x=24, y=386, width=732, height=130)

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready to translate ✨")
        tk.Label(self.card_frame, textvariable=self.status_var,
                 font=("Segoe UI", 9), fg=TEXT_MID, bg=CARD
                 ).place(x=24, y=528)

    # ────────────────────────── helpers ──────────────────────────────────────
    def _round_shadow(self, frame):
        """Thin coloured border to simulate card elevation."""
        frame.config(highlightbackground=BORDER,
                     highlightthickness=2)

    def _styled_combo(self, parent, var):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Cute.TCombobox",
                        fieldbackground="#F7F5FF",
                        background=ACCENT1,
                        foreground=TEXT_DARK,
                        arrowcolor=ACCENT1,
                        bordercolor=BORDER,
                        lightcolor="#F7F5FF",
                        darkcolor="#F7F5FF")
        cb = ttk.Combobox(parent, textvariable=var,
                          values=list(languages.keys()),
                          width=22, state="readonly",
                          style="Cute.TCombobox",
                          font=("Segoe UI", 10))
        return cb

    def _bind_focus_glow(self, widget):
        widget.bind("<FocusIn>",
            lambda e: widget.config(bg="#EDE8FF"))
        widget.bind("<FocusOut>",
            lambda e: widget.config(bg="#F7F5FF"))

    def _draw_pill_btn(self, canvas, text, color):
        canvas.delete("all")
        r = 22
        canvas.create_arc(0, 0, r*2, 44, start=90, extent=180,
                          fill=color, outline="")
        canvas.create_arc(200-r*2, 0, 200, 44, start=270, extent=180,
                          fill=color, outline="")
        canvas.create_rectangle(r, 0, 200-r, 44,
                                 fill=color, outline="")
        canvas.create_text(100, 22, text=text,
                           font=("Segoe UI", 12, "bold"),
                           fill="white")

    def _swap_langs(self, event=None):
        s = self.source_lang.get()
        t = self.target_lang.get()
        self.source_lang.set(t)
        self.target_lang.set(s)
        # quick spin effect
        self._spin_swap(0)

    def _spin_swap(self, step):
        chars = ["⇄", "↻", "⇄", "↺", "⇄"]
        self.swap_btn.config(text=chars[step % len(chars)])
        if step < 6:
            self.root.after(60, lambda: self._spin_swap(step + 1))
        else:
            self.swap_btn.config(text="⇄")

    def _on_translate_click(self):
        self._pulse_btn(0)
        self.root.after(200, self._translate_text)

    def _pulse_btn(self, step):
        colors = [ACCENT2, ACCENT1, ACCENT2, ACCENT1]
        self._draw_pill_btn(self.trans_btn, "Translate  →", colors[step % len(colors)])
        if step < 3:
            self.root.after(80, lambda: self._pulse_btn(step + 1))

    def _translate_text(self):
        try:
            text = self.input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Oops!", "Please enter some text first 😊")
                return

            self.status_var.set("Translating… 🔄")
            self.root.update()

            src = languages[self.source_lang.get()]
            tgt = languages[self.target_lang.get()]
            result = GoogleTranslator(source=src, target=tgt).translate(text)

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
            self.output_text.config(state="disabled")

            self.status_var.set(
                f"✅  Translated from {self.source_lang.get()} → {self.target_lang.get()}")
            self._flash_output()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("❌  Translation failed")

    def _flash_output(self):
        """Brief green flash on the output box."""
        colours = ["#C6F6D5", "#F0FDF8", "#C6F6D5", "#F0FDF8"]
        def step(i):
            if i < len(colours):
                self.output_text.config(bg=colours[i])
                self.root.after(80, lambda: step(i + 1))
        step(0)

    def _copy_output(self, event=None):
        content = self.output_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_var.set("📋  Copied to clipboard!")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = TranslatorApp(root)
    root.mainloop()
