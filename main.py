import flet as ft
from flet import *
import time
from firebase_config import init_firebase

firebase = init_firebase()

class Authentication(UserControl):
    def __init__(self):
        super().__init__()

        self.auth_box = Container(
            width=0,  # Start with 0 width for animation
            height=400,
            bgcolor="white",
            animate=animation.Animation(500, "easeOutBack"),  # Smooth animation
            border_radius=8,
            padding=20,
        )
        self.sign_in_email = self.auth_options("Enter Your Email ID", False)
        self.sign_in_password = self.auth_options("Enter Your Password", True)
        self.sign_in_btn = self.auth_buttons("Sign In", None)
        self.register_email = self.auth_options("Register Your Email ID", False)
        self.register_password = self.auth_options("Register Your Password", True)
        self.register_btn = self.auth_buttons("Register", None)

    def open_auth_box(self):
        self.auth_box.width = 740  # Expand the box to full width
        self.auth_box.update()

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
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=8),

            ),
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
                Text("Or", color="black", size=25, weight=FontWeight.BOLD, text_align=TextAlign.CENTER ,),
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

    # Trigger the animation after the page loads
    page.update()
    time.sleep(0.5)  # Slight delay for better visual effect
    auth.open_auth_box()

if __name__ == "__main__":
    ft.app(target=main)
