from model import VoiceConfigModel
from view.app_view import AppView
import json

class AppController:
    def __init__(self, root):
        self.model = VoiceConfigModel()
        self.view = AppView(root, self)
        self.model.attach(self.view)
    
    def add_voice(self, name, pages_str):
        self.model.add_voice(name, pages_str)

    def get_voices(self):
        return self.model.get_voices()
    
    def export_to_json(self, path):
        self.model.export_to_json(path)

    def import_from_json(self, path):
        self.model.import_from_json(path)

    def get_voices(self):
        return self.model.voices
    
    def add_pdf_in(self, path):
        self.model.add_path_pdf(filepath=path)

    def get_path_pdf(self):
        return self.model.get_path_pdf()

    def add_output_folder(self, folder_output):
        self.model.add_output_folder(folder_output)

    def run_cut(self):
        self.model.run_cut()

    def clear_states(self):
        self.model.clear_state_pdf_in()
        self.model.clear_state_output_folder()