from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
import sys

tick = QtGui.QImage("tick.png")

class TodoModel(QtCore.QAbstractListModel):
	def __init__(self, *args, todos=None, **kwargs):
		super(TodoModel, self).__init__(*args, **kwargs)
		self.todos = todos or []

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole:
			_, text = self.todos[index.row()]
			return text
		
		if role == QtCore.Qt.DecorationRole:
			status,_ = self.todos[index.row()]
			if status:
				return tick
		
	def rowCount(self, index):
		return len(self.todos)

def add(window):
	text = window.txt_todo.text().strip()
	if text:
		window.model.todos.append((False, text))
		window.model.layoutChanged.emit()
		window.txt_todo.setText("")

def delete(window):
	indexes = window.view_todo.selectedIndexes()
	for index in indexes:
		window.model.todos[index.row()] = None
	window.model.todos = [x for x in window.model.todos if x is not None]
	window.model.layoutChanged.emit()
	window.view_todo.clearSelection()

def complete(window):
	indexes = window.view_todo.selectedIndexes()
	if not indexes: return
	for index in indexes:
		row = index.row()
		_, text = window.model.todos[row]
		window.model.todos[row] = (True, text)
	window.model.dataChanged.emit(index, index)

def incomplete(window):
	indexes = window.view_todo.selectedIndexes()
	if not indexes: return
	for index in indexes:
		row = index.row()
		_, text = window.model.todos[row]
		window.model.todos[row] = (False, text)
	window.model.dataChanged.emit(index, index)


app = QtWidgets.QApplication(sys.argv)

window = QtUiTools.QUiLoader().load("mainwindow.ui")
window.model = TodoModel(todos=[(False,"Eat"),(False,"Pray"),(False,"Love"),(True, "Poop pants")])
window.view_todo.setModel(window.model)
window.btn_add.pressed.connect(lambda: add(window))
window.btn_delete.pressed.connect(lambda: delete(window))
window.btn_complete.pressed.connect(lambda: complete(window))
window.btn_incomplete.pressed.connect(lambda: incomplete(window))
window.show()

app.exec_()