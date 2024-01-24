import argparse
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from datetime import datetime, timedelta
from tkinter import ttk
from typing import Optional


class Minuterie(tk.Tk):
    """
    Classe qui permet de voir le temps restant
    """
    dim_columns: int = 25
    dim_rows: int = 25
    time_format: str = "%Y-%m-%d_%H:%M:%S"
    date_format: str = time_format.split("_")[0]
    hour_format: str = time_format.split("_")[1]

    # champs horaires
    initial_time: Optional[str] = None
    initial_type: Optional[int] = None
    time: str = None
    time_left: str = None
    curent_type: str = None
    timer_running: bool = False

    # dictionnaire de traduction
    Langage: str = "fr"
    dictionary_translation: dict = {
        "fr": {
            "title": "Minuterie",
            "time": "Temps",
            "time_left": "Temps restant",
            "start": "Démarrer",
            "stop": "Arrêter",
            "reset": "Réinitialiser",
            "quit": "Quitter",
            "explanatory_type_label": "Choisissez le type de durée :",
            "explanatory_type": ["Durée en secondes", f"{time_format}", f"{hour_format}"],
            "explanatory_label": f"Entrez la durée en secondes ou "
                                 f"la date de fin au format {time_format} ou "
                                 f"la durée au format {hour_format} :"
        },
        "en": {
            "title": "Timer",
            "time": "Time",
            "time_left": "Time left",
            "start": "Start",
            "stop": "Stop",
            "reset": "Reset",
            "quit": "Quit",
            "explanatory_type_label": "Choose the type of duration :",
            "explanatory_type": ["Duration in seconds", f"{time_format}", f"{hour_format}"],
            "explanatory_label": f"Enter the duration in seconds or "
                                 f"the end date in {time_format} format or "
                                 f"the duration in {hour_format} format :"
        }
    }

    # champs de saisie
    label_type: tk.Label = None
    type: ttk.Combobox = None

    label: tk.Label = None
    entry: tk.Entry = None

    # boutons
    frameButtons: tk.Frame = None
    start: tk.Button = None
    stop: tk.Button = None

    # champs de texte
    time_label: tk.Label = None
    time_label_placeholder: tk.Label = None
    time_left_label: tk.Label = None
    time_left_label_placeholder: tk.Label = None

    def __init__(
            self,
            langage: str = "fr",
            duration_str: Optional[str] = None,
            date_fin: Optional[str] = None,
            duree_horaire: Optional[str] = None
    ) -> None:
        """
        Constructeur de la classe interface
        :param langage: Langage de l'interface
        :return: None
        """
        super().__init__()
        self.title("Minuterie")
        self.resizable(False, False)

        self.Langage = langage

        if duration_str is not None and date_fin is not None and duree_horaire is not None:
            print("Vous ne pouvez pas utiliser les arguments -d, -df et -dh en même temps !")
            raise ValueError
        elif duration_str is not None:
            self.initial_time = duration_str
            self.initial_type = 0
        elif date_fin is not None:
            self.initial_time = date_fin
            self.initial_type = 1
        elif duree_horaire is not None:
            self.initial_time = duree_horaire
            self.initial_type = 2
        else:
            self.initial_time = None
            self.initial_type = None

        self.create_widgets()

        self.mainloop()

    def create_widgets(self) -> None:
        """
        Création des widgets
        :return: None
        """

        row: int = 0
        column: int = 0
        nb_columns: int = 2
        nb_rows: int = 1

        # champs de saisie
        self.label_type = tk.Label(self, text=self.dictionary_translation[self.Langage]["explanatory_type_label"])
        self.label_type.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        column += nb_columns

        self.type = ttk.Combobox(self, values=self.dictionary_translation[self.Langage]["explanatory_type"])
        self.type.current(0)
        self.type.bind("<<ComboboxSelected>>", self.change_type)
        self.type.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        if self.initial_type is not None:
            self.type.current(
                self.initial_type
                if self.initial_type < len(self.dictionary_translation[self.Langage]["explanatory_type"])
                else 0
            )

        self.change_type()

        row += nb_rows
        column = 0
        nb_columns = 4

        self.label = tk.Label(self, text=self.dictionary_translation[self.Langage]["explanatory_label"])
        self.label.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        row += nb_rows

        self.entry = tk.Entry(self, width=self.dim_by_nb_columns(nb_columns))
        self.entry.grid(row=row, column=column, sticky=tk.W + tk.E, columnspan=nb_columns, rowspan=nb_rows)

        if self.initial_time is not None:
            self.entry.insert(0, self.initial_time)

        row += nb_rows
        column = 1
        nb_columns = 1

        # boutons
        self.start = tk.Button(self.frameButtons, text=self.dictionary_translation[self.Langage]["start"],
                               command=self.start_timer)
        self.start.grid(row=row, column=column, sticky=tk.E, columnspan=nb_columns, rowspan=nb_rows)
        self.bind("<Return>", lambda event: self.start_timer())

        column += nb_columns

        self.stop = tk.Button(self.frameButtons, text=self.dictionary_translation[self.Langage]["stop"],
                              command=self.stop_timer)
        self.stop.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)
        self.stop.config(state=tk.DISABLED)

        row += nb_rows
        column = 0
        nb_columns = 1

        # champs de texte
        self.time_label = tk.Label(self, text=self.dictionary_translation[self.Langage]["time"])
        self.time_label.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        column += nb_columns

        self.time_label_placeholder = tk.Label(self, text=self.time)
        self.time_label_placeholder.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        column += nb_columns

        self.time_left_label = tk.Label(self, text=self.dictionary_translation[self.Langage]["time_left"])
        self.time_left_label.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        column += nb_columns

        self.time_left_label_placeholder = tk.Label(self, text=self.time_left)
        self.time_left_label_placeholder.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns,
                                              rowspan=nb_rows)

        if self.initial_time is not None and self.initial_type is not None:
            self.start_timer()

    def start_timer(self) -> None:
        """
        Démarre la minuterie
        :return: None
        """

        # vérrouille le champ de saisie et le type
        self.entry.config(state=tk.DISABLED)
        self.type.config(state=tk.DISABLED)

        # actualise les boutons
        self.start.config(state=tk.DISABLED)
        self.stop.config(state=tk.NORMAL)

        if self.validate_time(self.entry.get()):
            # actualise le temps
            self.time = self.calcul_time_end(self.entry.get())
            self.time_label_placeholder.config(text=self.time)

            # actualise le temps restant
            self.time_left = self.convert_time(self.entry.get())
            self.time_left_label_placeholder.config(text=self.time_left)

        else:
            self.reset_timer()
            return

        self.timer_running = True
        self.timer()

    # noinspection PyTypeChecker
    def stop_timer(self) -> None:
        """
        Arrête la minuterie
        :return: None
        """
        self.reset_timer()

        self.timer_running = False

    # noinspection PyTypeChecker
    def reset_timer(self) -> None:
        """
        Réinitialise la minuterie
        :return: None
        """

        # déverrouille le champ de saisie et le type
        self.entry.config(state=tk.NORMAL)
        self.type.config(state=tk.NORMAL)

        # réinitialise le champ de saisie
        self.entry.delete(0, tk.END)

        # réinitialise le type
        self.type.current(0)
        self.curent_type = self.dictionary_translation[self.Langage]["explanatory_type"][0]

        # actualise le temps
        self.time = None
        self.time_label_placeholder.config(text="")

        # actualise le temps restant
        self.time_left = None
        self.time_left_label_placeholder.config(text="")

        # actualise les boutons
        self.start.config(state=tk.NORMAL)
        self.stop.config(state=tk.DISABLED)

        # met à jour l'affichage des labels
        self.update()

    def timer(self) -> None:
        """
        Minuterie
        :return: None
        """

        if self.timer_running:

            # actualiser le temps restant
            horaire_actuel = datetime.now()
            horaire_fin = datetime.strptime(self.time, Minuterie.time_format)
            time_left = horaire_fin - horaire_actuel
            formatted_time_left = str(time_left).split(".")[0]
            self.time_left_label_placeholder.config(text=formatted_time_left)

            # actualise l'affichage
            self.update()

            # si le temps est écoulé
            if horaire_actuel >= horaire_fin:
                self.reset_timer()
                tkMessageBox.showinfo("Minuterie", "Temps écoulé !")
                return

            # rappel de la fonction
            self.after(1000, self.timer)
        else:
            tkMessageBox.showinfo("Minuterie", "Minuterie arrêtée !")

    # noinspection PyUnusedLocal
    def change_type(self, *args) -> None:
        """
        Change le type de durée
        :param args: Arguments
        :return: None
        """

        if self.curent_type is None:
            self.curent_type = self.dictionary_translation[self.Langage]["explanatory_type"][0]

        if self.type.get() not in self.dictionary_translation[self.Langage]["explanatory_type"]:
            self.type.current(0)

        if self.curent_type == self.type.get():
            return

        # actualise le type
        self.curent_type = self.type.get()

        # actualise le champ de saisie
        self.entry.delete(0, tk.END)

    def validate_time(self, time: str) -> bool:
        """
        Vérifie la durée
        :param time: Durée
        :return: True si la durée est valide, False sinon
        """

        if self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][0]:
            return self.validate_format_seconde(time)
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][1]:
            return self.validate_format_time(time)
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][2]:
            return self.validate_format_hour(time)
        else:
            return False

    def convert_time(self, time: str) -> Optional[str]:
        """
        Convertit le temps en time
        :param time: Temps
        :return: Temps
        """

        if self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][0]:
            return self.convert_second_to_time(time)
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][1]:
            return time
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][2]:
            return self.convert_hour_to_time(time)
        else:
            return None

    def calcul_time_end(self, time: str) -> Optional[str]:
        """
        Calcul la date de fin de la minuterie
        :param time: Durée
        :return: Date de fin de la minuterie
        """
        if self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][0]:
            return self.calcul_time_end_by_second(time)
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][1]:
            return self.calcul_time_end_by_time(time)
        elif self.curent_type == self.dictionary_translation[self.Langage]["explanatory_type"][2]:
            return self.calcul_time_end_by_hour(time)
        else:
            return None

    @staticmethod
    def validate_format_time(time: str) -> bool:
        """
        Vérifie le format de la date
        :param time: Date
        :return: True si le format est valide, False sinon
        """

        try:
            datetime.strptime(time, Minuterie.time_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_hour(hour: str) -> bool:
        """
        Vérifie le format de l'heure
        :param hour: Heure
        :return: True si le format est valide, False sinon
        """

        try:
            datetime.strptime(hour, Minuterie.hour_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_date(date: str) -> bool:
        """
        Vérifie le format de la date
        :param date: Date
        :return: True si le format est valide, False sinon
        """

        try:
            datetime.strptime(date, Minuterie.date_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_seconde(seconde: str) -> bool:
        """
        Vérifie le format de la seconde
        :param seconde: Seconde
        :return: True si le format est valide, False sinon
        """
        try:
            s = int(seconde)
            if s < 0:
                return False

            if float(s) != float(seconde):
                return False

        except ValueError:
            return False

        return True

    @staticmethod
    def convert_second_to_time(second: str) -> Optional[str]:
        """
        Convertit les secondes en temps
        :param second: Secondes
        :return: Temps
        """
        if not Minuterie.validate_format_seconde(second):
            return None
        second = int(second)
        return str(timedelta(seconds=second))

    @staticmethod
    def convert_hour_to_time(hour: str) -> str:
        """
        Convertit l'heure en temps
        :param hour: horaire format hh:mm:ss
        :return: Temps
        """
        time = datetime.strptime(hour, Minuterie.hour_format)

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def calcul_time_end_by_second(second: str) -> str:
        """
        Calcul la date de fin de la minuterie
        :param second: Secondes
        :return: Date de fin de la minuterie
        """
        time = datetime.now() + timedelta(seconds=int(second))

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def calcul_time_end_by_time(time: str) -> str:
        """
        Calcul la date de fin de la minuterie
        :param time: Temps
        :return: Date de fin de la minuterie
        """
        return time

    @staticmethod
    def calcul_time_end_by_hour(hour: str) -> str:
        """
        Calcul la date de fin de la minuterie
        :param hour: Heure
        :return: Date de fin de la minuterie
        """
        time = datetime.now() + timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1]),
                                          seconds=int(hour.split(":")[2]))

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def dim_by_nb_columns(nb_columns: int) -> int:
        """
        Calcul les dimensions en fonction du nombre de colonnes
        :param nb_columns: Nombre de colonnes
        :return: Dimensions
        """
        return nb_columns * Minuterie.dim_columns

    @staticmethod
    def dim_by_nb_rows(nb_rows: int) -> int:
        """
        Calcul les dimensions en fonction du nombre de lignes
        :param nb_rows: Nombre de lignes
        :return: Dimensions
        """
        return nb_rows * Minuterie.dim_rows


# noinspection PyTypeChecker
def main() -> bool:
    programme_name: str = "Minuterie"
    programme_version: str = "v0.5.0"
    programme_description: str = "Minuterie en Python"

    parser = argparse.ArgumentParser(description=programme_description)
    parser.add_argument("-v", "--version", action="version",
                        version=f"{programme_name} [%(prog)s] : {programme_version}")
    parser.add_argument("-d", "--duree", type=int, default=None,
                        help="Durée de la minuterie en secondes")
    parser.add_argument("-df", "--date_fin", type=str, default=None,
                        help="Date de fin de la minuterie au format yyyy-mm-dd_HH:MM:SS")
    parser.add_argument("-dh", "--duree_horaire", type=str, default=None,
                        help="Durée de la minuterie au format hh:mm:ss")
    args = parser.parse_args()

    if args.duree is not None and args.date_fin is not None and args.duree_horaire is not None:
        print("Vous ne pouvez pas utiliser les arguments -d, -df et -dh en même temps !")
        return False
    elif args.duree is not None:
        Minuterie(duration_str=str(args.duree))
    elif args.date_fin is not None:
        Minuterie(date_fin=args.date_fin)
    elif args.duree_horaire is not None:
        Minuterie(duree_horaire=args.duree_horaire)
    else:
        Minuterie()

    return True


if __name__ == "__main__":
    if main():
        exit(0)
    else:
        exit(1)
