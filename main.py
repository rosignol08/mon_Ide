import os
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtGui import QIcon, QTextCursor,QFont, QColor
from PyQt5.QtCore import Qt
from settings import SettingsWindow


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Charger les paramètres depuis le fichier JSON
        self.settings = self.load_settings()
        
        # Définir la taille de l'indentation depuis les paramètres ou par défaut
        self.tab_size = self.settings.get("editor", {}).get("tabSize", 4)
        self.indentation = " " * self.tab_size
        
        # Définir l'indentation depuis les paramètres ou par défaut
        #self.indentation = " " * self.settings.get("editor", {}).get("tabSize", 4)
        #self.tab_size = self.settings.get("editor", {}).get("tabSize", 4)
        
        # Initialiser l'interface utilisateur
        self.initUI()

        # Définir l'indentation depuis les paramètres ou par défaut
        indentation = self.settings.get("editor", {}).get("tabSize", 4)
        self.indentation = " " * indentation  # Utilisation d'espaces pour l'indentation

        # Zone d'édition de texte avec les paramètres personnalisés
        #self.text_edit = CodeEditor(self, settings=self.settings.get("editor", {}))
        self.text_edit = CodeEditor(self, settings=self.settings.get("editor", {}), indentation=self.indentation)
        self.setCentralWidget(self.text_edit)

        # Appel de la méthode pour créer la barre de menu
        self._create_menu_bar()
    def initUI(self):
        self.setWindowTitle("IDE Personnalisée")
        self.setGeometry(100, 100, 800, 600)

        # Create menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Paramètres")

        # Add settings action
        settings_action = QAction("Ouvrir les paramètres", self)
        #settings_action.setShortcut("Ctrl+P")
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        
        # Zone d'édition de texte avec les paramètres personnalisés
        self.text_edit = QTextEdit(self)
        self.text_edit.setTabStopDistance(self.tab_size * 8)  # Assuming 8 pixels per space
        self.setCentralWidget(self.text_edit)

    #def open_settings(self):
    #    self.settings_window = SettingsWindow(self)
    #    self.settings_window.show()
    #def open_settings(self):
    #    self.settings_window = SettingsWindow(self)
    #    if self.settings_window.exec_() == QDialog.Accepted:
    #        self.settings = self.load_settings()
    #        self.tab_size = self.settings.get("editor", {}).get("tabSize", 4)
    #        self.indentation = " " * self.tab_size
    #        self.text_edit.setTabStopDistance(self.tab_size * 8)  # Assuming 8 pixels per space
    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        if self.settings_window.exec_() == QDialog.Accepted:
            self.reload_settings()

    def reload_settings(self):
        self.settings = self.load_settings()
        self.tab_size = self.settings.get("editor", {}).get("tabSize", 4)
        self.indentation = " " * self.tab_size
        self.text_edit.setTabStopDistance(self.tab_size * 8)  # Assuming 8 pixels per space

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Fichier 'settings.json' introuvable. Utilisation des paramètres par défaut.")
            return {}
    
    def keyPressEvent(self, event):
        # Gestion de la touche Tab pour ajouter une indentation
        if event.key() == Qt.Key_Tab:
            self.insertPlainText(self.indentation)
            return
    
        # Gestion de la touche Enter pour l'indentation automatique
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            current_line = cursor.selectedText().strip()
    
            # Récupère l'indentation de la ligne actuelle
            indentation = ""
            for char in current_line:
                if char == " " or char == "\t":
                    indentation += char
                else:
                    break
                
            # Vérifie si le fichier est un fichier Python et si la ligne se termine par ":"
            if hasattr(self, "current_file") and self.current_file.endswith(".py"):
                if current_line.endswith(":"):
                    indentation += self.indentation  # Ajoute une indentation supplémentaire
    
            # Ajoute une nouvelle ligne avec l'indentation
            super().keyPressEvent(event)
            self.insertPlainText(indentation)
            return
    
        # Garde les autres événements de touche par défaut
        super().keyPressEvent(event)

    def _create_menu_bar(self):
        # Barre de menu
        menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")

        # Action pour ouvrir un fichier
        open_action = QAction(QIcon(), "Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Action pour enregistrer un fichier
        save_action = QAction(QIcon(), "Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Action pour quitter l'application
        exit_action = QAction(QIcon(), "Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Tous les fichiers (*);;Fichiers texte (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.text_edit.setText(file.read())
            self.text_edit.current_file = file_name  # Définir le fichier courant


    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", "", "Tous les fichiers (*);;Fichiers texte (*.txt)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quitter", "Voulez-vous vraiment quitter ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class CodeEditor(QTextEdit):
    def __init__(self, parent=None, settings={}, indentation="    "):
        super().__init__(parent)
        
        # Application des paramètres
        font_family = settings.get("fontFamily", "Courier New")
        font_size = settings.get("fontSize", 12)
        tab_size = settings.get("tabSize", 4)
        
        # Définition de la police
        font = QFont(font_family, font_size)
        self.setFont(font)
        
        # Définition de la taille de tabulation
        self.tab_size = " " * tab_size if settings.get("insertSpaces", True) else "\t"
        
        # Application du thème
        if settings.get("theme", "light") == "dark":
            self.setStyleSheet("background-color: #1e1e1e; color: #d774d4;")
        
        # Indentation à partir de l'argument
        self.indentation = indentation  # Définir l'indentation reçue en paramètre

    def load_indent_rules(self):
        # Charger les règles d'indentation à partir du fichier JSON
        try:
            with open("indent_rules.json", "r") as f:
                rules = json.load(f)
            self.indent_after = set(rules.get("indent_after", []))
            self.indent_decrease = set(rules.get("indent_decrease", []))
        except FileNotFoundError:
            self.indent_after = set()
            self.indent_decrease = set()
            print("Fichier 'indent_rules.json' introuvable.")

    def keyPressEvent(self, event):
        # Gestion de la touche Tab pour ajouter une indentation personnalisée
        if event.key() == Qt.Key_Tab:
            self.insertPlainText(self.tab_size)
            return
    
        # Gestion de la touche Enter pour l'indentation automatique
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            current_line = cursor.selectedText().strip()
    
            # Récupère l'indentation de la ligne actuelle
            base_indentation = ""
            for char in cursor.block().text():
                if char == " " or char == "\t":
                    base_indentation += char
                else:
                    break
                
            # Si la ligne se termine par ":", ajoute une indentation supplémentaire
            if current_line.endswith(":"):
                new_indentation = base_indentation + self.indentation
            else:
                # Sinon, conserve l'indentation de la ligne précédente
                new_indentation = base_indentation
    
            # Ajoute une nouvelle ligne avec l'indentation calculée
            super().keyPressEvent(event)
            self.insertPlainText(new_indentation)
            return
    
        # Garde les autres événements de touche par défaut
        super().keyPressEvent(event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())
