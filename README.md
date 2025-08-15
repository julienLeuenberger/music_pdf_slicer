# MUSIC PDF SLICER
## Tkinter vs NiceGUI
- Tkinter is sufficient for this application

## Tkinter with docker
- It needs a X11server for Windows, it is not so simple

## Cross compatibility
- Developp all with Windows, Python, Tkinter and venv
- Send to someone with MAC to compile

## Language
- English
- French
- German

## Development
- CI/CD
- Beta version

## Model-View-Controller
```bash
partition_splitter_gui/
├── main.py                  # Entry point
├── controller.py            # Control Logic: link view and model
├── model.py                 # Data structure
├── view/
│   ├── __init__.py
│   ├── app_view.py          # Main window, champs, layout Tkinter
│   └── widgets.py           # For special component if needed
├── utils/
│   └── pdf_utils.py         # PDF tools
└── data/
    └── *.json  # datas
```

## Example files
To avoid any problem with pyinstaller and everything, just deliver:
- main.exe
- data/jsons/diane.json
- data/pdf_in/Diane.pdf
- data/outputs/outputs_here.txt
- manual.pdf to do


## To Do

### GUI
- Improves the button alingment
- Say something when the cut is done, like a status message box
### Functionnalities
- PyPDF extract text?
### Code
- Enhance every paths
- Secure the entry
- GUI strategy on Python book
- Get logs everywhere
### Documentation
- Add a linter
- Document the method
- Make a manual.pdf (latex of course), one .tex for all languages
### Test
- Test a lot
- Test procedure for new features
### Branding
- Add logo
- Buy me a coffee or buy me a reed
- Email address with domain
