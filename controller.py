from model import VoiceConfigModel
from view.app_view import AppView

class AppController:
    def __init__(self, root):
        self.model = VoiceConfigModel()
        self.view = AppView(root, self)
    
    def add_voice(self, name, pages_str):
        self.model.add_voice(name, pages_str)
    
    def export_to_json(self, path):
        self.model.export_to_json(path)

    def get_voices(self):
        return self.model.voices