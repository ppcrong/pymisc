class uilib:

    @staticmethod
    def get_text_size(font_name: str, font_size: int, text: str):
        """
        get text size w/h
        """

        from PyQt5.QtGui import QFontMetrics
        from PyQt5.QtGui import QFont
        font = QFont(font_name, font_size)
        fm = QFontMetrics(font)
        width = fm.width(text)
        height = fm.height()
        return width, height

    @staticmethod
    def get_elided_text(font=None, font_name: str = 'Arial', font_size: int = 12, text: str = None,
                        ui_width: int = None):
        """
        get elided text by elide left
        """

        from PyQt5.QtGui import QFontMetrics
        from PyQt5.QtGui import QFont

        if not font:
            font = QFont(font_name, font_size)
        fm = QFontMetrics(font)
        width, _ = uilib.get_text_size(font_name, font_size, text)
        if width > ui_width:
            from PyQt5.QtCore import Qt
            ret_text = fm.elidedText(text, Qt.ElideLeft, ui_width)
        else:
            ret_text = text
        return ret_text
