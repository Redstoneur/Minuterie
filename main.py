import argparse
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from datetime import datetime


class Minuterie(tkinter.Tk):
    """
    Classe qui permet de voir le temps restant
    """
    date_format: str = "%Y-%m-%d_%H:%M:%S"
    duration: int = 0
    duree: int = 0

    def __init__(self, durations: int) -> None:
        """
        Constructeur de la classe interface
        :param durations: Durée
        :type durations: Durations
        :return: None
        """
        tkinter.Tk.__init__(self)
        self.title("Minuterie")
        self.geometry("300x100")
        self.resizable(False, False)
        self.duration = durations

        self.label = tkinter.Label(self, text=self.duree)
        self.label.pack()
        self.restart_button = tkinter.Button(self, text="Redémarrer", command=self.restart)

        self.restart()

        self.mainloop()

    def define_duree(self):
        """
        Fonction qui permet de définir la durée de la minuterie
        :return: None
        """
        self.duree = self.duration + 1

    def forget_button(self) -> None:
        """
        Fonction qui permet de faire disparaitre le bouton start ou restart
        :return: None
        """
        if self.restart_button.winfo_ismapped():
            self.restart_button.pack_forget()

    def update_clock(self) -> None:
        """
        Fonction qui permet de mettre à jour le temps restant
        :return: None
        """
        # si le bouton start ou restart est affiché, le faire disparaitre
        self.forget_button()
        self.duree -= 1
        self.label.configure(text=self.duree)
        if self.duree > 0:
            self.after(1000, self.update_clock)
        else:
            tkinter.messagebox.showinfo("Minuterie", "La minuterie est terminée !")
            # si le bouton restart n'est pas affiché, l'afficher et faire disparaitre le bouton start
            self.restart_button.pack()

    def restart(self) -> None:
        """
        Fonction qui permet de redémarrer la minuterie
        :return: None
        """
        self.forget_button()
        self.define_duree()
        self.label.configure(text=self.duree)
        self.update_clock()

    @staticmethod
    def create_duree_with_end_date(end_date: datetime) -> int:
        """
        Fonction qui permet de créer une minuterie avec une date de fin
        :param end_date: Date de fin
        :type end_date: datetime
        :return: None
        """
        return int((end_date - datetime.now()).total_seconds())


# noinspection PyTypeChecker
def main() -> bool:
    programe_name: str = "Minuterie"
    programe_version: str = "v0.5.0"
    programe_description: str = "Minuterie en Python"

    parser = argparse.ArgumentParser(description=programe_description)
    parser.add_argument("-v", "--version", action="version",
                        version=f"{programe_name} [%(prog)s] : {programe_version}")
    parser.add_argument("-d", "--duree", type=int, default=None,
                        help="Durée de la minuterie en secondes")
    parser.add_argument("-df", "--date_fin", type=str, default=None,
                        help="Date de fin de la minuterie au format yyyy-mm-dd_HH:MM:SS")
    args = parser.parse_args()

    if args.duree is not None and args.date_fin is not None:
        print("Vous ne pouvez pas utiliser les arguments -d et -df en même temps !")
        return False
    elif args.duree is not None:
        Minuterie(args.duree)
        return True
    elif args.date_fin is not None:
        try:
            end_date = datetime.strptime(args.date_fin, Minuterie.date_format)
        except ValueError:
            print("Le format de la date de fin est incorrect !")
            return False
        durations = Minuterie.create_duree_with_end_date(end_date)
        if durations < 0:
            print("La date de fin est inférieure à la date actuelle !")
            return False
        Minuterie(durations)
        return True
    else:
        print("Vous devez utiliser les arguments -d ou -df !")
        return False


if __name__ == "__main__":
    if main():
        exit(0)
    else:
        exit(1)
