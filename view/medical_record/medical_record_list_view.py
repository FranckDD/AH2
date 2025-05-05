# view/medical_views/medical_records_list_view.py
import customtkinter as ctk
from tkinter import ttk

class MedicalRecordListView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        # barre + Treeview + pagination
        self.refresh()

    def refresh(self):
        recs = self.ctrl.list_records()
        # remplir le tableau…
