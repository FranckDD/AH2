import customtkinter as ctk

class AppointmentsBookView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Prendre un Rendez-vous", font=(None, 24)).pack(pady=20)
