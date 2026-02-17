import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from hwctool.view.mainwindow import MainWindow
from hwctool.controller import MainController
from hwctool.view.themes import get_theme

# Setup Logging
def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_file = 'app.log'
    my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, 
                                     backupCount=2, encoding=None, delay=False)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)
    app_log.addHandler(console_handler)
    
    return app_log

def main():
    logger = setup_logging()
    logger.info("Iniciando Halo Wars 2 Casting Tool...")

    app = QApplication(sys.argv)
    app.setApplicationName("HW2 Casting Tool")

    # Initialize Controller and View
    controller = MainController()
    window = MainWindow(controller)
    
    # Connect View and Controller
    controller.set_view(window)
    
    # Apply saved theme
    saved_theme = controller.config_manager.get("theme", "dark")
    window.apply_theme(saved_theme)
    
    window.show()
    logger.info("GUI Iniciada.")

    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Error critico: {e}", exc_info=True)

if __name__ == "__main__":
    main()
