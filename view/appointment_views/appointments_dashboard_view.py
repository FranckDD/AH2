import customtkinter as ctk

class AppointmentsDashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Dashboard des Rendez-vous", font=(None, 24)).pack(pady=20)
