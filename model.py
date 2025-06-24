import json

class VoiceConfigModel:
    def __init__(self):
        self.voices = []

    def add_voice(self, name, pages_str):
        pages = self.parse_pages(pages_str)
        self.voices.append({"name": name, "pages": pages})

    def parse_pages(self, pages_str):
        pages = []
        for part in pages_str.split(','):
            if '-' in part:
                start, end = map(int, part.strip().split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(part.strip()))
        return pages

    def export_to_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.voices, f, indent=4)