# FILE: settings.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton
import json

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Paramètres")
        
        layout = QVBoxLayout()

        # Indentation size setting
        self.indentation_label = QLabel("Taille de l'indentation:")
        self.indentation_spinbox = QSpinBox()
        self.indentation_spinbox.setRange(1, 8)
        self.indentation_spinbox.setValue(parent.settings.get("editor", {}).get("tabSize", 4))  # Default value

        layout.addWidget(self.indentation_label)
        layout.addWidget(self.indentation_spinbox)

        # Theme selection setting
        self.theme_label = QLabel("Choisir un thème:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Clair", "Sombre"])
        self.theme_combobox.setCurrentText(parent.settings.get("editor", {}).get("theme", "Clair"))

        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combobox)

        # Save button
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        indentation_size = self.indentation_spinbox.value()
        selected_theme = self.theme_combobox.currentText()
        
        # Save the settings to a JSON file
        settings = {
            "editor": {
                "tabSize": indentation_size,
                "theme": selected_theme
            }
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        
        self.parent.settings = settings
        self.accept()