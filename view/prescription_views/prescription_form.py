import customtkinter as ctk
from tkcalendar import DateEntry
from controller.prescription_controller import PrescriptionController

class PrescriptionFormView(ctk.CTkFrame):
    def __init__(self, parent, controller, patient_id=None):
        super().__init__(parent)
        self.controller = controller
        self.patient_id = patient_id
        self._create_widgets()

    def _create_widgets(self):
        fields = [
            ('patient_id', 'ID Patient', 'entry'),
            ('medication', 'Médicament*', 'entry'),
            ('dosage', 'Dosage*', 'entry'),
            ('frequency', 'Fréquence*', 'entry'),
            ('duration', 'Durée', 'entry'),
            ('start_date', 'Date début', 'date'),
            ('end_date', 'Date fin', 'date'),
            ('notes', 'Notes', 'text')
        ]

        self.entries = {}
        for i, field in enumerate(fields):
            label = ctk.CTkLabel(self, text=field[1])
            label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if field[2] == 'date':
                entry = DateEntry(self, date_pattern='yyyy-mm-dd')
            elif field[2] == 'text':
                entry = ctk.CTkTextbox(self, height=50)
            else:
                entry = ctk.CTkEntry(self)
                if field[0] == 'patient_id' and self.patient_id:
                    entry.insert(0, str(self.patient_id))
                    entry.configure(state='disabled')
                
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entries[field[0]] = entry

        self.submit_btn = ctk.CTkButton(self, text="Enregistrer", command=self._submit)
        self.submit_btn.grid(row=len(fields), columnspan=2, pady=10)

    def _submit(self):
        data = {
            'patient_id': self.entries['patient_id'].get(),
            'medication': self.entries['medication'].get(),
            'dosage': self.entries['dosage'].get(),
            'frequency': self.entries['frequency'].get(),
            'duration': self.entries['duration'].get(),
            'start_date': self.entries['start_date'].get_date() if 'start_date' in self.entries else None,
            'end_date': self.entries['end_date'].get_date() if 'end_date' in self.entries else None,
            'notes': self.entries['notes'].get("1.0", "end-1c") if 'notes' in self.entries else None
        }
        
        try:
            self.controller.create_prescription(data)
            ctk.CTkMessagebox.showinfo("Succès", "Prescription enregistrée")
        except Exception as e:
            ctk.CTkMessagebox.showerror("Erreur", str(e))