import fitz
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog,messagebox


class PDFreader:
    def __init__(self,root):
        self.root = root
        self.root.title("Digital Magazine Viewer")
        self.current_page = 0
        self.zoom_level = 1
        
        self.pdf_document = None
        
        self.load_button = tk.Button(root, text="Load PDF", command=self.load_pdf)
        self.load_button.pack()
        
        self.canavas = tk.Canvas(root, width=600,height=800)
        self.canavas.pack()        
        
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(pady=10)
        
        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_page)
        self.prev_button.grid(row=0,column=0,padx=5)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_page)
        self.next_button.grid(row=0,column=1,padx=5)
        
    def load_pdf(self):

        file_path = filedialog.askopenfile(filetypes=[("PDF files","*.pdf")])
        
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)
                self.current_page = 0
                self.display_page(self.current_page)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {e}")
                self.pdf_document = None
                
        
    def display_page(self,page_num):
        
        if not self.pdf_document:
            messagebox.showerror("Error","No PDF loaded")
            return
        
        
        self.canavas.delete("all")
        
        page = self.pdf_document.load_page(page_num)
        pix = page.get_pixmap() 
        img = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
        canvas_width = self.canavas.winfo_width()
        canvas_height = self.canavas.winfo_height()
        
        scale_factor = min(canvas_width / pix.width, canvas_height / pix.height)
        
        new_width = int(pix.width * scale_factor)
        new_height = int(pix.height * scale_factor)
        img = img.resize((new_width,new_height),Image.LANCZOS)
        
        self.img_tk = ImageTk.PhotoImage(img)
        self.canavas.create_image(0,0, anchor=tk.NW, image=self.img_tk)
         
         
         
    def next_page(self):
        if self.pdf_document and self.current_page < len(self.pdf_document) -1:
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