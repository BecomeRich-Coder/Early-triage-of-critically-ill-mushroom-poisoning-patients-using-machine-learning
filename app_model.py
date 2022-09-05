"""
实体类库
"""
from PyQt5.QtWidgets import QTableWidget
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class My_Table_Widget(QTableWidget):
    # 重写快捷键事件
    def keyPressEvent(self, e: QtGui.QKeyEvent):
        super(My_Table_Widget, self).keyPressEvent(e)

        # # 回车键和down键可以实现切换单元格进行编辑，有问题
        # key = e.key()
        # if key == Qt.Key_Enter or key == Qt.Key_Return or key == Qt.Key_Down:
        #     if self.currentRow() + 1 < self.rowCount():
        #         self.setFocus()
        #         self.setCurrentCell(self.currentRow() + 1, self.currentColumn())
        # # up键可以实现切换单元格进行编辑
        # if key == Qt.Key_Up:
        #     if self.currentRow() - 1 >= 0:
        #         self.setCurrentCell(self.currentRow() - 1, self.currentColumn())

        # 按下粘贴键Ctrl+V
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_V:
            text_to_past = QApplication.clipboard().text()
            text_to_past = text_to_past.replace('\t', '\n')  # 可以粘贴行或列数据
            table_row_data = text_to_past.split('\n')
            s = 0
            for i in range(self.currentRow(), self.rowCount()):
                row_data = table_row_data[s]
                item = QtWidgets.QTableWidgetItem()
                item.setText(row_data)
                self.setItem(i, 0, item)
                s += 1