# Kami menggunakan Sphinx utk documentation API
project = "SONI-128 API"
author = "Kelompok 07 - IF4020 Kriptografi"
copyright = "2026, Kelompok 07 IF4020"
release = "1.0"

extensions = []

language = "id"
exclude_patterns = ["_build"]
templates_path = []

html_theme = "furo"
html_title = "SONI-128 API Documentation"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/indahtangdililing/IF4020_Tugas2_07",  
}

autodoc_typehints = "description"
add_module_names = False
python_use_unqualified_type_names = True
