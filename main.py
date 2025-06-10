import fitz
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class PDFreader:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Magazine Viewer")

        # Initial theme: light
        self.theme = "light"
        self.set_theme()

        self.current_page = 0
        self.pdf_document = None

        # Load PDF button
        self.load_button = tk.Button(
            root, text="Load PDF", command=self.load_pdf,
            bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_active_bg
        )
        self.load_button.pack(pady=10)

        # Canvas for PDF page
        self.canavas = tk.Canvas(root, width=600, height=800, bg=self.canvas_bg)
        self.canavas.pack()

        # Navigation frame with buttons
        self.nav_frame = tk.Frame(root, bg=self.bg_color)
        self.nav_frame.pack(pady=10)

        self.prev_button = tk.Button(
            self.nav_frame, text="Previous", command=self.prev_page,
            width=10,
            bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_active_bg
        )
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(
            self.nav_frame, text="Next", command=self.next_page,
            width=10,
            bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_active_bg
        )
        self.next_button.grid(row=0, column=1, padx=10)

        # Theme toggle button
        self.theme_button = tk.Button(
            root, text="Toggle Theme", command=self.toggle_theme,
            bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_active_bg
        )
        self.theme_button.pack(pady=10)

        # Page label
        self.page_label = tk.Label(root, text="Page 0 of 0", bg=self.bg_color, fg=self.fg_color)
        self.page_label.pack()

    def set_theme(self):
        if self.theme == "light":
            self.bg_color = "lightblue"
            self.fg_color = "black"
            self.btn_bg = "white"
            self.btn_fg = "black"
            self.btn_active_bg = "#d9d9d9"
            self.canvas_bg = "lightgray"
        else:  # dark theme
            self.bg_color = "#2e2e2e"
            self.fg_color = "white"
            self.btn_bg = "#444444"
            self.btn_fg = "white"
            self.btn_active_bg = "#666666"
            self.canvas_bg = "#1e1e1e"

        self.root.configure(bg=self.bg_color)

    def update_widget_colors(self):
        # Update colors for all widgets
        self.root.configure(bg=self.bg_color)
        self.canavas.configure(bg=self.canvas_bg)
        self.nav_frame.configure(bg=self.bg_color)
        self.page_label.configure(bg=self.bg_color, fg=self.fg_color)

        for btn in [self.load_button, self.prev_button, self.next_button, self.theme_button]:
            btn.configure(bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_active_bg)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.set_theme()
        self.update_widget_colors()

    def load_pdf(self):
        file_path = filedialog.askopenfile(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)
                self.current_page = 0
                self.display_page(self.current_page)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {e}")
                self.pdf_document = None

    def display_page(self, page_num):
        if not self.pdf_document:
            messagebox.showerror("Error", "No PDF loaded")
            return

        self.canavas.delete("all")

        page = self.pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        default_width = 600
        scale_factor = default_width / pix.width
        new_width = default_width
        new_height = int(pix.height * scale_factor)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)
        self.canavas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Update page label
        self.page_label.config(text=f"Page {self.current_page + 1} of {len(self.pdf_document)}")

    def next_page(self):
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def prev_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFreader(root)
    root.mainloop()