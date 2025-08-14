from model import VoiceConfigModel
from view.app_view import AppView
import json

class AppController:
    def __init__(self, root):
        self.model = VoiceConfigModel()
        self.view = AppView(root, self)
    
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

    def add_folder_output(self, folder_output):
        self.model.add_folder_output(folder_output)

    def run_cut(self):
        self.model.run_cut()