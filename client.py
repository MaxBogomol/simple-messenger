import socket
import errno
import sys
import traceback

from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QTextEdit, QLabel
from PyQt5.QtGui import QIcon

#import ctypes
#myappid = 'mycompany.myproduct.subproduct.version'
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
client_socket.setblocking(True)
client_socket.send(f"{100:<{HEADER_LENGTH}}".encode('utf-8'))

class MyThread(QThread):
    add_message = pyqtSignal(object, bool)
    add_user = pyqtSignal(object)
    
    def __init__(self,worker):
        super(MyThread, self).__init__()
        self.worker=worker
 
    def run(self):
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.thread={}

        self.label_messenger = QLabel("Simple Messanger")
        self.label_login = QLabel("Login")
        self.label_reg = QLabel("Registration")
        
        self.button_send = QPushButton("Send")
        self.button_join = QPushButton("Join")
        self.button_login = QPushButton("Login")
        self.button_reg = QPushButton("Registration")
        self.button_login_back = QPushButton("Back")
        self.button_reg_back = QPushButton("Back")
        self.button_login_join = QPushButton("Join")
        self.button_reg_join = QPushButton("Registration")
        self.button_load_messages = QPushButton("Load more messages")

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
        self.menu_v_line1.addWidget(self.label_messenger, alignment=Qt.AlignCenter)
        self.menu_v_line1.addWidget(self.button_login)
        self.menu_v_line1.addWidget(self.button_reg)
        self.menu_v_line1.addWidget(self.button_join)
        self.menu_v_line1.setAlignment(Qt.AlignTop)

        self.menu_h_line1=QHBoxLayout()
        self.menu_h_line1.addWidget(self.button_login_back)
        self.menu_h_line1.addWidget(self.button_login_join)

        self.menu_v_line2=QVBoxLayout()
        self.menu_v_line2.addWidget(self.label_login, alignment=Qt.AlignCenter)
        self.menu_v_line2.addWidget(self.username_login_text)
        self.menu_v_line2.addWidget(self.usertag_login_text)
        self.menu_v_line2.addWidget(self.password_login_text)
        self.menu_v_line2.addLayout(self.menu_h_line1)
        self.menu_v_line2.setAlignment(Qt.AlignTop)

        self.menu_h_line2=QHBoxLayout()
        self.menu_h_line2.addWidget(self.button_reg_back)
        self.menu_h_line2.addWidget(self.button_reg_join)

        self.menu_v_line3=QVBoxLayout()
        self.menu_v_line3.addWidget(self.label_reg, alignment=Qt.AlignCenter)
        self.menu_v_line3.addWidget(self.username_reg_text)
        self.menu_v_line3.addWidget(self.password_reg_text)
        self.menu_v_line3.addWidget(self.password_reg_two_text)
        self.menu_v_line3.addLayout(self.menu_h_line2)
        self.menu_v_line3.setAlignment(Qt.AlignTop)

        self.messages_v_line=QVBoxLayout()
        self.messages_v_line.setAlignment(Qt.AlignBottom)
        self.messages_v_line.addWidget(self.button_load_messages, alignment=Qt.AlignCenter)
        self.messages_widget = QWidget()
        self.messages_widget.setLayout(self.messages_v_line)
        
        self.scroll_messages = QScrollArea(alignment=Qt.AlignTop)
        self.scroll_messages.setWidget(self.messages_widget)
        self.scroll_messages.setWidgetResizable(True)
        self.scroll_messages.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.users_v_line=QVBoxLayout()
        self.users_v_line.setAlignment(Qt.AlignTop)
        self.users_widget = QWidget()
        self.users_widget.setLayout(self.users_v_line)
        
        self.scroll_users = QScrollArea(alignment=Qt.AlignTop)
        self.scroll_users.setWidget(self.users_widget)
        self.scroll_users.setWidgetResizable(True)
        self.scroll_users.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.h_line2=QHBoxLayout()
        self.h_line2.addWidget(self.scroll_messages,80)
        self.h_line2.addWidget(self.scroll_users,20)

        self.h_line1=QHBoxLayout()
        self.h_line1.addWidget(self.send_text,80)
        self.h_line1.addWidget(self.button_send,20)

        self.v_line1=QVBoxLayout()
        self.v_line1.addLayout(self.h_line2,95)
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
        self.button_load_messages.clicked.connect(self.load_messages)

        self.button_login.clicked.connect(self.to_login)
        self.button_reg.clicked.connect(self.to_reg)
        self.button_login_back.clicked.connect(self.back_to_menu)
        self.button_reg_back.clicked.connect(self.back_to_menu)

        self.send_text.returnPressed.connect(self.send)

        self.button_login_join.clicked.connect(self.login)
        self.button_reg_join.clicked.connect(self.reg)

        self.scroll_messages.verticalScrollBar().rangeChanged.connect(self.scrollToBottomIfNeeded)
        self.scroll_bar_down = False
        self.scroll_bar_center = False

        self.messages = []
        self.users = []

        self.my_thread = MyThread(self)
        self.my_thread.add_message.connect(self.add_message)
        self.my_thread.add_user.connect(self.add_user)
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
            #self.messages_text.append(f'{my_username}#{str(my_usertag)} > ' + message)
            self.send_text.setText("")
            
            message = message.encode('utf-8')
            socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(socket_header + message_header + message)

    def load_messages(self):
        message = str(self.messages[0].messageid)
        
        message = message.encode('utf-8')
        socket_header = f"{4:<{HEADER_LENGTH}}".encode('utf-8')
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

                            client_socket.send(f"{101:<{HEADER_LENGTH}}".encode('utf-8'))
                            type_connect = 3
                            is_login = False
                        except:
                            print('Connection closed by the server')
                            sys.exit()

                    header = int(socket_header.decode('utf-8').strip())
                    if is_login:
                        if header == 0:
                            userid_header = client_socket.recv(HEADER_LENGTH)
                            userid_length = int(userid_header.decode('utf-8').strip())
                            userid = client_socket.recv(userid_length).decode('utf-8')

                            messageid_header = client_socket.recv(HEADER_LENGTH)
                            messageid_length = int(messageid_header.decode('utf-8').strip())
                            messageid = client_socket.recv(messageid_length).decode('utf-8')

                            message_header = client_socket.recv(HEADER_LENGTH)
                            message_length = int(message_header.decode('utf-8').strip())
                            message = client_socket.recv(message_length).decode('utf-8')

                            new_message = Message(userid, messageid, message, self)
                            self.messages.append(new_message)
                            
                            self.my_thread.add_message.emit(new_message, False)
                        
                        if header == 3:
                            userid_header = client_socket.recv(HEADER_LENGTH)
                            userid_length = int(userid_header.decode('utf-8').strip())
                            username_header = client_socket.recv(HEADER_LENGTH)
                            username_length = int(username_header.decode('utf-8').strip())
                            usertag_header = client_socket.recv(HEADER_LENGTH)
                            usertag_length = int(usertag_header.decode('utf-8').strip())
                            
                            userid = client_socket.recv(userid_length).decode('utf-8')
                            username = client_socket.recv(username_length).decode('utf-8')
                            usertag = client_socket.recv(usertag_length).decode('utf-8')

                            new_user = User(userid, username, usertag, 1, self)
                            self.users.append(new_user)
                            
                            self.my_thread.add_user.emit(new_user)

                        if header == 5:
                            userid_header = client_socket.recv(HEADER_LENGTH)
                            userid_length = int(userid_header.decode('utf-8').strip())
                            userid = client_socket.recv(userid_length).decode('utf-8')

                            messageid_header = client_socket.recv(HEADER_LENGTH)
                            messageid_length = int(messageid_header.decode('utf-8').strip())
                            messageid = client_socket.recv(messageid_length).decode('utf-8')

                            message_header = client_socket.recv(HEADER_LENGTH)
                            message_length = int(message_header.decode('utf-8').strip())
                            message = client_socket.recv(message_length).decode('utf-8')

                            new_message = Message(userid, messageid, message, self)
                            self.messages.insert(0, new_message)
                            
                            self.my_thread.add_message.emit(new_message, True)
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
                        if type_connect == 3 and header == 101:
                            type_connect = 1
                            self.connect_login()
                                
            except IOError as e:
                traceback.print_exc()
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                    
                continue

            except Exception as e:
                traceback.print_exc()
                print('Reading error: '.format(str(e)))
                sys.exit()

    def scrollToBottomIfNeeded(self):
        scrollbar = self.scroll_messages.verticalScrollBar()
        
        if self.scroll_bar_down:
            scrollbar.setValue(scrollbar.maximum())
            self.scroll_bar_down = False
        
        if self.scroll_bar_center:
            scrollbar.setValue(int(scrollbar.maximum()/2))
            self.scroll_bar_center = False

    @pyqtSlot(object, bool)
    def add_message(self, message, up):
        message.create(up)

    @pyqtSlot(object)
    def add_user(self, user):
        user.create()
        

class Message():
    def __init__(self, userid, messageid, data, gui):
        self.userid = userid
        self.messageid = messageid
        self.data = data
        self.gui = gui

    def create(self, up):
        self.label_data = QLabel()
        self.label_data.setText((" " * 4) + self.data)
        self.label_data.setAlignment(Qt.AlignLeft)

        self.label_user = QLabel()
        self.label_user.setAlignment(Qt.AlignLeft)
        self.label_user.hide()
        
        self.h_line1=QHBoxLayout()
        self.h_line1.addWidget(self.label_data)
        
        self.v_line1=QVBoxLayout()
        self.v_line1.addWidget(self.label_user)
        self.v_line1.addLayout(self.h_line1)

        scrollbar = self.gui.scroll_messages.verticalScrollBar()
        scroll = False
        if scrollbar.maximum() == scrollbar.value():
            scroll = True
        if up:
            self.gui.messages_v_line.insertLayout(1, self.v_line1)
        else:
            self.gui.messages_v_line.addLayout(self.v_line1)
        if scroll:
            self.gui.scroll_bar_down = True

        self.update()

    def update(self):
        index = self.gui.messages.index(self)
        show = False
        
        if index == 0:
            show = True
        else:
            if not self.gui.messages[index - 1].userid == self.userid:
                show = True

        if show:
            self.label_user.show()
            is_user = False
            for user in self.gui.users:
                if user.userid == self.userid:
                    is_user = True
                    break

            if is_user:
                self.label_user.setText(user.username + "#" + user.usertag + " >")
        else:
            self.label_user.hide()

class User():
    def __init__(self, ID, username, usertag, status, gui):
        global client_socket
        
        self.userid = ID
        self.username = username
        self.usertag = usertag
        self.status = status
        self.gui = gui

    def create(self):
        self.label_data = QLabel()
        self.label_data.setText(self.username + "#" + self.usertag)
        self.label_data.setAlignment(Qt.AlignLeft)
        #self.label_data.setWordWrap(True)
        #if self.status == 1:
        #    self.label_data.opacity_effect.setEnabled(True)
        #else:
        #    self.label_data.opacity_effect.setEnabled(False)
        
        self.h_line1=QHBoxLayout()
        self.h_line1.addWidget(self.label_data)
        
        self.v_line1=QVBoxLayout()
        self.v_line1.addLayout(self.h_line1)

        self.gui.users_v_line.addLayout(self.v_line1)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = SimpleMessenger()
    sys.exit(app.exec_())

#nuitka --standalone --onefile --plugin-enable=pyqt5 --windows-icon-from-ico=icon.ico --include-data-file=icon.ico=icon.ico client_gui.py
