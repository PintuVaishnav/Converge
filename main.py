import flet as ft
from flet import *
import time
from firebase_config import init_firebase

firebase = init_firebase()

class Authentication(UserControl):
    def __init__(self):
        self.auth_box = Container(
            width=740,
            height=250,
            bgcolor="white",
            animate=animation.Animation(550, "easeOutBack"),
            border_radius=8,
            padding=10
        )
        self.auth_box.rows = Row(
            alignment=MainAxisAlignment.CENTER,
            spacing=30,
            # opacity=0,
            animate_opacity=800,
        )

        self.sign_in_email = self.auth_options("Email You Email Id", False)
        self.sign_in_password = self.auth_options("Password", True)

        self.register_email = self.auth_options("Email You Email Id", False)
        self.register_password = self.auth_options("Password", True)

        self.register_confirm_password = self.auth_options("Confirm Password", True)
        



        super().__init__()

    def open_auth_box(self):
        time.sleep(1)
        self.auth_box.width = 790
        self.auth_box.update()

    def auth_options(self , label, password):
        return TextField(
                label = label,
                label_style = TextStyle(size=8, color="black", weight=FontWeight.BOLD),
                width=250,
                height=50,
                password = password
            
        )


    def build(self):

        labels = [
            "Sign In",
            "Register"
        ]
        texts = [
            self.sign_in_email,
            self.sign_in_password,
            self.register_email,
            self.register_password,
            self.register_confirm_password

        ]

        for label, text in zip(labels, texts):
            column = Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                spacing=30
            )
            items = []
            items.append(Text(label, color="black", size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER))
            items.append(text)

            column.controls = items
            self.auth_box.rows.controls.append(column)

        self.auth_box.rows.controls.insert(
            1, Text("Or", color="black", size=30, weight=FontWeight.BOLD)
        )

        self.auth_box.content = self.auth_box.rows
        self.update()

    def build(self):
        return self.auth_box

def main(page: ft.Page):
    page.title = "Converge"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    auth = Authentication()
    page.add(auth)

    auth.open_auth_box()
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
