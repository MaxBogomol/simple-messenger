import socket
import errno
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QTextEdit

HEADER_LENGTH = 10

IP = "209.25.141.181"
PORT = 12620

my_username = ""
my_usertag = "0000"
my_password = "1"
is_login = False
type_connect = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
client_socket.send(f"{100:<{HEADER_LENGTH}}".encode('utf-8'))

class MyThread(QThread):
    my_signal = pyqtSignal(str)
    
    def __init__(self,worker):
        super(MyThread, self).__init__()
        self.count = 0
        self.worker=worker
 
    def run(self):
        self.my_signal.emit(str(self.count))
        self.worker.loop()

class SimpleMessenger(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.setGeometry(round(screen_size.width()/4), round(screen_size.height()/4), round(screen_size.width()/2), round(screen_size.height()/2))
        self.setWindowTitle("Simple Messenger")
        self.thread={}
        
        self.button_send = QPushButton("Send")
        self.button_join = QPushButton("Join")
        self.button_login = QPushButton("Login")
        self.button_reg = QPushButton("Registration")
        self.button_login_back = QPushButton("Back")
        self.button_reg_back = QPushButton("Back")
        self.button_login_join = QPushButton("Join")
        self.button_reg_join = QPushButton("Registration")

        self.messages_text = QTextEdit()
        self.messages_text.setReadOnly(True)

        self.username_login_text = QLineEdit()
        self.username_login_text.setPlaceholderText("Username: ")
        self.usertag_login_text = QLineEdit()
        self.usertag_login_text.setPlaceholderText("Usertag: ")
        self.usertag_login_text.setMaxLength(4)
        self.password_login_text = QLineEdit()
        self.password_login_text.setPlaceholderText("Password: ")

        self.username_reg_text = QLineEdit()
        self.username_reg_text.setPlaceholderText("Username: ")
        self.password_reg_text = QLineEdit()
        self.password_reg_text.setPlaceholderText("Password: ")
        self.password_reg_two_text = QLineEdit()
        self.password_reg_two_text.setPlaceholderText("Password: ")
        
        self.send_text = QLineEdit()

        self.menu_v_line1=QVBoxLayout()
        self.menu_v_line1.addWidget(self.button_login)
        self.menu_v_line1.addWidget(self.button_reg)
        self.menu_v_line1.addWidget(self.button_join)

        self.menu_h_line1=QHBoxLayout()
        self.menu_h_line1.addWidget(self.button_login_back)
        self.menu_h_line1.addWidget(self.button_login_join)

        self.menu_v_line2=QVBoxLayout()
        self.menu_v_line2.addWidget(self.username_login_text)
        self.menu_v_line2.addWidget(self.usertag_login_text)
        self.menu_v_line2.addWidget(self.password_login_text)
        self.menu_v_line2.addLayout(self.menu_h_line1)

        self.menu_h_line2=QHBoxLayout()
        self.menu_h_line2.addWidget(self.button_reg_back)
        self.menu_h_line2.addWidget(self.button_reg_join)

        self.menu_v_line3=QVBoxLayout()
        self.menu_v_line3.addWidget(self.username_reg_text)
        self.menu_v_line3.addWidget(self.password_reg_text)
        self.menu_v_line3.addWidget(self.password_reg_two_text)
        self.menu_v_line3.addLayout(self.menu_h_line2)

        self.h_line1=QHBoxLayout()
        self.h_line1.addWidget(self.send_text,95)
        self.h_line1.addWidget(self.button_send,5)

        self.v_line1=QVBoxLayout()
        self.v_line1.addWidget(self.messages_text,95)
        self.v_line1.addLayout(self.h_line1,5)
        
        self.scroll = QScrollArea(alignment=Qt.AlignTop)
        self.scroll.setLayout(self.v_line1)
        self.scroll.setWidgetResizable(True)

        self.scroll_menu1 = QScrollArea(alignment=Qt.AlignTop)
        self.scroll_menu1.setLayout(self.menu_v_line1)
        self.scroll_menu1.setWidgetResizable(True)

        self.scroll_menu2 = QScrollArea(alignment=Qt.AlignTop)
        self.scroll_menu2.setLayout(self.menu_v_line2)
        self.scroll_menu2.setWidgetResizable(True)

        self.scroll_menu3 = QScrollArea(alignment=Qt.AlignTop)
        self.scroll_menu3.setLayout(self.menu_v_line3)
        self.scroll_menu3.setWidgetResizable(True)

        self.v_line=QVBoxLayout()
        self.v_line.addWidget(self.scroll_menu1)
        self.v_line.addWidget(self.scroll_menu2)
        self.v_line.addWidget(self.scroll_menu3)
        self.v_line.addWidget(self.scroll)

        self.scroll_menu2.hide()
        self.scroll_menu3.hide()
        self.scroll.hide()
        
        self.setLayout(self.v_line)
        self.show()

        self.button_join.clicked.connect(self.join)
        self.button_send.clicked.connect(self.send)

        self.button_login.clicked.connect(self.to_login)
        self.button_reg.clicked.connect(self.to_reg)
        self.button_login_back.clicked.connect(self.back_to_menu)
        self.button_reg_back.clicked.connect(self.back_to_menu)

        self.button_login_join.clicked.connect(self.login)
        self.button_reg_join.clicked.connect(self.reg)

        self.my_thread = MyThread(self)
        self.my_thread.start()

    def back_to_menu(self):
        self.scroll_menu2.hide()
        self.scroll_menu3.hide()
        self.scroll_menu1.show()

    def to_login(self):
        self.scroll_menu1.hide()
        self.scroll_menu2.show()

    def to_reg(self):
        self.scroll_menu1.hide()
        self.scroll_menu3.show()

    def to_messenger(self):
        self.scroll_menu1.hide()
        self.scroll_menu2.hide()
        self.scroll_menu3.hide()
        self.scroll.show()

    def login(self):
        global my_username
        global my_usertag
        global my_password
        global type_connect

        username = self.username_login_text.text()
        usertag = self.usertag_login_text.text()
        password = self.password_login_text.text()

        login = False
        numbers = "0123456789"

        if len(username) and len(usertag)==4 and len(password):
            username_split = username.split()
            username = ""
            i = 0
            for text in username_split:
                username = username + text
                if i+1 < len(username_split):
                    username = username + " "
                i = i+1

            tag = 0
            for i in usertag:
                for number in numbers:
                    if i == number:
                        tag = tag + 1
                        
            if len(username) and tag==4:
                login = True
                my_username = username
                my_usertag = usertag
                my_password = password

        if login:
            type_connect = 1
            self.connect_login()

    def reg(self):
        global my_username
        global my_password
        global type_connect

        username = self.username_reg_text.text()
        password = self.password_reg_text.text()
        password_two = self.password_reg_two_text.text()

        login = False

        if len(username) and len(password) and len(password_two):
            username_split = username.split()
            username = ""
            i = 0
            for text in username_split:
                username = username + text
                if i+1 < len(username_split):
                    username = username + " "
                i = i+1
                        
            if len(username) and password == password_two:
                login = True
                my_username = username
                my_password = password

        if login:
            type_connect = 2
            self.connect_reg()
            
        
    def connect_login(self):
        global my_username
        global my_usertag
        global my_password
        
        username = my_username.encode('utf-8')
        usertag = my_usertag.encode('utf-8')
        password = my_password.encode('utf-8')
        
        socket_header = f"{2:<{HEADER_LENGTH}}".encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        usertag_header = f"{len(usertag):<{HEADER_LENGTH}}".encode('utf-8')
        password_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')
            
        client_socket.send(socket_header + username_header + usertag_header + password_header + username + usertag + password)

    def connect_reg(self):
        global my_username
        global my_password
        
        username = my_username.encode('utf-8')
        password = my_password.encode('utf-8')

        socket_header = f"{1:<{HEADER_LENGTH}}".encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        password_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')
            
        client_socket.send(socket_header + username_header + password_header + username + password)

    def join(self):
        global type_connect

        type_connect = 1
        self.connect_login()

    def send(self):
        global my_username
        global my_usertag
        
        if self.send_text.text() != "":
            message = self.send_text.text()
            self.messages_text.append(f'{my_username}#{str(my_usertag)} > ' + message)
            self.send_text.setText("")
            
            message = message.encode('utf-8')
            socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(socket_header + message_header + message)

    def loop(self):
        global my_username
        global my_usertag
        global client_socket
        global is_login
        global type_connect
        
        while True:
            self.my_thread.usleep(1)
            
            try:
                while True:
                    socket_header = client_socket.recv(HEADER_LENGTH)

                    if not len(socket_header):
                        try:
                            print('Reconnection to the server')
                            
                            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client_socket.connect((IP, PORT))
                            client_socket.setblocking(False)

                            client_socket.send(f"{100:<{HEADER_LENGTH}}".encode('utf-8'))
                        except:
                            print('Connection closed by the server')
                            sys.exit()

                    header = int(socket_header.decode('utf-8').strip())
                    if is_login:
                        if header == 0:
                            username_header = client_socket.recv(HEADER_LENGTH)
                            username_length = int(username_header.decode('utf-8').strip())
                            usertag_header = client_socket.recv(HEADER_LENGTH)
                            usertag_length = int(usertag_header.decode('utf-8').strip())

                            username = client_socket.recv(username_length).decode('utf-8')
                            usertag = client_socket.recv(usertag_length).decode('utf-8')

                            message_header = client_socket.recv(HEADER_LENGTH)
                            message_length = int(message_header.decode('utf-8').strip())
                            message = client_socket.recv(message_length).decode('utf-8')

                            self.messages_text.append(f'{username}#{usertag} > ' + message)
                    else:
                        if type_connect == 1 and header == 2:
                            connect_header = client_socket.recv(HEADER_LENGTH)
                            connect_length = int(connect_header.decode('utf-8').strip())

                            connect = client_socket.recv(connect_length).decode('utf-8')

                            if connect == "1":
                                type_connect = 0
                                is_login = True
                                self.to_messenger()
                                self.send_text.setPlaceholderText(f'{my_username}#{my_usertag} > ')
                            else:
                                type_connect = 0
                        if type_connect == 2 and header == 1:
                            connect_header = client_socket.recv(HEADER_LENGTH)
                            connect_length = int(connect_header.decode('utf-8').strip())
                            usertag_header = client_socket.recv(HEADER_LENGTH)
                            usertag_length = int(usertag_header.decode('utf-8').strip())

                            connect = client_socket.recv(connect_length).decode('utf-8')
                            usertag = client_socket.recv(usertag_length).decode('utf-8')

                            if connect == "1":
                                my_usertag = usertag
                                type_connect = 0
                                is_login = True
                                self.to_messenger()
                                self.send_text.setPlaceholderText(f'{my_username}#{my_usertag} > ')
                            else:
                                type_connect = 0
                                
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                    
                continue

            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = SimpleMessenger()
    sys.exit(app.exec_())

#nuitka --standalone --onefile --plugin-enable=pyqt5 client_gui.py
