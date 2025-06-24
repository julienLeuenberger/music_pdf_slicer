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
├── main.py                   # Entry point
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