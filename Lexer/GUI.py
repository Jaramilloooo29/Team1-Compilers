# Team 1 - Subject: Compilers
# Members:
# 1. Cano Nieto Carlos Arturo
# 2. Cortes Bolaños Luis Angel
# 3. Martinez Garcia Luis Angel
# 4. Rodriguez Jaramillo Alejandro
# 5. Urbano Meza Joseph Gael

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, PhotoImage
import LEX_C as LEX_C


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEXER TEAM 1")
        self.root.geometry("1200x800")

        # Available themes
        self.themes = ["flatly", "darkly", "solar", "superhero", "cyborg", "morph"]
        self.current_theme = "flatly"
        self.style = ttk.Style(self.current_theme)

        # Header
        header_frame = ttk.Frame(self.root, padding=15, bootstyle="dark")
        header_frame.pack(fill=X)

        header_label = ttk.Label(
            header_frame,
            text=" 🖱️Lexical Analyzer",
            font=("Segoe UI", 18, "bold"),
            bootstyle="inverse-light"
        )
        header_label.pack(side=LEFT, padx=10)

        # Theme selector in header
        self.theme_combobox = ttk.Combobox(header_frame, values=self.themes, state="readonly", width=15)
        self.theme_combobox.set(self.current_theme)
        self.theme_combobox.pack(side=RIGHT, padx=5)

        self.change_theme_button = ttk.Button(
            header_frame,
            text="Change Theme",
            bootstyle="secondary-outline",
            command=self.change_theme
        )
        self.change_theme_button.pack(side=RIGHT, padx=5)

        # --- Main layout in vertical style ---
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Source Code Section
        self.label_input = ttk.Label(main_frame, text="🧑‍💻 Source Code", font=("Segoe UI", 12, "bold"))
        self.label_input.pack(anchor=W, pady=5)

        self.text_area_input = ttk.Text(
            main_frame,
            height=15,
            font=("Consolas", 12),
            bg="#1e1e1e",
            fg="#dcdcdc",
            insertbackground="white",
            relief="flat",
            wrap="word",
            highlightthickness=1,
            highlightbackground="#3c3c3c"
        )
        self.text_area_input.pack(fill=BOTH, expand=True, pady=5)

        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)

        ttk.Button(button_frame, text="📂 Load File", bootstyle="success", command=self.load_file).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="⚡ Analyze Code", bootstyle="info", command=self.analyze).pack(side=LEFT, padx=5)

        # Result Section
        self.label_output = ttk.Label(main_frame, text="📊 Analysis Result", font=("Segoe UI", 12, "bold"))
        self.label_output.pack(anchor=W, pady=5)

        self.text_area_output = ttk.Text(
            main_frame,
            height=15,
            font=("Consolas", 12),
            state="disabled",
            bg="#1e1e1e",
            fg="#a6e22e",
            insertbackground="white",
            relief="flat",
            wrap="word",
            highlightthickness=1,
            highlightbackground="#3c3c3c"
        )
        self.text_area_output.pack(fill=BOTH, expand=True, pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Code Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area_input.delete("1.0", "end")
                self.text_area_input.insert("end", file.read())

    def analyze(self):
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Warning", "No code to analyze")
            return

        analysis_result = LEX_C.analyze_code(code_content)

        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", analysis_result)
        self.text_area_output.config(state="disabled")

    def change_theme(self):
        new_theme = self.theme_combobox.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.style = ttk.Style(new_theme)


# --- Run the GUI ---
if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    icon = PhotoImage(file="escudo-fi.png")  # Custom window icon
    root.iconphoto(False, icon)
    app = CodeAnalyzerApp(root)
    root.mainloop()
