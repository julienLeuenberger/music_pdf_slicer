import os
import json
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from utils import Observer, Subject
from typing import List

class VoiceConfigModel(Subject):
    def __init__(self):
        self.voices = []
        self.path_pdf_in = ""
        self.path_folder_output = ""

        self._state_pdf_in_set = False
        self._state_output_folder_set = False

        self._observers: List[Observer] = []

    def attach(self, observer:Observer)->None:
        self._observers.append(observer)

    def detach(self, observer:Observer)->None:
        self._observers.remove(observer)

    def notify(self)->None:
        for observer in self._observers:
            observer.update(self)

    def add_voice(self, name, pages_str):
        pages = self.parse_pages(pages_str)
        self.voices.append({"name": name, "pages": pages})

    def get_voices(self):
        return self.voices

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

    def import_from_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Invalid JSON format: expected a list of voices.")

        self.voices.clear()

        for item in data:
            if not isinstance(item, dict) or "name" not in item or "pages" not in item:
                raise ValueError(f"Invalid voice entry: {item}")

            # Convertir la liste de pages en chaîne "1,2,3"
            if isinstance(item["pages"], list):
                pages_str = ",".join(map(str, item["pages"]))
            else:
                pages_str = str(item["pages"])

            self.add_voice(item["name"], pages_str)

    def add_path_pdf(self, filepath):
        self.path_pdf_in = filepath
        self._state_pdf_in_set = True
        self.notify()

    def get_path_pdf(self):
        if self._state_pdf_in_set:
            return self.path_pdf_in
        else:
            raise ValueError("No pdf path set!")

    def clear_state_pdf_in(self):
        self.path_pdf_in = ""
        self._state_pdf_in_set = False
        self.notify()

    def add_output_folder(self, path_folder_output):
        self.path_folder_output = path_folder_output
        self._state_output_folder_set = True
        self.notify()

    def clear_state_output_folder(self):
        self.path_folder_output = ""
        self._state_output_folder_set = False
        self.notify()

    def run_cut(self):
        # first create a json
        file_temp_json = self.path_pdf_in.split(".")[0]+".json"
        self.export_to_json(file_temp_json)

        if self.path_folder_output == "":
            print("Error")
        else:
            self.pdf_splitting(file_temp_json, self.path_pdf_in, self.path_folder_output)

        # delete file_temp_json
        os.remove(file_temp_json)

    def pdf_splitting(self, file_temp_json, path_pdf_in, path_folder_output):
        path = path_pdf_in
        path_to_save = path_folder_output

        name_sheet = path_pdf_in.split("/")[-1]
        name_sheet = name_sheet.split(".")[0]

        json_file = file_temp_json

        """
        print(f"path = {path}")
        print(f"path_to_save = {path_to_save}")
        print(f"name_sheet = {name_sheet}")
        print(f"json_file = {json_file}")
        """
        
        # Create the folder if it does not exist
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        
        
        # Read instruments from JSON file
        with open(json_file, 'r') as f:
            instruments_data = json.load(f)

        # Define the names of the pdfs
        class Instrument:
            def __init__(self, name, page):
                '''
                name: string
                page: int or list of ints
                '''
                self.name = name
                self.page = page

        # Create a list of instruments
        instruments = []
        for instrument_data in instruments_data:
            # if there is only one page per instrument
            if isinstance(instrument_data['pages'], int):
                instruments.append(Instrument(instrument_data['name'], [instrument_data['pages']]))
            # if there are multiple pages per instrument
            else:
                instruments.append(Instrument(instrument_data['name'], instrument_data['pages']))

        # Open the pdf
        with open(path, "rb") as f:
            pdf = PdfReader(f)

            # Loop over the instruments
            for instrument in instruments:
                # Create a new pdf
                pdf_writer = PdfWriter()

                # Loop over the pages for the current instrument
                for page_num in instrument.page:
                    # Extract the page
                    page = pdf.pages[page_num - 1]
                    # Add the page to the pdf
                    pdf_writer.add_page(page)

                # Create the name of the pdf
                pdf_name = name_sheet + '_' + instrument.name + ".pdf"

                # Create the path to the pdf
                pdf_path = os.path.join(path_to_save, pdf_name)

                # Save the pdf
                with open(pdf_path, "wb") as f:
                    pdf_writer.write(f)

