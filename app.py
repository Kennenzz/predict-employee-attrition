import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QScrollArea, QComboBox, QMainWindow, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer

import socket_client
import rsa


class ScrollableLabel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.layout = QVBoxLayout(self.content_widget)
        self.setWidget(self.content_widget)

        self.chat_history = QLabel()
        self.chat_history.setWordWrap(True)
        self.layout.addWidget(self.chat_history)

        self.scroll_to_point = QLabel()
        self.layout.addWidget(self.scroll_to_point)

    def update_chat_history(self, message):
        self.chat_history.setText(self.chat_history.text() + '\n' + message)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

class ConnectPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        prev = {'ip': '', 'port': '', 'username': ''}
        if os.path.isfile('prev_details.txt'):
            with open('prev_details.txt', 'r') as f:
                d = f.read().split(",")
                prev = {'ip': d[0], 'port': d[1], 'username': d[2]}

        layout.addWidget(QLabel("IP: "), 0, 0)
        self.ip = QLineEdit(prev['ip'])
        layout.addWidget(self.ip, 0, 1)

        layout.addWidget(QLabel("Port: "), 1, 0)
        self.port = QLineEdit(prev['port'])
        layout.addWidget(self.port, 1, 1)

        layout.addWidget(QLabel("Username: "), 2, 0)
        self.username = QLineEdit(prev['username'])
        layout.addWidget(self.username, 2, 1)

        self.join_btn = QPushButton("Join")
        self.join_btn.clicked.connect(self.join_button)
        layout.addWidget(self.join_btn, 3, 0, 1, 2)

    def join_button(self):
        ip = self.ip.text()
        port = self.port.text()
        username = self.username.text()

        with open('prev_details.txt', 'w') as f:
            f.write(f'{ip},{port},{username}')

        info = f'Trying to join {ip}:{port} as {username}'
        chat_app.info_page.update_info(info)
        chat_app.stack.setCurrentIndex(1)

        QTimer.singleShot(1000, self.connect)

    def connect(self):
        port = int(self.port.text())
        ip = self.ip.text()
        username = self.username.text()

        if not socket_client.connect(ip, port, username, show_error):
            return
        else:
            chat_app.create_chat_page()
            chat_app.stack.setCurrentIndex(2)


class InfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.message = QLabel(alignment=Qt.AlignCenter)
        self.layout.addWidget(self.message)

    def update_info(self, message):
        self.message.setText(message)


class ChatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.history = ScrollableLabel()
        layout.addWidget(self.history)

        self.new_message = QLineEdit()
        layout.addWidget(self.new_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.send_btn)

        self.users_list = QComboBox()
        layout.addWidget(self.users_list)

        socket_client.start_listening(self.incoming_message, show_error)

    def send_message(self):
        message = self.new_message.text()
        self.new_message.clear()

        if message:
            username = chat_app.connect_page.username.text()
            self.history.update_chat_history(f'{username} > {message}')
            socket_client.send(message, {'user': self.users_list.currentText(), 'key': ''})

    def incoming_message(self, username, message):
        self.history.update_chat_history(f'{username} > {message}')


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.connect_page = ConnectPage()
        self.stack.addWidget(self.connect_page)

        self.info_page = InfoPage()
        self.stack.addWidget(self.info_page)

    def create_chat_page(self):
        self.chat_page = ChatPage()
        self.stack.addWidget(self.chat_page)


def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.stack.setCurrentIndex(1)
    QTimer.singleShot(10000, sys.exit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
