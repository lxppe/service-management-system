import customtkinter as ctk
from Python.ordem_serviço_app.database.db import listar_os

class TelaListaros(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Listar ordens de serviço").pack(pady=(1))

        self.tabela = ctk.CTkFrame(self)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        #ctk.CTkButton(
            #self,
            #text="Voltar",
            #command=mostrar_ordem
        #).pack(pady=10)

    def atualizar(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        headers = ["cliente", "descrição", "data de abertura", "prioridade", "status", "responsável"]
        for col, texto in enumerate(headers):
            ctk.CTkLabel(
                self.tabela,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        listagem = listar_os()  
      
        for row, cliente in enumerate(listagem, start=1):
            for col, valor in enumerate(cliente):
                ctk.CTkLabel(
                    self.tabela,
                    text=valor if valor else "-"
                ).grid(row=row, column=col, padx=10, pady=5, sticky="w")

       
        for i in range(4):
            self.tabela.grid_columnconfigure(i, weight=1)

        

    