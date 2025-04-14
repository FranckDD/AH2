-- Table: patients
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom varchar(65) NOT NULL,
    prenom varchar(65),
    adresse varchar(65),
    telephone varchar(65),
    mois_naiss DATE,
    email varchar(65),
    assurance varchar(65),
    date_enregistrement DATETIME
);