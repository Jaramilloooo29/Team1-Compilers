# Team 1 - Subject: Compilers
# Members:
# 1. Cano Nieto Carlos Arturo
# 2. Cortes Bolaños Luis Angel
# 3. Martinez Garcia Luis Angel
# 4. Rodriguez Jaramillo Alejandro
# 5. Urbano Meza Joseph Gael

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Required files (Updated Lexer and Parser)
import LEX_C
import PARSER_C

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Team 1 - Compilers - Parser & SDT")
        self.root.geometry("1000x700")
        self.root.minsize(950, 650)

        # Application icon
        try:
            self.root.iconphoto(False, ImageTk.PhotoImage(file="escudo-fi.png"))
        except:
            pass

        # Style and theme
        self.themes = ["flatly", "darkly", "solar", "superhero", "minty", "cyborg"]
        self.current_theme = "flatly"
        self.style = ttk.Style(self.current_theme)
        self.root.configure(bg="#f0f0f0")

        # --- Title ---
        self.title_label = ttk.Label(root, text="Team 1 - Compilers - Parser & SDT", bootstyle="primary-inverse fs-4 fw-bold", anchor="center")
        self.title_label.pack(fill=X, pady=10)

        # --- Main frame ---
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)

        # --- Source code box ---
        self.code_frame = ttk.LabelFrame(self.main_frame, text="Source Code", bootstyle="primary")
        self.code_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.text_area_input = ttk.Text(self.code_frame, height=12, font=("Consolas", 12), relief="solid", borderwidth=1)
        self.text_area_input.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Default code for SDT testing
        default_code = """int main(){
    int x;
    x = 10 * 2 + 1;
    if (x > 10){
        printf("x es mayor que 10");
    }else{
        printf("x es menor que 10");
    }
}"""
        self.text_area_input.insert("1.0", default_code)

        # --- Analysis result box ---
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Analysis Result - Parser & SDT", bootstyle="warning")
        self.output_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.text_area_output = ttk.Text(self.output_frame, height=12, font=("Consolas", 12), state="disabled", relief="solid", borderwidth=1)
        self.text_area_output.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Options box ---
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Analysis Options", bootstyle="success")
        self.options_frame.pack(fill=X, padx=5, pady=5)

        # UPDATED option buttons
        ttk.Button(self.options_frame, text="Load File", bootstyle="success-outline", width=20, command=self.load_file).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(self.options_frame, text="Lexical Analyzer", bootstyle="info-outline", width=20, command=self.analyze_lexical).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(self.options_frame, text="Parser + SDT", bootstyle="warning-outline", width=20, command=self.analyze_parser_sdt).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(self.options_frame, text="Clear Results", bootstyle="secondary-outline", width=20, command=self.clear_results).pack(side=LEFT, padx=5, pady=5)

        # Theme
        self.theme_frame = ttk.Frame(root, padding=10)
        self.theme_frame.pack(fill=X)

        self.theme_label = ttk.Label(self.theme_frame, text="Select Theme:", bootstyle="secondary")
        self.theme_label.pack(side=LEFT, padx=5)

        self.theme_combobox = ttk.Combobox(self.theme_frame, values=self.themes, state="readonly", width=15)
        self.theme_combobox.set(self.current_theme)
        self.theme_combobox.pack(side=LEFT, padx=5)

        self.change_theme_button = ttk.Button(self.theme_frame, text="Change Theme", bootstyle="secondary", command=self.change_theme)
        self.change_theme_button.pack(side=LEFT, padx=5)

    # --- UPDATED Functions ---
    def load_file(self):
        """Load file with multiple fallback options"""
        try:
            # Opción 1: Intentar con el formato estándar
            file_path = filedialog.askopenfilename(
                title="Select a source code file",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("C source files", "*.c"),
                    ("All files", "*")
                ]
            )
            
            # Si no funciona, intentar opción alternativa
            if not file_path:
                # Opción 2: Diálogo sin filtros
                file_path = filedialog.askopenfilename(title="Select any file")
            
            if file_path:
                # Verificar extensión del archivo
                _, ext = os.path.splitext(file_path)
                if ext.lower() not in ['.txt', '.c', '']:
                    if not messagebox.askyesno("Confirm", 
                                             f"This file has extension {ext}. Are you sure you want to load it?"):
                        return
                
                # Leer el archivo con diferentes encodings
                content = self.read_file_with_fallback(file_path)
                if content is not None:
                    self.text_area_input.delete("1.0", "end")
                    self.text_area_input.insert("end", content)
                    messagebox.showinfo("Success", f"File loaded: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Could not read the file content")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def read_file_with_fallback(self, file_path):
        """Try reading file with different encodings"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error with encoding {encoding}: {e}")
                continue
        
        # Último intento: leer como binario y decodificar
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Binary read failed: {e}")
            return None

    def change_theme(self):
        new_theme = self.theme_combobox.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.style = ttk.Style(new_theme)
            bg_color = "#f5f5f5" if new_theme != "darkly" else "#2b2b2b"
            fg_color = "#000000" if new_theme != "darkly" else "#ffffff"
            border_color = "#cccccc" if new_theme != "darkly" else "#444444"
            self.root.configure(bg=bg_color)
            self.text_area_input.configure(bg=bg_color, fg=fg_color, highlightbackground=border_color)
            self.text_area_output.configure(bg=bg_color, fg=fg_color, highlightbackground=border_color)

    def analyze_lexical(self):
        """Lexical analysis only"""
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Warning", "No code to analyze")
            return
        
        tokens = LEX_C.analyze_code(code_content)
        errors = LEX_C.get_lexical_errors()
        
        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        
        if errors:
            self.text_area_output.insert("end", "=== LEXICAL ERRORS ===\n")
            for error in errors:
                self.text_area_output.insert("end", f"{error}\n")
            self.text_area_output.insert("end", "\n")
        
        self.text_area_output.insert("end", "=== RECOGNIZED TOKENS ===\n")
        self.text_area_output.insert("end", f"Total tokens: {len(tokens)}\n")
        for i, token in enumerate(tokens):
            self.text_area_output.insert("end", f"{i+1}: {token['type']} = '{token['value']}'\n")
        
        self.text_area_output.config(state="disabled")

    def analyze_parser_sdt(self):
        """Complete Parser + SDT analysis"""
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Warning", "No code to analyze")
            return
        
        # Execute Parser + SDT
        result = PARSER_C.parse_code(code_content)
        
        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", result)
        self.text_area_output.config(state="disabled")

    def clear_results(self):
        """Clear results area"""
        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.config(state="disabled")

if __name__ == "__main__":
    root = ttk.Window()
    app = CodeAnalyzerApp(root)
    root.mainloop()