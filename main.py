import flet as ft
from flet import *
import time
from firebase_config import init_firebase

firebase = init_firebase()
auth = firebase.auth()  

class Authentication(UserControl):
    def __init__(self):
        super().__init__()

        self.userid = ""
        self.email = ""

        self.auth_box = Container(
            width=0,
            height=400,
            bgcolor="white",
            animate=animation.Animation(500, "easeOutBack"),
            border_radius=8,
            opacity=0,
            padding=20,
        )
        self.sign_in_email = self.auth_options("Enter Your Email ID", False)
        self.sign_in_password = self.auth_options("Enter Your Password", True)
        self.sign_in_btn = self.auth_buttons("Sign In", self.auth_users)
        self.register_email = self.auth_options("Register Your Email ID", False)
        self.register_password = self.auth_options("Register Your Password", True)
        self.register_btn = self.auth_buttons("Register", self.register_user)

    def open_auth_box(self):
        self.auth_box.width = 740
        self.auth_box.opacity = 1
        self.auth_box.update()

    def close_auth_box(self):
        self.auth_box.width = 0
        self.auth_box.opacity = 0
        self.auth_box.update()
        time.sleep(0.8)
        self.update()
        self.page.controls.remove(self.auth_box)
        time.sleep(0.3)

    def auth_users(self, event):
        try:
            user = auth.sign_in_with_email_and_password(self.sign_in_email.value, self.sign_in_password.value)
            self.userid = user["localId"]
            self.email = user["email"]
            print("Sign-in successful:", self.email)
            self.close_auth_box()
        except Exception as e:
            print("Error during sign-in:", e)

    def register_user(self, event):
        try:
            user = auth.create_user_with_email_and_password(self.register_email.value, self.register_password.value)
            self.userid = user["localId"]
            self.email = user["email"]
            print("Registration successful:", self.email)
            self.showmessage("Registration successful for user: " + self.email)
        except Exception as e:
            print("Error during registration:", e)

    def auth_options(self, label, password):
        return TextField(
            label=label,
            label_style=TextStyle(size=12, color="black", weight=FontWeight.BOLD),
            width=250,
            height=50,
            password=password,
        )

    def auth_buttons(self, label, btn_func):
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

def main(page: ft.Page):
    page.title = "Converge"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "black"

    auth = Authentication()
    page.add(auth)
    page.update()
    time.sleep(0.99)
    auth.open_auth_box()

if __name__ == "__main__":
    ft.app(target=main)
