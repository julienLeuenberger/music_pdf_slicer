import tkinter as tk
from tkinter import ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk

class SimplePDFViewer(tk.Frame):
    def __init__(self, parent, pdf_path, width=600, height=800):
        super().__init__(parent)
        self.parent = parent
        self.pdf_path = pdf_path
        self.width = width
        self.height = height
        
        # Open the PDF
        self.doc = fitz.open(self.pdf_path)
        self.current_page = 0
        self.total_pages = len(self.doc)
        
        # Create widgets
        self.create_widgets()
        self.show_page()
    
    def create_widgets(self):
        # Navigation frame
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill=tk.X, pady=5)
        
        # Navigation buttons
        self.prev_btn = ttk.Button(nav_frame, text="Previous Page", command=self.prev_page)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(nav_frame, text="Next Page", command=self.next_page)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Page info label
        self.page_label = ttk.Label(nav_frame, text=f"Page 1 of {self.total_pages}")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        # PDF display area
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
    
    def show_page(self):
        # Get the page
        page = self.doc.load_page(self.current_page)
        
        # Render the page as an image
        zoom = 1.0  # You can adjust this for different resolutions
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to ImageTk format
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = self.resize_image(img)
        self.tk_img = ImageTk.PhotoImage(image=img)
        
        # Display on canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        
        # Update page info
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")
        
        # Update button states
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED)
    
    def resize_image(self, img):
        """Resize image to fit canvas while maintaining aspect ratio"""
        img_width, img_height = img.size
        ratio = min(self.width / img_width, self.height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        return img.resize(new_size, Image.LANCZOS)
    
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page()
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()