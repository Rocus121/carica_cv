import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

# Connessione al database SQLite
conn = sqlite3.connect("cv_database.db", check_same_thread=False)
cursor = conn.cursor()

# Creazione della tabella se non esiste
cursor.execute("""
CREATE TABLE IF NOT EXISTS cv_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    cv BLOB
)
""")
conn.commit()

# Titolo dell'app
st.title("Raccolta CV")

# Form per l'inserimento dei dati
with st.form("cv_form"):
    nome = st.text_input("Nome")
    mail = st.text_input("Email")
    file_cv = st.file_uploader("Carica il tuo CV (PDF)", type=["pdf"])
    submit = st.form_submit_button("Invia")

    if submit and nome and mail and file_cv:
        # Legge il file in formato binario
        cv_data = file_cv.read()

        # Inserisce i dati nel database
        cursor.execute("INSERT INTO cv_data (nome, email, cv) VALUES (?, ?, ?)", (nome, mail, cv_data))
        conn.commit()
        
        st.success("Dati salvati con successo!")

# Recupero dei dati dal database
cursor.execute("SELECT id, nome, email FROM cv_data")
records = cursor.fetchall()

if records:
    st.write("### Elenco CV caricati")
    
    # Creazione di un DataFrame per visualizzare i dati
    df = pd.DataFrame(records, columns=["ID", "Nome", "Email"])
    st.dataframe(df)

    # Pulsanti per scaricare i CV
    for row in records:
        cv_id = row[0]
        nome = row[1]
        
        cursor.execute("SELECT cv FROM cv_data WHERE id = ?", (cv_id,))
        file_data = cursor.fetchone()[0]
        
        st.download_button(
            label=f"Scarica CV di {nome}",
            data=BytesIO(file_data),
            file_name=f"{nome}_CV.pdf",
            mime="application/pdf"
        )

# Chiude la connessione al database
conn.close()


# import streamlit as st

# # Percorso del file database SQLite
# DB_FILE = "cv_database.db"

# st.title("Gestione CV")

# # Pulsante per scaricare il database
# with open(DB_FILE, "rb") as f:
#     st.download_button(label="📥 Scarica Database", data=f, file_name="cv_database.db", mime="application/octet-stream")
