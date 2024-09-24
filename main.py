from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
import random
import time


class Reflex(MDApp):
    def build(self):
        self.title = "Reflex"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "200"
        return Builder.load_file("main.kv")
    
    dialog = None
    info_dialog = None
    player_name_dialog = None
    buttons = []
    current_button = None
    attempts = 0
    reaction_times = []  # Lista per memorizzare i tempi di reazione
    start_time = None
    player_name = ""
    leaderboard = []  # Lista per memorizzare la classifica dei giocatori

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

    def show_info(self):
        if not self.info_dialog:
            self.info_dialog = MDDialog(  # Cambia self.dialog in self.info_dialog
                title="Team Di Sviluppo",
                text=" \n\n Pietro Vergara \n\n Giovanni Ferrante \n\n Mattia Capasso",
                buttons=[
                    MDRaisedButton(
                        text="CHIUDI",
                        on_release=self.close_info_dialog
                    ),
                ],
            )
        self.info_dialog.open()


    def close_info_dialog(self, *args):
        self.info_dialog.dismiss()

    def start_game(self):
        if not self.player_name_dialog:
            self.player_name_dialog = MDDialog(
                title="Inserisci il tuo nome",
                type="custom",
                content_cls=MDTextField(
                    hint_text="Nome del giocatore",
                    on_text_validate=self.set_player_name
                ),
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.set_player_name
                    ),
                ],
            )
        self.player_name_dialog.open()

    def set_player_name(self, *args):
        self.player_name = self.player_name_dialog.content_cls.text
        self.player_name_dialog.dismiss()
        self.buttons = [self.root.ids.btn1, self.root.ids.btn2, self.root.ids.btn3,
                        self.root.ids.btn4, self.root.ids.btn5, self.root.ids.btn6,
                        self.root.ids.btn7, self.root.ids.btn8, self.root.ids.btn9]
        self.attempts = 0
        self.reaction_times = []  
        self.next_button()

    def next_button(self):
        if self.current_button:
            self.current_button.md_bg_color = [0, 0.55, 0.8, 1]
        if self.attempts < 30:
            self.current_button = random.choice(self.buttons)
            self.current_button.md_bg_color = [1, 0, 0, 1]
            self.current_button.bind(on_release=self.on_button_press)
            self.start_time = time.time() 
            self.attempts += 1
        else:
            self.end_game()

    def on_button_press(self, instance):
        reaction_time = (time.time() - self.start_time) * 1000  
        self.reaction_times.append(reaction_time)
        instance.md_bg_color = self.theme_cls.primary_color 
        instance.unbind(on_release=self.on_button_press)
        Clock.schedule_once(lambda dt: self.next_button(), 0.5)

    def end_game(self):
        average_reaction_time = sum(self.reaction_times) / len(self.reaction_times)  
        self.leaderboard.append((self.player_name, average_reaction_time))  
        self.dialog = MDDialog(
            title="Gioco Terminato",
            text=f"Hai completato il gioco! Ottimo lavoro!\nVelocità media di reazione: {average_reaction_time:.2f} ms",
            buttons=[
                MDRaisedButton(
                    text="CHIUDI",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def show_leaderboard(self):
        leaderboard_text = "\n".join([f"{name}: {time:.2f} ms" for name, time in sorted(self.leaderboard, key=lambda x: x[1])])
        self.leaderboard_dialog = MDDialog(
            title="Classifica Giocatori",
            text=leaderboard_text,
            buttons=[
                MDRaisedButton(
                    text="CHIUDI",
                    on_release=self.close_leaderboard_dialog  # Usa la nuova funzione per chiudere la finestra di dialogo
                ),
            ],
        )
        self.leaderboard_dialog.open()
        
    def close_leaderboard_dialog(self, *args):
        self.leaderboard_dialog.dismiss()



if __name__ == '__main__':
    Reflex().run()
