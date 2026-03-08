"""
Theme stylesheets for the Halo Wars 2 Casting Tool GUI.
Provides Dark and Light theme QSS stylesheets.
"""

DARK_THEME = """
/* === DARK THEME === */
QMainWindow, QWidget#centralWidget {
    background-color: transparent;
}
QWidget {
    color: #cdd6f4;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QTabWidget::pane {
    border: 1px solid #45475a;
    background-color: rgba(30, 30, 46, 120);
    border-radius: 4px;
}
QTabBar::tab {
    background-color: #313244;
    color: #a6adc8;
    padding: 8px 18px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #45475a;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 2px solid #89b4fa;
}
QTabBar::tab:hover:!selected {
    background-color: #45475a;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #89b4fa;
}

QComboBox::drop-down {
    border: none;
    padding-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #585b70;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 4px 8px;
    background-color: #313244;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #45475a;
}

QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    border: 1px solid #585b70;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #585b70;
    border: 1px solid #89b4fa;
}
QPushButton:pressed {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QGroupBox {
    border: 1px solid #45475a;
    background-color: rgba(49, 50, 68, 80);
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #89b4fa;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QLabel {
    color: #cdd6f4;
}

QCheckBox {
    color: #cdd6f4;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #45475a;
    border-radius: 3px;
    background-color: #313244;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border: 1px solid #89b4fa;
    border-radius: 3px;
    image: url(hwctool/view/check_white.svg);
}

QSlider::groove:horizontal {
    height: 6px;
    background: #45475a;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #89b4fa;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::sub-page:horizontal {
    background: #89b4fa;
    border-radius: 3px;
}

QScrollArea {
    border: none;
    background-color: #1e1e2e;
}
QScrollBar:vertical {
    background: #1e1e2e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #585b70;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QListWidget {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}
QListWidget::item:hover:!selected {
    background-color: #45475a;
}

QMessageBox {
    background-color: #1e1e2e;
    color: #cdd6f4;
}
"""

LIGHT_THEME = """
/* === LIGHT THEME === */
QMainWindow, QWidget#centralWidget {
    background-color: transparent;
}
QWidget {
    color: #4c4f69;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QTabWidget::pane {
    border: 1px solid #ccd0da;
    background-color: rgba(239, 241, 245, 120);
    border-radius: 4px;
}
QTabBar::tab {
    background-color: #e6e9ef;
    color: #6c6f85;
    padding: 8px 18px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #ccd0da;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #eff1f5;
    color: #4c4f69;
    border-bottom: 2px solid #1e66f5;
}
QTabBar::tab:hover:!selected {
    background-color: #dce0e8;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #1e66f5;
    selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #1e66f5;
}

QComboBox::drop-down {
    border: none;
    padding-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #bcc0cc;
    selection-background-color: #1e66f5;
    selection-color: #ffffff;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 4px 8px;
    background-color: #ffffff;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #e6e9ef;
}

QPushButton {
    background-color: #e6e9ef;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #dce0e8;
    border: 1px solid #1e66f5;
}
QPushButton:pressed {
    background-color: #1e66f5;
    color: #ffffff;
}

QGroupBox {
    border: 1px solid #ccd0da;
    background-color: rgba(230, 233, 239, 80);
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #1e66f5;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QLabel {
    color: #4c4f69;
}

QCheckBox {
    color: #4c4f69;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #ccd0da;
    border-radius: 3px;
    background-color: #ffffff;
}
QCheckBox::indicator:checked {
    background-color: #1e66f5;
    border: 1px solid #1e66f5;
    border-radius: 3px;
    image: url(hwctool/view/check_white.svg);
}

QSlider::groove:horizontal {
    height: 6px;
    background: #ccd0da;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #1e66f5;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::sub-page:horizontal {
    background: #1e66f5;
    border-radius: 3px;
}

QScrollArea {
    border: none;
    background-color: #eff1f5;
}
QScrollBar:vertical {
    background: #eff1f5;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #ccd0da;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #bcc0cc;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QListWidget {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #1e66f5;
    color: #ffffff;
}
QListWidget::item:hover:!selected {
    background-color: #e6e9ef;
}

QMessageBox {
    background-color: #eff1f5;
    color: #4c4f69;
}
"""

THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}

def get_theme(name):
    """Returns the QSS stylesheet for the given theme name."""
    return THEMES.get(name, DARK_THEME)
