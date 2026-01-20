from datetime import datetime
from tkinter import END, Text
from pathlib import Path
import json


profile = None
tela: Text = None


def write_profile(new_profile):
    global profile
    profile = new_profile
    dados = {"profile": f"{new_profile}"}
    with open("profile.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)
    return profile


def detectar_profile():   
    with open("profile.json", "r") as perfil:
        dados = json.load(perfil)
        profile = dados["profile"]
    return profile  
    
def set_screen(screen):
    global tela
    tela = screen
    return tela


def log(texto):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y %H:%M:%S")
    data = now.strftime("%d-%m-%Y")
    profile = detectar_profile()
    path_log = Path.cwd()/"Logs"/f"{data}"/f"{profile}.log"
    path_log.parent.mkdir(parents=True, exist_ok=True)
    tela.insert(END, f'[{date}] => {texto}\n')
    tela.see(END)
    with open(path_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f'[{date}] => {texto}\n')
    return print(f'[{date}] => {texto}\n')


def chat_dialog():
    from app import app
    app.wait_variable(app.string_var)
    dialog = app.input_chat()
    return dialog
   