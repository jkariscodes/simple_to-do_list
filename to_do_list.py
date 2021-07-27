"""
/***************************************************************************
Name                 : PyQt To Do List
Description          : A simple to-do list application for your desktop.
Date                 : 15/July/2021
copyright            : (C) 2021 by Joseph Kariuki
email                : joehene@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the stated license; or any later version.       *                             *
 *                                                                         *
 ***************************************************************************/
"""

import sys
import sqlite3
from sqlite3 import Error
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QListWidget,
    QMessageBox
)


class ToDoDB:
    """
    Container that handles the database operations.
    """
    def __init__(self):
        try:
            # Create database connection
            self._con = sqlite3.connect('to_do.db')
            # Create SQLite3 cursor and create table
            self._cursor = self._con.cursor()
            self._cursor.execute(
                "CREATE TABLE if not exists todo_tbl(todo_list_item text)"
            )
            # Commit changes and close connection.
            self._con.commit()
        except Error:
            # Show message box with error notification.
            QMessageBox.critical(
                self,
                'To Do List App',
                str(Error)
            )

    def fetch_items(self):
        """
        Fetch items from the database.
        """
        # Execute SQL query.
        self._cursor.execute(
            "SELECT * FROM todo_tbl"
        )
        # Fetch all items in the database
        all_items = self._cursor.fetchall()
        # Commit the changes to the database
        self._con.commit()
        self._con.close()
        return all_items

    def save_all_items(self, item):
        """
        Save newly added to do items in the database.
        :param item: To do item.
        :type item: str
        """
        self._cursor.execute(
            "INSERT INTO todo_tbl VALUES (:item)", {'item': item.text()}
        )
        # Commit changes to the database.
        self._con.commit()
        self._con.close()


class ToDOApp(QMainWindow):
    """
    To Do application user interface.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('To Do Application')
        self.setFixedSize(400, 400)
        # Set the widgets
        self.vbox_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.vbox_layout)
        # Creating the user interface controls
        self._init_ui()
        # Load items for the database
        self.get_db_items()

    def _init_ui(self):
        """
        Create user interface controls and properties.
        """
        # Create line edit and set GUI properties
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText('Type here...')
        self.line_edit.setFixedHeight(30)
        self.line_edit.setAlignment(Qt.AlignLeft)
        # Create buttons
        self.add_btn = QPushButton('Add')
        self.delete_btn = QPushButton('Delete')
        self.save_btn = QPushButton('Save')
        self.clear_btn = QPushButton('Clear')
        self.close_btn = QPushButton('Close')
        # Create button grid layout and add buttons
        button_layout = QGridLayout()
        button_layout.addWidget(self.add_btn, 0, 0)
        button_layout.addWidget(self.delete_btn, 0, 2)
        button_layout.addWidget(self.save_btn, 0, 1)
        button_layout.addWidget(self.clear_btn, 0, 3)
        button_layout.addWidget(self.close_btn, 0, 4)
        # Add a list widget to show added/saved items
        self.list_widget = QListWidget()
        # Add widgets and layouts to the main layout.
        self.vbox_layout.addWidget(self.line_edit)
        self.vbox_layout.addLayout(button_layout)
        self.vbox_layout.addWidget(self.list_widget)
        # Connect the signals to their slots.
        self._connect_signals()

    def _connect_signals(self):
        """
        Connect signals to their slots.
        """
        self.add_btn.clicked.connect(self.on_add_item)
        self.save_btn.clicked.connect(self.on_save_items)
        self.delete_btn.clicked.connect(self.on_delete_item)
        self.clear_btn.clicked.connect(self.on_clear_item)
        self.close_btn.clicked.connect(self.on_close)

    def on_add_item(self):
        """
        Slot raised when add item button is clicked and ddd item to the list
        of to do items.
        """
        item = self.line_edit.text()
        # Check if the line edit is without text
        if item == " " or item == "":
            QMessageBox.warning(
                self,
                'To Do List App',
                'Cannot add an empty item'
            )
        self.list_widget.addItem(item)
        # Clear item entry.
        self.line_edit.setText("")

    def on_save_items(self):
        """
        Slot raised when add item button is clicked and save to do items in
        the database.
        """
        items = []
        for item in range(self.list_widget.count()):
            items.append(self.list_widget.item(item))

        if len(items) == 0:
            QMessageBox.warning(
                self,
                'To Do List App',
                'Cannot save empty item'
            )
        else:
            for item in items:
                ToDoDB().save_all_items(item)

            self.list_widget.clear()

    def get_db_items(self):
        """
        Get items fetched
        from the database.
        """
        saved_items = ToDoDB().fetch_items()
        for item in saved_items:
            self.list_widget.addItem(item[0])

    def on_delete_item(self):
        """
        Slot raised when add item button is clicked and remove items from
        list of to do items.
        """
        clicked = self.list_widget.currentRow()
        self.list_widget.takeItem(clicked)

    def on_clear_item(self):
        """
        Slot raised when add item button is clicked and clear all items in
        the list widget.
        """
        self.list_widget.clear()

    def on_close(self):
        """
        Slot raised when close button is clicked.
        """
        self.close()

    def closeEvent(self, event):
        """
        Initiates a closing event for the Window.
        :param event:
        :type event:
        """
        reply = QMessageBox.question(
            self,
            'To Do List App',
            'Are you sure you want to quit the app?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    to_do_app = QApplication(sys.argv)
    to_do_ui = ToDOApp()
    to_do_ui.show()
    sys.exit(to_do_app.exec())
