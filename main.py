# main.py

import sys
from PyQt6.QtWidgets import QApplication
from controleur import Controleur

if __name__ == '__main__':
    
    print(f' --- main --- ')
    
    app = QApplication(sys.argv)
    
    # fichier_style = open(sys.path[0] + '/style.qss', 'r')
    # with fichier_style :
    #     qss = fichier_style.read()
    #     # app.setStyleSheet(qss)
    
    controleur = Controleur()
    sys.exit(app.exec())
