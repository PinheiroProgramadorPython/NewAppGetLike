from pathlib import Path
import sqlite3
import json
from app.logger import detectar_profile, write_profile, log




BASE_DIR = Path.cwd()
myBank = Path(BASE_DIR/"myBank/myBank.db")
myBank.parent.mkdir(parents=True, exist_ok=True)

def create_db():
    with sqlite3.connect(myBank) as connect:
        operador = connect.cursor()
        operador.execute("""
            CREATE TABLE IF NOT EXISTS  profiles(
                ID_Profile INTEGER PRIMARY KEY,
                Profile_Name TEXT NOT NULL,
                Email TEXT NOT NULL,
                Social_Network TEXT NOT NULL,
                Password BLOB NOT NULL,
                Created_At TEXT NOT NULL DEFAULT(datetime('now')),
                Update_At TEXT,
                is_Active INTEGER NOT NULL DEFAULT 1,
                Note TEXT
            );      
        """)
        connect.commit()
    return myBank


def create_profile(dados):
    with sqlite3.connect(myBank) as conectar:
        operador = conectar.cursor()
        operador.execute("""
            INSERT INTO profiles(Profile_Name, Email, Social_Network, Password, Created_At, Update_At, is_Active, Note)
            VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conectar.commit()
        log("Dados Inseridos com Sucesso!")


def lista_profiles():
    if not myBank.exists():
        log("Criando Banco de Dados...")
        create_db()
        log("Vc precisa salvar os Dados dos Perfils")
        log("Clique em Adicionar Tiktok")
    with sqlite3.connect(myBank) as conectar:
        operador = conectar.cursor()
        operador.execute('''
            SELECT Profile_Name
            FROM profiles;            
            ''')
        profile_names = operador.fetchall()
    profiles = []
    for profile in profile_names:
        profiles.append(profile[0])
    return profiles


def profile_tiktok():
    profile = detectar_profile()
    with sqlite3.connect(myBank) as conectar:
        operador = conectar.cursor()
        operador.execute("""
                SELECT Profile_Name, Password
                FROM profiles WHERE Profile_Name = ?       
        """, (profile,))
        dados = operador.fetchone()
    return dados


def mudar_profile():
    profile = detectar_profile()
    lista_profils = lista_profiles()
    position = lista_profils.index(profile)
    if position == len(lista_profils) -1:
        profile = lista_profils[0]
    else:
        profile = lista_profils[position + 1]
        
    write_profile(profile)
    log(f"Mudei para o Profile: {profile}")
    return profile
