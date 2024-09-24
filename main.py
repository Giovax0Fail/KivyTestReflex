from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


class Reflex(MDApp):
    def build(self):
        self.title = "Reflex"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "200"
        return Builder.load_file("main.kv")
    
    dialog = None

    def on_start(self):
        self.show_dialog()
    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Testa i Tuoi riflessi",
                text="Metti alla prova i tuoi riflessi con la nostra app! \nMisura la tua velocità di reazione e confronta i tuoi tempi con la media umana di circa 250 millisecondi per gli stimoli visivi\nSfida te stesso e i tuoi amici per vedere chi ha i riflessi più rapidi!",
                buttons=[
                    MDRaisedButton(
                        text="CHIUDI",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    info_dialog = None

    def show_info(self):
        if not self.info_dialog:
            self.dialog = MDDialog(
                title="Team Di Sviluppo",
                text=" \n\n Pietro Vergara \n\n Giovanni Ferrante \n\n Mattia Capasso",
                buttons=[
                    MDRaisedButton(
                        text="CHIUDI",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

if __name__ == '__main__':
    Reflex().run()