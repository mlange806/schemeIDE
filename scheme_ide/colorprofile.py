import tkinter as tk
import json

class Colorprofile():
    def update_scheme_text(self, scheme_text):
        scheme_text.configure(foreground=self.colors["text"])
        scheme_text.configure(background=self.colors["background"])
        scheme_text.configure(insertbackground=self.colors["cursor"])
        scheme_text.tag_configure("keyword", foreground=self.colors["keyword"])
        scheme_text.tag_configure("operator", foreground=self.colors["operator"])
        scheme_text.tag_configure("paren_highlight", background=self.colors["paren_highlight"])

    def __init__(self, root):
        # Initialize default colors
        self.colors = dict()
        self.colors["text"] = "white"
        self.colors["background"] = "black"
        self.colors["cursor"] = "blue"
        self.colors["keyword"] = "#0000ff"
        self.colors["operator"] = "#00ff00"
        self.colors["paren_highlight"] = "#633cff"

        # Provides "colorprofile_updated" function
        self.root = root

    def pickcolor(self, tag):
        color = tk.colorchooser.askcolor()[1]
        if color != None:
            self.colors[tag] = color
            self.root.colorprofile_updated()

    def save_profile(self, parent, testMode=False, path=None):
        if not testMode: path = tk.filedialog.asksaveasfilename(parent=parent)
        if path == None or path == "": return

        file = open(path, "w")
        json.dump(self.colors, file)
        file.close()

    def load_profile(self, parent, testMode=False, path=None):
        if not testMode: path = tk.filedialog.askopenfilename(parent=parent)
        if path == None or path == "": return

        file = open(path, "r")
        self.colors = json.load(file)
        file.close()

        self.root.colorprofile_updated()
