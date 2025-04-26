import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget, 
                             QListWidgetItem, QCheckBox, QMessageBox, QLabel,
                             QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.todo_file = "todo_data.json"
        self.tasks = []
        self.initUI()
        self.loadTasks()
        
    def initUI(self):
        # Main window setup
        self.setWindowTitle('Todo List')
        self.setGeometry(300, 300, 400, 500)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header 
        header_label = QLabel("Todo List")
        header_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # Input area
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Enter a new task...')
        add_button = QPushButton('Add Task')
        add_button.clicked.connect(self.add_task)
        self.task_input.returnPressed.connect(self.add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)
        main_layout.addLayout(input_layout)
        
        # Task list
        self.task_list = QListWidget()
        self.task_list.setAlternatingRowColors(True)
        self.task_list.setSpacing(2)
        main_layout.addWidget(self.task_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        delete_button = QPushButton('Delete Selected')
        delete_button.clicked.connect(self.delete_selected)
        clear_button = QPushButton('Clear All')
        clear_button.clicked.connect(self.clear_all)
        
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage('Ready')
        
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            # Create task dict
            task = {"text": task_text, "completed": False}
            self.tasks.append(task)
            
            # Add to list widget
            self.add_task_to_list(task)
            
            # Clear the input field
            self.task_input.clear()
            
            # Save tasks
            self.saveTasks()
            self.statusBar().showMessage('Task added')
        else:
            QMessageBox.warning(self, 'Empty Task', 'Please enter a task.')
    
    def add_task_to_list(self, task):
        # Create a list widget item
        item = QListWidgetItem()
        self.task_list.addItem(item)
        
        # Create a widget to hold the task layout
        task_widget = QWidget()
        layout = QHBoxLayout(task_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Add checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(task["completed"])
        checkbox.stateChanged.connect(lambda state, item=item: self.update_task_style(item, state))
        layout.addWidget(checkbox)
        
        # Add task text
        task_label = QLineEdit(task["text"])
        task_label.setReadOnly(True)
        task_label.setFixedHeight(25)  # Ensure consistent height
        
        # Apply style based on completed status
        if task["completed"]:
            task_label.setStyleSheet('text-decoration: line-through; border: none; background: transparent;')
        else:
            task_label.setStyleSheet('border: none; background: transparent;')
            
        layout.addWidget(task_label)
        
        # Set the item widget
        item.setSizeHint(task_widget.sizeHint())
        self.task_list.setItemWidget(item, task_widget)
    
    def update_task_style(self, item, state):
        # Get the index of the item
        index = self.task_list.row(item)
        
        # Update the task data
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = (state == Qt.Checked)
            
            # Get the task widget
            task_widget = self.task_list.itemWidget(item)
            
            # Find the QLineEdit (task text) within the layout
            task_text = None
            for i in range(task_widget.layout().count()):
                widget = task_widget.layout().itemAt(i).widget()
                if isinstance(widget, QLineEdit):
                    task_text = widget
                    break
            
            # Update the style
            if task_text:
                if state == Qt.Checked:
                    task_text.setStyleSheet('text-decoration: line-through; border: none; background: transparent;')
                else:
                    task_text.setStyleSheet('border: none; background: transparent;')
            
            # Save tasks
            self.saveTasks()
            self.statusBar().showMessage('Task updated')
    
    def delete_selected(self):
        # Get all selected items
        selected_items = self.task_list.selectedItems()
        
        if not selected_items:
            QMessageBox.information(self, 'No Selection', 'Please select a task first.')
            return
        
        # Remove items in reverse order to avoid index shifting problems
        for item in reversed(selected_items):
            index = self.task_list.row(item)
            
            # Remove from data
            if 0 <= index < len(self.tasks):
                self.tasks.pop(index)
            
            # Remove from UI
            self.task_list.takeItem(index)
        
        # Save tasks
        self.saveTasks()
        self.statusBar().showMessage('Task(s) deleted')
    
    def clear_all(self):
        confirmation = QMessageBox.question(
            self, 'Confirm Clear All', 
            'Are you sure you want to clear all tasks?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            self.task_list.clear()
            self.tasks = []
            self.saveTasks()
            self.statusBar().showMessage('All tasks cleared')
    
    def loadTasks(self):
        try:
            if os.path.exists(self.todo_file):
                with open(self.todo_file, 'r') as file:
                    self.tasks = json.load(file)
                    
                    # Add tasks to UI
                    for task in self.tasks:
                        self.add_task_to_list(task)
                    
                    self.statusBar().showMessage(f'Loaded {len(self.tasks)} tasks')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load tasks: {str(e)}')
    
    def saveTasks(self):
        try:
            with open(self.todo_file, 'w') as file:
                json.dump(self.tasks, file)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to save tasks: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()