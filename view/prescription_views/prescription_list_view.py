# view/prescription_views/prescriptions_list_view.py
import customtkinter as ctk
from tkinter import ttk

class PrescriptionListView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        # barre recherche + table + pagination comme pour PatientListView
        self.refresh()

    def refresh(self):
        items = self.ctrl.list_prescriptions()
        # … remplir un Treeview …
