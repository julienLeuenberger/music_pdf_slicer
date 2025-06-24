import tkinter as tk
from tkinter import filedialog, messagebox

class AppView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Music PDF Slicer")
        self.entries = []

        self.setup_ui()

    def setup_ui(self):
        menubar = tk.Menu(self.root)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="À propos", command=self.show_about)

        menubar.add_cascade(label="❓ Aide", menu=help_menu)

        self.root.config(menu=menubar)

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.add_row()

        btn_add = tk.Button(self.frame, text="➕ Ajouter voix", command=self.add_row)
        btn_add.grid(row=999, column=0, columnspan=2, pady=5)

        btn_export = tk.Button(self.frame, text="💾 Exporter JSON", command=self.export)
        btn_export.grid(row=1000, column=0, columnspan=2)

    def add_row(self):
        row = len(self.entries)
        name_entry = tk.Entry(self.frame, width=30)
        pages_entry = tk.Entry(self.frame, width=30)

        name_entry.grid(row=row, column=0, padx=5, pady=2)
        pages_entry.grid(row=row, column=1, padx=5, pady=2)

        # Link Tab to page field to add one row
        pages_entry.bind("<Tab>", self.on_tab_pressed)
        pages_entry.bind("<FocusIn>", lambda e: pages_entry.select_range(0, 'end'))

        self.entries.append((name_entry, pages_entry))


    def on_tab_pressed(self, event):
        widget = event.widget
        last_name, last_pages = self.entries[-1]
        
        # If we press tab
        if widget == last_pages:
            self.add_row()
            self.entries[-1][0].focus_set()
            return "break"  # Avoid double jump

    def export(self):
        self.controller.model.voices = []  # reset before export
        for name_entry, pages_entry in self.entries:
            name = name_entry.get().strip()
            pages = pages_entry.get().strip()
            if name and pages:
                try:
                    self.controller.add_voice(name, pages)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur sur '{name}': {e}")
                    return

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Fichiers JSON", "*.json")])
        if path:
            self.controller.export_to_json(path)
            messagebox.showinfo("Succès", "Fichier exporté avec succès !")

    def show_about(self):
        tk.messagebox.showinfo(
            "À propos",
            "Générateur de configuration pour découpage de partitions PDF.\n\n"
            "Créé avec ❤️ en Python.\n"
            "Utilisez Tab pour ajouter rapidement des lignes.\n"
            "Exportez au format JSON compatible avec le script de découpe."
        )
