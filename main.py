import argparse
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from datetime import datetime, timedelta
from tkinter import ttk
from typing import Optional

import winsound as ws


class Beep:
    """
    This class is used to generate a beep sound.

    Attributes:
        frequency (int): The frequency of the beep. Default is 1000.
        duration (int): The duration of the beep in milliseconds. Default is 1000.
    """

    frequency: int = 1000
    duration: int = 1000

    def __init__(self, frequency: int = 1000, duration: int = 1000) -> None:
        """
        Initializes the Beep class.

        :param frequency: The frequency of the beep. Default is 1000.
        :param duration: The duration of the beep in milliseconds. Default is 1000.
        """
        self.frequency = frequency
        self.duration = duration

    def run(self):
        """
        Generates the beep sound.
        """
        ws.Beep(frequency=self.frequency, duration=self.duration)

    def set_frequency(self, frequency: int) -> None:
        """
        Sets the frequency of the beep.

        :param frequency: The frequency to set.
        """
        self.frequency = frequency

    def set_duration(self, duration: int) -> None:
        """
        Sets the duration of the beep.

        :param duration: The duration to set in milliseconds.
        """
        self.duration = duration

    def get_frequency(self) -> int:
        """
        Returns the frequency of the beep.

        :return: The frequency of the beep.
        """
        return self.frequency

    def get_duration(self) -> int:
        """
        Returns the duration of the beep.

        :return: The duration of the beep in milliseconds.
        """
        return self.duration

    def __str__(self) -> str:
        """
        Returns a string representation of the Beep object.

        :return: A string representation of the Beep object.
        """
        return f"Beep(frequency={self.frequency}, duration={self.duration})"


class Minuterie(tk.Tk):
    """
    This class is used to create a timer.

    Attributes:
        dim_columns (int): The dimension of columns. Default is 25.
        dim_rows (int): The dimension of rows. Default is 25.
        time_format (str): The format of time. Default is "%Y-%m-%d_%H:%M:%S".
        date_format (str): The format of date. Default is time_format.split("_")[0].
        hour_format (str): The format of hour. Default is time_format.split("_")[1].
        super_beep (bool): The flag to indicate if super beep is enabled. Default is False.
        beep (Beep): The Beep object.
        initial_time (Optional[str]): The initial time. Default is None.
        initial_type (Optional[int]): The initial type. Default is None.
        time (str): The time.
        time_left (str): The time left.
        curent_type (str): The current type.
        timer_running (bool): The flag to indicate if timer is running. Default is False.
        Langage (str): The language. Default is "fr".
        dictionary_translation (dict): The dictionary for translation.
        label_type (tk.Label): The label for type.
        type (ttk.Combobox): The type.
        label (tk.Label): The label.
        entry (tk.Entry): The entry.
        start (tk.Button): The start button.
        stop (tk.Button): The stop button.
        time_label (tk.Label): The label for time.
        time_label_placeholder (tk.Label): The placeholder for time label.
        time_left_label (tk.Label): The label for time left.
        time_left_label_placeholder (tk.Label): The placeholder for time left label.
        beep_Checkbutton (tk.Checkbutton): The checkbutton for beep.
        beep_var (tk.BooleanVar): The variable for beep.
    """

    # attributs
    dim_columns: int = 25
    dim_rows: int = 25
    time_format: str = "%Y-%m-%d_%H:%M:%S"
    date_format: str = time_format.split("_")[0]
    hour_format: str = time_format.split("_")[1]
    super_beep: bool = False
    beep: Beep = Beep()

    # attributs time fields
    initial_time: Optional[str] = None
    initial_type: Optional[int] = None
    time: str = None
    time_left: str = None
    curent_type: str = None
    timer_running: bool = False

    # attributs Dictionary
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
            "beep_label": "Bip",
            "explanatory_type_label": "Choisissez le type de durée :",
            "explanatory_type": ["Durée en secondes", f"{time_format}", f"{hour_format}"],
            "explanatory_label": f"Entrez la durée en secondes ou "
                                 f"la date de fin au format {time_format} ou "
                                 f"la durée au format {hour_format} :",
            "Error": {
                "ArgError": "Vous ne pouvez pas utiliser les arguments -d, -df et -dh en même temps !",
            }
        },
        "en": {
            "title": "Timer",
            "time": "Time",
            "time_left": "Time left",
            "start": "Start",
            "stop": "Stop",
            "reset": "Reset",
            "quit": "Quit",
            "beep_label": "Beep",
            "explanatory_type_label": "Choose the type of duration :",
            "explanatory_type": ["Duration in seconds", f"{time_format}", f"{hour_format}"],
            "explanatory_label": f"Enter the duration in seconds or "
                                 f"the end date in {time_format} format or "
                                 f"the duration in {hour_format} format :",
            "Error": {
                "ArgError": "You cannot use the arguments -d, -df and -dh at the same time !",
            }
        }
    }

    # attributs widgets
    label_type: tk.Label = None
    type: ttk.Combobox = None

    label: tk.Label = None
    entry: tk.Entry = None

    # attributs buttons
    start: tk.Button = None
    stop: tk.Button = None

    # attributs text fields
    time_label: tk.Label = None
    time_label_placeholder: tk.Label = None
    time_left_label: tk.Label = None
    time_left_label_placeholder: tk.Label = None

    # attributs beep
    beep_Checkbutton: tk.Checkbutton = None
    beep_var: tk.BooleanVar = None

    def __init__(
            self,
            langage: str = "fr",
            duration_str: Optional[str] = None,
            date_fin: Optional[str] = None,
            duree_horaire: Optional[str] = None,
            super_beep: bool = False
    ) -> None:
        """
        Initializes the Minuterie class.

        :param langage: The language. Default is "fr".
        :param duration_str: The duration. Default is None.
        :param date_fin: The end date. Default is None.
        :param duree_horaire: The duration in hour. Default is None.
        :param super_beep: The flag to indicate if super beep is enabled. Default is False.

        :raises ValueError: If duration_str, date_fin and duree_horaire are not None.
        :raises ValueError: If the arguments -d, -df and -dh are used at the same time.
        """
        super().__init__()
        self.title("Minuterie")
        self.resizable(False, False)

        self.Langage = "fr" if langage not in self.dictionary_translation.keys() else langage

        if duration_str is not None and date_fin is not None and duree_horaire is not None:
            print(self.dictionary_translation[self.Langage]["Error"]["ArgError"])
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

        self.super_beep = super_beep

        self.create_widgets()

        self.mainloop()

    def create_widgets(self) -> None:
        """
        Create the widgets.
        """

        row: int = 0
        column: int = 0
        nb_columns: int = 2
        nb_rows: int = 1

        # input fields
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
        column = 0
        nb_columns = 1

        # buttons
        self.start = tk.Button(self, text=self.dictionary_translation[self.Langage]["start"],
                               command=self.start_timer)
        self.start.grid(row=row, column=column, sticky=tk.E, columnspan=nb_columns, rowspan=nb_rows)
        self.bind("<Return>", lambda event: self.start_timer())

        column += nb_columns

        self.stop = tk.Button(self, text=self.dictionary_translation[self.Langage]["stop"],
                              command=self.stop_timer)
        self.stop.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)
        self.stop.config(state=tk.DISABLED)

        column += nb_columns + 1

        self.beep_var = tk.BooleanVar()
        self.beep_Checkbutton = tk.Checkbutton(self, text=self.dictionary_translation[self.Langage]["beep_label"],
                                               variable=self.beep_var, onvalue=True, offvalue=False)
        self.beep_Checkbutton.grid(row=row, column=column, sticky=tk.W, columnspan=nb_columns, rowspan=nb_rows)

        if self.super_beep:
            self.beep_Checkbutton.select()
        else:
            self.beep_Checkbutton.deselect()

        row += nb_rows
        column = 0
        nb_columns = 1

        # text fields
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
        Start the timer.
        """

        # locks the input field and the type
        self.entry.config(state=tk.DISABLED)
        self.type.config(state=tk.DISABLED)
        self.beep_Checkbutton.config(state=tk.DISABLED)

        # updates the buttons
        self.start.config(state=tk.DISABLED)
        self.stop.config(state=tk.NORMAL)

        if self.validate_time(self.entry.get()):
            # updates the time
            self.time = self.calcul_time_end(self.entry.get())
            self.time_label_placeholder.config(text=self.time)

            # updates the time left
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
        Stop the timer.
        """
        self.reset_timer()

        self.timer_running = False

    # noinspection PyTypeChecker
    def reset_timer(self) -> None:
        """
        Reset the timer.
        """

        # unlock the input field and the type
        self.entry.config(state=tk.NORMAL)
        self.type.config(state=tk.NORMAL)
        self.beep_Checkbutton.config(state=tk.NORMAL)

        # reset the input field
        self.entry.delete(0, tk.END)

        # reset the type
        self.type.current(0)
        self.curent_type = self.dictionary_translation[self.Langage]["explanatory_type"][0]

        # update the time
        self.time = None
        self.time_label_placeholder.config(text="")

        # update the time left
        self.time_left = None
        self.time_left_label_placeholder.config(text="")

        # update the buttons
        self.start.config(state=tk.NORMAL)
        self.stop.config(state=tk.DISABLED)

        # update display of labels
        self.update()

    def timer(self) -> None:
        """
        Timer.
        """

        if self.timer_running:

            # update the time left
            horaire_actuel = datetime.now()
            horaire_fin = datetime.strptime(self.time, Minuterie.time_format)
            time_left = horaire_fin - horaire_actuel
            formatted_time_left = str(time_left).split(".")[0]
            self.time_left_label_placeholder.config(text=formatted_time_left)

            # update the display
            self.update()

            # check if the time is over
            if horaire_actuel >= horaire_fin:
                self.reset_timer()
                if self.beep_var.get():
                    self.beep.run()
                    pass
                tkMessageBox.showinfo("Minuterie", "Temps écoulé !")
                return

            # call the timer function every second
            self.after(1000, self.timer)
        else:
            tkMessageBox.showinfo("Minuterie", "Minuterie arrêtée !")

    # noinspection PyUnusedLocal
    def change_type(self, *args) -> None:
        """
        Change the type.

        :param args: The arguments.
        """

        if self.curent_type is None:
            self.curent_type = self.dictionary_translation[self.Langage]["explanatory_type"][0]

        if self.type.get() not in self.dictionary_translation[self.Langage]["explanatory_type"]:
            self.type.current(0)

        if self.curent_type == self.type.get():
            return

        # update the type
        self.curent_type = self.type.get()

        # update the input field
        self.entry.delete(0, tk.END)

    def validate_time(self, time: str) -> bool:
        """
        Validate the time.

        :param time: Time
        :return: True if the format is valid, False otherwise
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
        Convert the time.

        :param time: Time
        :return: Time
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
        Calculate the end time of the timer.

        :param time: Time
        :return: End time of the timer
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
        Validate the format of the time.

        :param time: Time
        :return: True if the format is valid, False otherwise
        """

        try:
            datetime.strptime(time, Minuterie.time_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_hour(hour: str) -> bool:
        """
        Validate the format of the hour.

        :param hour: Hour
        :return: True if the format is valid, False otherwise
        """

        try:
            datetime.strptime(hour, Minuterie.hour_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_date(date: str) -> bool:
        """
        Validate the format of the date.

        :param date: Date
        :return: True if the format is valid, False otherwise
        """

        try:
            datetime.strptime(date, Minuterie.date_format)
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_format_seconde(seconde: str) -> bool:
        """
        Validate the format of the second.

        :param seconde: Second
        :return: True if the format is valid, False otherwise
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
        Convert the second to time.

        :param second: Second
        :return: Time
        """
        if not Minuterie.validate_format_seconde(second):
            return None
        second = int(second)
        return str(timedelta(seconds=second))

    @staticmethod
    def convert_hour_to_time(hour: str) -> str:
        """
        Convert the hour to time.

        :param hour: Hour
        :return: Time
        """
        time = datetime.strptime(hour, Minuterie.hour_format)

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def calcul_time_end_by_second(second: str) -> str:
        """
        Calculate the end time of the timer.

        :param second: Second
        :return: End time of the timer
        """
        time = datetime.now() + timedelta(seconds=int(second))

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def calcul_time_end_by_time(time: str) -> str:
        """
        Calculate the end time of the timer.

        :param time: Time
        :return: End time of the timer
        """
        return time

    @staticmethod
    def calcul_time_end_by_hour(hour: str) -> str:
        """
        Calculate the end time of the timer.

        :param hour: Hour
        :return: End time of the timer
        """
        time = datetime.now() + timedelta(hours=int(hour.split(":")[0]), minutes=int(hour.split(":")[1]),
                                          seconds=int(hour.split(":")[2]))

        return time.strftime(Minuterie.time_format)

    @staticmethod
    def dim_by_nb_columns(nb_columns: int) -> int:
        """
        Calculate the dimensions based on the number of columns.

        :param nb_columns: Number of columns
        :return: Dimensions
        """
        return nb_columns * Minuterie.dim_columns

    @staticmethod
    def dim_by_nb_rows(nb_rows: int) -> int:
        """
        Calculate the dimensions based on the number of rows.

        :param nb_rows: Number of rows
        :return: Dimensions
        """
        return nb_rows * Minuterie.dim_rows


# noinspection PyTypeChecker
def main() -> bool:
    program_name: str = "Minuterie"
    program_version: str = "v0.6.0"
    program_description: str = "Minuterie en Python"

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument("-v", "--version", action="version",
                        version=f"{program_name} [%(prog)s] : {program_version}")
    parser.add_argument("-d", "--duration", type=int, default=None,
                        help="Duration of the timer in seconds")
    parser.add_argument("-ed", "--end_date", type=str, default=None,
                        help="End date of the timer in the format yyyy-mm-dd_HH:MM:SS")
    parser.add_argument("-dh", "--duration_hour", type=str, default=None,
                        help="Duration of the timer in the format hh:mm:ss")
    parser.add_argument("-sb", "--super_beep", action="store_true", default=False,
                        help="Activate the super beep")
    args = parser.parse_args()

    if args.duration is not None and args.end_date is not None and args.duration_hour is not None:
        print("You cannot use the arguments -d, -ed and -dh at the same time!")
        return False
    elif args.duree is not None:
        Minuterie(duration_str=str(args.duree), super_beep=args.super_beep)
    elif args.date_fin is not None:
        Minuterie(date_fin=args.date_fin, super_beep=args.super_beep)
    elif args.duree_horaire is not None:
        Minuterie(duree_horaire=args.duree_horaire, super_beep=args.super_beep)
    else:
        Minuterie(super_beep=args.super_beep)

    return True


if __name__ == "__main__":
    if main():
        exit(0)
    else:
        exit(1)
