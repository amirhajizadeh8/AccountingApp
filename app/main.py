#Entry‑point of the AccountingApp.

import sys
from pathlib import Path
from PySide2.QtCore import Qt
from PySide2.QtGui import QFontDatabase, QFont
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QTextStream

# ────────────────────────────────────────────────────────────────────────────
# local import – Main UI shell (tabs)
# path: app/ui/main_window.py   (the file you already have in Canvas)
# ────────────────────────────────────────────────────────────────────────────
from app.ui.main_window import MainWindow  # << corrected absolute import

# ---------------------------------------------------------------------------
# helper: load custom font (Vazir.ttf) if exists
# ---------------------------------------------------------------------------

def _load_vazir_font(app: QApplication) -> None:
    """Load Vazir.ttf from resources/fonts and apply it globally."""
    font_path = (
        Path(__file__).resolve().parent.parent / "resources" / "fonts" / "Vazir.ttf"
    )
    if font_path.exists():
        fid = QFontDatabase.addApplicationFont(str(font_path))
        if fid != -1:
            fam = QFontDatabase.applicationFontFamilies(fid)[0]
            app.setFont(QFont(fam, 11))


# ---------------------------------------------------------------------------
# helper: apply minimal QSS purple/white theme (optional)
# ---------------------------------------------------------------------------

def apply_stylesheet(app):
    style_file = QFile("resources/styles/style.qss")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())

# ---------------------------------------------------------------------------
# main entry
# ---------------------------------------------------------------------------

def main() -> None:
    """Initialise QApplication, apply styling, launch MainWindow."""
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    ...


    # RTL for whole UI
    app.setLayoutDirection(Qt.RightToLeft)

    # font + style
    _load_vazir_font(app)


    # show main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
