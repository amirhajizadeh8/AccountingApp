from PySide2.QtWidgets import QTabBar, QStyleOptionTab, QStyle
from PySide2.QtGui import QPainter
from PySide2.QtCore import QSize, Qt


class RightTabBar(QTabBar):
    """تب‌بار عمودی در سمت راست با متن افقی راست‌به‌چپ."""

    def tabSizeHint(self, index):
        s = super().tabSizeHint(index)
        return QSize(120, 40)

    def paintEvent(self, event):
        painter = QPainter(self)
        opt = QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(opt, index)
            rect = self.tabRect(index)

            # رسم پس‌زمینه تب به صورت استاندارد
            self.style().drawControl(QStyle.CE_TabBarTabShape, opt, painter, self)

            # رسم متن با راست‌چین
            painter.save()
            painter.setPen(opt.palette.buttonText().color())
            painter.drawText(rect.adjusted(8, 0, -8, 0),
                             Qt.AlignVCenter | Qt.AlignRight,
                             opt.text)
            painter.restore()
