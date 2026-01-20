from tkinter import Tk , Text , Entry , Button, StringVar, END
from tkinter.ttk import Combobox
from threading import Thread
from datetime import datetime
import json
from pathlib import Path
from app.manage_db import lista_profiles, create_profile
from app.functions import carregar_fernet
from app.system import system
from app.logger import log, detectar_profile, set_screen, write_profile
from nodriver import Browser
import asyncio




class Tela (Tk):
    def __init__(self):
        super().__init__()
        self.string_var = StringVar()
        self.fernet = self.criptografar()
        self.dados = self.create_profile
        self.perfil = None
        if not self.perfil:
            self.title("App GetLike")
        self.title(self.perfil)
        self.geometry('700x700+660+0')
        self.attributes('-topmost', True)
        
        self.tela = Text(self, width=100,height=15,bg='black',fg='green',font=('Consolas',12))
        self.tela.pack()
        set_screen(self.tela)
        
        

        self.chat = Entry(width=94, font=('Consolas',12))
        self.chat.pack()
        
         
        self.enter = Button(text="Ok",bg='white', fg='green', width=80, height=1, font=('Consolas',9), command= self.input_chat)
        self.enter.pack()

        self.lista_profiles = lista_profiles()
        self.perfils = Combobox(values=self.lista_profiles, font=('Consolas',12))
        self.perfils.pack()
        
        self.choose_profile = Button(text="Escolher Profile",bg='white', fg='green', width=80, height=2, command= self.get_profile, font=('Consolas',9))
        self.choose_profile.pack(pady=0.5)
        
        self.add = Button(text="Adicionar Tiktok",bg='white', fg='blue', width=80, height=2, command= self.create_profile, font=('Consolas',9))
        self.add.pack(pady=0.5)
        
        
        self.mostrar_esconder_navegador = Button(text='Mostar Navegador/Esconder Navegador', bg='white', fg='blue', width=80, height=2,command=self.iniciar_thread4, font=('Consolas',10))
        self.mostrar_esconder_navegador.pack(pady=10)
        
        self.salvarlogin_gnr = Button(text='Salvar Login GetLikes', bg='white', fg='black', width=80, height=2, command=self.iniciar_thread3, font=('Consolas',10))
        self.salvarlogin_gnr.pack(pady=0.5)
        
        self.salvarlogin_tiktok = Button(text='Salvar Login TikTok', bg='white', fg='green', width=80, height=2, command=self.iniciar_thread2, font=('Consolas',10))
        self.salvarlogin_tiktok.pack(pady=0.5)
        
        self.iniciar_sistema = Button(text='Iniciar', bg='white', fg='blue', width=80, height=2, command=self.iniciar_thread, font=('Consolas',12))
        self.iniciar_sistema.pack(pady=10)

        self.close = Button(text="Stop Automation", bg="red", fg="white", width=80, height=1, font=('Consolas',9), command=self.iniciar_thread5)
        self.close.pack()
        self.detectar_perfil()

        
    def mudar_title(self, title):
        title = self.perfil
        return self.after(0, lambda: self.title(title))
        
      
    def detectar_perfil(self):
        self.perfil = detectar_profile()
        self.title(self.perfil)
        return self.perfil   
       

        
    def criptografar(self):
        fernet = carregar_fernet()
        return fernet
        
        
    def get_profile(self):  
        if self.perfils:
            self.perfil = self.perfils.get()  
        write_profile(self.perfil)
        log(f"Profile Selecionado: {self.perfil}")
        self.mudar_title(self.perfil)
        return self.perfil
       
       
    def input_chat(self):     
        if self.chat.get():
            texto = self.chat.get().strip()
            self.string_var.set(texto)
            return texto
    
    def clear_chat(self):
        self.chat.delete(0, END)    
    
    
    def stringvar(self):
        self.string_var.set(self.input_chat())
        return self.string_var
   
    
    def create_profile(self):
        log("Digite o Username da conta Tiktok: ")
        self.wait_variable(self.string_var)     
        Profile_Name = self.input_chat()
        self.clear_chat()
        
        log("Digite o Email da conta Tiktok: ")
        self.wait_variable(self.string_var)
        Email = self.input_chat()
        self.clear_chat()
        
        Social_Network = "Tiktok"
        
        log("Digite a Senha da conta Tiktok: ")
        self.wait_variable(self.string_var)
        senha = self.input_chat()
        Password = self.fernet.encrypt(senha.encode('utf-8'))
        self.clear_chat()
        
        Created_At = datetime.now()
        Update_At = datetime.now()
        is_Active =  1
        
        log("Digite Anotações Gerais da conta Tiktok: ")
        self.wait_variable(self.string_var)
        Note = self.input_chat()
        self.clear_chat()
        
        dados = (Profile_Name, Email, Social_Network, Password, Created_At, Update_At, is_Active, Note)
        create_profile(dados)
        self.lista_profiles = lista_profiles()
        self.perfils.configure(values=self.lista_profiles)
        return dados
        
    
    def rodar_asyncio(self, callback):
        asyncio.run(callback())
        

    def iniciar_thread(self):
        cor = Thread(target= self.rodar_asyncio, args=(system.run,), daemon=True)
        cor.start()

    def iniciar_thread2(self):
        cor = Thread(target= self.rodar_asyncio, args=(system.login_profile,), daemon=True)
        cor.start()

    def iniciar_thread3(self):
        cor = Thread(target= self.rodar_asyncio, args=(system.login_getlike,), daemon=True)
        cor.start()

    def iniciar_thread4(self):
        thread = Thread(target= self.rodar_asyncio, args=(system.mostrar_navegador,), daemon=True)
        thread.start()
        
    def iniciar_thread5(self):
        thread = Thread(target= self.rodar_asyncio, args=(system.stop,), daemon=True)
        thread.start()
