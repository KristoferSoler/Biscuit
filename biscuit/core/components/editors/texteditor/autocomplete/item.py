import tkinter as tk

from .kind import Kind
from core.components.utils import Frame

class AutoCompleteItem(Frame):
    def __init__(self, master, text, kind=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(width=400, **self.base.theme.editors.autocomplete)
        
        self.text = text
        self.kind = kind

        self.kindw = Kind(self, self.master.autocomplete_kinds, kind)
        self.textw = tk.Text(self, 
            font=('Consolas', 11), **self.base.theme.editors.autocomplete.item,
            relief=tk.FLAT, highlightthickness=0, width=30, height=1)
        self.textw.insert(tk.END, text)
        self.textw.config(state=tk.DISABLED)

        self.textw.tag_config("term", foreground="#dc8c34")
        
        self.kindw.bind("<Button-1>", self.on_click)
        self.textw.bind("<Button-1>", self.on_click)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.off_hover)

        self.selected = False
        self.hovered = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.kindw.grid(row=0, column=0, sticky=tk.NSEW)
        self.textw.grid(row=0, column=1, sticky=tk.NSEW)
    
    def get_text(self):
        return self.text
    
    def get_kind(self):
        return self.kind

    def mark_term(self, term):
        start_pos = self.text.find(term)
        end_pos = start_pos + len(term)
        self.textw.tag_remove("term", 1.0, tk.END)
        self.textw.tag_add("term", f"1.{start_pos}", f"1.{end_pos}")
    
    def on_click(self, *args):
        self.master.choose(self)
    
    def on_hover(self, *args):
        if not self.selected:
            self.kindw.config(bg="#f2f2f2")
            self.textw.config(bg="#f2f2f2")
            self.hovered = True

    def off_hover(self, *args):
        if not self.selected:
            self.kindw.config(bg="#f8f8f8")
            self.textw.config(bg="#f8f8f8")
            self.hovered = False
    
    def toggle_selection(self):
        if self.selected:
            self.select()
        else:
            self.deselect()

    def select(self):
        self.kindw.config(bg="#e8e8e8")
        self.textw.config(bg="#e8e8e8", fg="black")
        self.selected = True
    
    def deselect(self):
        self.kindw.config(bg="#f8f8f8")
        self.textw.config(bg="#f8f8f8", fg="#717171")
        self.selected = False