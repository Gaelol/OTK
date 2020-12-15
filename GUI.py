import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

kivy.require("1.10.1")


class LoginUI(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        Window.size = (500, 300)
        self.add_widget(Label(text="Evenement Perso"))
        self.add_widget(Label(text="Nom: "))
        self.nom = TextInput(multiline=False, write_tab=False)
        self.nom.focus = True
        self.add_widget(self.nom)
        self.add_widget(Label(text="Debut de l'event: "))
        self.start_time = TextInput(multiline=False, write_tab=False)
        self.start_time.focus = True
        self.add_widget(self.start_time)
        self.add_widget(Label(text="Fin de l'event: "))
        self.end_time = TextInput(multiline=False, write_tab=False)
        self.end_time.focus = True
        self.add_widget(self.end_time)
        self.add_widget(Label(text="Timezone: "))
        self.timezone = TextInput(multiline=False, write_tab=False)
        self.timezone.focus = True
        self.add_widget(self.timezone)

        self.connect = Button(text="Créer")
        # binds a button to the connect button with a parameter pass to send
        # login params to the button click event, why the empty quote is needed,
        # no idea, will investigate later
        self.connect.bind(on_press=self.connect_btn)
        self.add_widget(self.connect)

        Window.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 36:  # 40 - Enter key pressed

            self.connect_btn(instance)

    def connect_btn(self, instance):
        # print username / password to verify it works
        print(f"{self.username.text}" + "," + f"{self.password.text}")

        # Example of using createPopup
        self.createPopUp("Recieved the credentials: ",
                         "Username: " + self.username.text + "," + "Password: " + self.password.text)

    def createPopUp(self, title, msg):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=msg))
        btn1 = Button(text="Ok")

        box.add_widget(btn1)

        popup = Popup(title=title, title_size=(30), title_align='center', content=box, size_hint=(None, None),
                      size=(430, 200), auto_dismiss=True)

        btn1.bind(on_press=popup.dismiss)
        popup.open()


class Login(App):
    def build(self):
        self.title = 'Login-UI-Example'

        return LoginUI()


if __name__ == "__main__":
    Login().run()


