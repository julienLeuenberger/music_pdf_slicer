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
        btn_add.grid(row=999, column=0, columnspan=2)

        btn_clear = tk.Button(self.frame, text="Nettoyer tout", command=self.clear_entries)
        btn_clear.grid(row=1000, column=0, columnspan=2)

        btn_export = tk.Button(self.frame, text="💾 Exporter JSON", command=self.export)
        btn_export.grid(row=1001, column=0, columnspan=2)

        btn_load = tk.Button(self.frame, text="Importer JSON", command=self.load_from_json)
        btn_load.grid(row=1002, column=0, columnspan=2)

        btn_add_pdf_in = tk.Button(self.frame, text= "Ajouter PDF IN", command=self.add_pdf_in)
        btn_add_pdf_in.grid(row=1003, column=0, columnspan=2)

        btn_add_folder_out = tk.Button(self.frame, text= "Ajouter Dossier OUT", command=self.add_folder_out)
        btn_add_folder_out.grid(row=1004, column=0, columnspan=2)

        btn_run_cut = tk.Button(self.frame, text= "Découper PDF", command=self.run_cut)
        btn_run_cut.grid(row=1005, column=0, columnspan=2)

    def add_row(self, name="", pages=""):
        row = len(self.entries)
        name_entry = tk.Entry(self.frame, width=30)
        name_entry.insert(0, name)  # Fill with given name if provided
        pages_entry = tk.Entry(self.frame, width=30)
        pages_entry.insert(0, pages)  # Fill with given pages if provided

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
        self.add_voices_to_model()

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Fichiers JSON", "*.json")])
        if path:
            self.controller.export_to_json(path)
            messagebox.showinfo("Succès", "Fichier exporté avec succès !")

    def load_from_json(self):
        path = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
        if path:
            try:
                self.controller.import_from_json(path)
                self.import_voices_from_model()
                messagebox.showinfo("Succès", "Les voix ont été importées avec succès!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def add_pdf_in(self):
        path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])
        self.controller.add_pdf_in(path)

    def add_folder_out(self):
        path = filedialog.askdirectory()
        if path[-1] != "/":
            path = path + "/"
        self.controller.add_folder_output(path)

    def clear_entries(self):
        for name_entry, pages_entry in self.entries:
                name_entry.destroy()
                pages_entry.destroy()
        self.entries.clear()

    def add_voices_to_model(self):
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

    def import_voices_from_model(self):
        self.clear_entries()

        # Get voices from the model
        voices = self.controller.get_voices()

        # Recreate the UI rows for each voice
        for voice in voices:
            name = voice.get("name", "")
            pages = ",".join(map(str, voice.get("pages", [])))  # Convert list to string
            self.add_row(name, pages)

        # If the model is empty, create at least one empty row
        if not voices:
            self.add_row("", "")

    def run_cut(self):
        self.add_voices_to_model()        
        self.controller.run_cut()

    def show_about(self):
        tk.messagebox.showinfo(
            "À propos",
            "Générateur de configuration pour découpage de partitions PDF.\n\n"
            "Créé avec ❤️ en Python.\n"
            "Utilisez Tab pour ajouter rapidement des lignes.\n"
            "Exportez au format JSON compatible avec le script de découpe."
        )
