import customtkinter as ctk
from database.db import listar_clientes


class TelaListar(ctk.CTkFrame):
    def __init__(self, master, mostrar_dashboard):
        super().__init__(master)
        self.mostrar_dashboard = mostrar_dashboard

        # ================== TÍTULO ==================
        ctk.CTkLabel(
            self,
            text="Histórico de Clientes",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        # ================== TABELA ==================
        self.tabela = ctk.CTkFrame(self)
        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        # ================== BOTÕES ==================
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.frame_botoes,
            text="Voltar",
            height=40,
            command=self.mostrar_dashboard
        ).pack(side="right")

    # ==================================================
    # ATUALIZAR LISTA
    # ==================================================
    def atualizar(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        headers = ["ID", "Nome", "Telefone", "Email", "Observações"]
        for col, texto in enumerate(headers):
            ctk.CTkLabel(
                self.tabela,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=10, pady=8, sticky="w")

        clientes = listar_clientes()

        for row, cliente in enumerate(clientes, start=1):
            for col, valor in enumerate(cliente):
                ctk.CTkLabel(
                    self.tabela,
                    text=valor if valor else "-"
                ).grid(row=row, column=col, padx=10, pady=6, sticky="w")

        for i in range(len(headers)):
            self.tabela.grid_columnconfigure(i, weight=1)

       

    