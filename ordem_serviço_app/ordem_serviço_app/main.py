import customtkinter as ctk
import tkinter as tk

from ui.dashboard import TelaDashboard
from ui.detos import TelaDetos
from ui.config import TelaConfig
from ui.cadastro import TelaCadastro
from ui.listar import TelaListar

from database.db import criar_tabela

class app (ctk.CTk):
    def __init__(self):
        super().__init__()

        criar_tabela()

        self.minsize(800, 700)
        self.geometry('800x700')
        ctk.set_widget_scaling(1.0)

        self.tela_dashboard = TelaDashboard(self, self.mostrar_cadastro, self.mostrar_detos, self.mostrar_listar, self.mostrar_config)
        self.tela_cadastro = TelaCadastro(self, self.mostrar_dashboard)
        self.tela_detos = TelaDetos(self, self.mostrar_dashboard)
        self.tela_config = TelaConfig(self, self.mostrar_dashboard)
        self.tela_listar = TelaListar(self, self.mostrar_dashboard)

        self.mostrar_dashboard()

    def mostrar_detos(self):
        self.tela_dashboard.pack_forget()
        self.tela_detos.atualizar()
        self.title('detalhes da ordem de serviço')
        self.tela_detos.pack(fill='both', expand=True)
    
    def mostrar_dashboard(self):
        self.tela_detos.pack_forget()
        self.tela_config.pack_forget()
        self.tela_cadastro.pack_forget()
        self.tela_listar.pack_forget()
        self.tela_dashboard.status_atualizar()
        self.title('dashboard')
        self.tela_dashboard.pack(fill='both', expand=True)

    def mostrar_cadastro(self):
        self.tela_dashboard.pack_forget()
        self.title('cadastro de clientes')
        self.tela_cadastro.pack(fill='both', expand=True)

    def mostrar_config(self):
        self.title('Configuraçoes')
        self.tela_dashboard.pack_forget()
        self.tela_config.pack(fill='both', expand=True)
        
    def mostrar_listar(self):
        self.title('histórico de clientes')
        self.tela_dashboard.pack_forget()
        self.tela_listar.atualizar()
        self.tela_listar.pack(fill='both', expand=True)

    def mudar_tema(self,escolha):
        if escolha.get() == 'op1':
            ctk.set_appearance_mode("Light")
        elif escolha.get() == 'op2':
            ctk.set_appearance_mode("Dark")
    

app = app()
app.mainloop()