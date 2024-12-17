# Converge is a real-time chat application that allows users to communicate with each other in a secure and private way. In simple this is a group chat app Where The auth Users can chat among themselves.
import datetime
import flet as ft
from flet import *
import time
import tkinter as tk
import requests
from firebase_config import init_firebase

# Initialize Firebase
firebase = init_firebase()
auth = firebase.auth()
db = firebase.database()

class Authentication(UserControl):
    def __init__(self):
        super().__init__()
        self.userid = ""
        self.email = ""

        self.auth_box = Container(
            width=0,
            height=400,
            bgcolor="#FFFAF0",
            animate=animation.Animation(500, "easeOutBack"),
            border_radius=8,
            opacity=0,
            padding=20,
        )
        self.sign_in_email = self.create_textfield("Enter Your Email ID", False,)
        self.sign_in_password = self.create_textfield("Enter Your Password", True)
        self.sign_in_btn = self.create_button("Sign In", self.auth_users)
        self.register_email = self.create_textfield("Register Your Email ID", False)
        self.register_password = self.create_textfield("Register Your Password", True)
        self.register_btn = self.create_button("Register", self.register_user)
    

    def open_auth_box(self):
        self.auth_box.width = 740
        self.auth_box.opacity = 1
        self.auth_box.update()

    def close_auth_box(self):
        self.auth_box.opacity = 0
        self.auth_box.update()
        time.sleep(0.8)
        self.auth_box.width = 0
        self.auth_box.update()
        time.sleep(0.8)

        self.page.controls.remove(self)
        time.sleep(0.3)

        self.chat = ChatView(self.userid, self.email)

        self.page.controls.insert(0, self.chat)
        self.page.update()
        time.sleep(0.3)


        self.chat.open_chat_box()



    def auth_users(self, event):
        try:
            user = auth.sign_in_with_email_and_password(
                self.sign_in_email.value, self.sign_in_password.value
            )
            self.userid = user["localId"]
            self.email = user["email"]
            print("Sign-in successful:", self.email)
            self.close_auth_box()
        except Exception as e:
            print("Error during sign-in:", e)

    def register_user(self, event):
        try:
            user = auth.create_user_with_email_and_password(
                self.register_email.value, self.register_password.value
            )
            self.userid = user["localId"]
            self.email = user["email"]
            print("Registration successful:", self.email)
        except Exception as e:
            print("Error during registration:", e)

    def create_textfield(self, label, password):
        return TextField(
            label=label,
            label_style=TextStyle(size=12, color="black", weight=FontWeight.BOLD),
            width=250,
            height=50,
            password=password,
            text_style=TextStyle(color="black")
        )

    def create_button(self, label, btn_func):
        return ElevatedButton(
            content=Text(label, color="white", size=15, weight=FontWeight.BOLD),
            width=250,
            height=50,
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=8)),
            bgcolor="black",
            on_click=btn_func,
        )
    
    
    def build(self):
        sign_in_column = Column(
            [
                Text("Sign In", color="black", size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
                self.sign_in_email,
                self.sign_in_password,
                self.sign_in_btn,
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=30,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        register_column = Column(
            [
                Text("Register", color="black", size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
                self.register_email,
                self.register_password,
                self.register_btn,
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=30,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        self.auth_box.content = Row(
            [
                sign_in_column,
                Text("Or", color="black", size=25, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
                register_column,
            ],
            spacing=20,
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )

        return self.auth_box


class ChatView(UserControl):
    def __init__(self, userid, email):
        super().__init__()  
        self.userid = userid
        self.email = email
        self.count = 0
        self.chat_box = Container(
            width=680,
            height=0,
            bgcolor="white",
            animate=animation.Animation(550, "easeOutBack"),
            border_radius=8,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        self.chat_area = Column(
            expand=True,
            auto_scroll=True,
            scroll="hidden",
        )
        self.chat_input = TextField(
            hint_text="Type your message here...",
            multiline=True,
            width=600,
            height=50,
            text_size=15,
            content_padding=8,
            border_radius=5,
            text_style=TextStyle(color="black"),
        )
        self.send_chat_btn = ElevatedButton(
            content=Icon(
                name=Icons.SEND,
                color="white",
                size=15,
                rotate=transform.Rotate(5.5, alignment.center)
            ),
            width=50,
            height=50,
            bgcolor="black",
            style=ButtonStyle(shape=RoundedRectangleBorder(radius=8)),
            on_click=lambda e: self.push_message_to_db(e),
        )

        self.start_listening()
        self.set_chat_history()

    def push_message_to_db(self, event):
        try:
            data = {
                "email": self.email,
                "message": self.chat_input.value,
                "sender": self.userid,
                "timestamp": int(time.time() * 1000),
            }
            db.child("message").child(data["timestamp"]).set(data)
        except requests.exceptions.HTTPError as e:
            print("Error during message push:",e )
        except Exception as e:
            print("Unexpected error:", e)
        finally:
            self.chat_input.value = ""
            self.chat_input.update()

    



    def chat_message_ui(self,sent_time, name, text_message, bg, col_pos, row_pos):
        return Container(
         padding=padding.only(left=25, right=25, top=12, bottom=12),   
         bgcolor=bg,
         border_radius=8,
         margin=5,
         content=Column(
         horizontal_alignment=col_pos,
         spacing=10,
         controls=[
             Row(
                 alignment=row_pos,
                 controls=[
                     Text(
                         name + " 0 " + sent_time,
                         color="black",
                         size=15,
                         weight=FontWeight.BOLD,
                     )
                 ],
             ),
             Row(
                 alignment=row_pos,
                 controls=[
                     Text(
                         text_message,
                         color="black",
                         size=15,
             )
             ],
             ),
         ],

         )
        )
    
    def set_chat_history(self):
        try:
            messages = db.child("message").get()
            if messages.each():
                items = []
                for message in messages.each():
                    value = message.val()
                    time = datetime.datetime.fromtimestamp(int(value["timestamp"]) / 1000.0).strftime('%H:%M')
                    items.append(
                        self.chat_message_ui(
                            time,
                            value["email"],
                            value["message"],
                            "#90EE90" if value["sender"] == self.userid else "#ADD8E6",
                            CrossAxisAlignment.END if value["sender"] == self.userid else CrossAxisAlignment.START,
                            MainAxisAlignment.END if value["sender"] == self.userid else MainAxisAlignment.START,
                        )
                    )
                for item in items:
                    self.chat_area.controls.append(item)
                if hasattr(self, 'page'):
                    self.page.update()
                self.chat_area.update()
            else:
                print("No messages found in the database.")
        except Exception as e:
            print("Error retrieving messages:", e)




    def start_listening(self):
        try:
            if auth.current_user is None:
                print("No user is authenticated.")
            else:
                print("Authenticated user:", auth.current_user['email'])
            self.stream = db.child("message").stream(self.stream_handler, auth.current_user['idToken'])
        except Exception as e:
            print("Error during message push:", e)


    def stream_handler(self, value):
        if 'data' in value and self.count > 0:
            data = value['data']
            if 'timestamp' in data and 'sender' in data and 'email' in data and 'message' in data:
                time = datetime.datetime.fromtimestamp(int(data["timestamp"]) / 1000.0).strftime('%H:%M')
                if data["sender"] == self.userid:
                    self.chat_area.controls.append(
                        self.chat_message_ui(
                            time,
                            data["email"],
                            data["message"],
                            "#90EE90",
                            CrossAxisAlignment.END,
                            MainAxisAlignment.END,
                        )
                    )
                else:
                    self.chat_area.controls.append(
                        self.chat_message_ui(
                            time,
                            data["email"],
                            data["message"],
                            "#ADD8E6",
                            CrossAxisAlignment.START,
                            MainAxisAlignment.START,
                        )
                    )
                self.chat_area.update()
        self.count += 1

        

    def open_chat_box(self):
        self.chat_box.height = 650
        self.chat_box.update()

    def chat_box_header(self):
        return Card(
            width=680,
            height=50,
            elevation=10,
            margin=-12,
            content = Container(
                alignment=alignment.center,
                padding=padding.only(top=20),
                content=Text("Converge - Chat Room", color="white", size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
                bgcolor="black",
            )
        )
    
    def build(self):
        chat_column = Column(
            controls=[
                self.chat_box_header(),
                Divider(height=2, thickness=2, color="transparent"),
                Container(
                    width=680,
                    height=500,
                    bgcolor="white",
                    border = border.only(bottom=border.BorderSide(1, "black")),
                    content = self.chat_area,
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.chat_input ,
                            self.send_chat_btn,     
                        ]
                    ),
            ],    
        )
        self.chat_box.content = chat_column
        return self.chat_box


def main(page: ft.Page):
    page.title = "Converge"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "black"

    auth_view = Authentication()
    page.add(auth_view)
    page.update()
    time.sleep(1)
    auth_view.open_auth_box()


if __name__ == "__main__":
    ft.app(target=main)