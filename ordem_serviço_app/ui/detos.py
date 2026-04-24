import customtkinter as ctk
from database.db import listar_os, buscar_detalhes_os


class TelaDetos(ctk.CTkFrame):
    def __init__(self, master, mostrar_dashboard):
        super().__init__(master)
        self.mostrar_dashboard = mostrar_dashboard

        # ================== CONTAINERS ==================
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_detalhes = ctk.CTkFrame(self)

        self.frame_lista.pack(fill="both", expand=True)
        self.frame_detalhes.pack_forget()

        self._criar_tela_lista()
        self._criar_tela_detalhes()

    # ==================================================
    # TELA LISTA
    # ==================================================
    def _criar_tela_lista(self):
        ctk.CTkLabel(
            self.frame_lista,
            text="Ordens de Serviço",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        self.tabela = ctk.CTkFrame(self.frame_lista)
        self.tabela.pack(fill="both", expand=True, padx=20, pady=10)

        self.frame_botoes_lista = ctk.CTkFrame(self.frame_lista)
        self.frame_botoes_lista.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.frame_botoes_lista,
            text="Voltar",
            height=40,
            command=self.mostrar_dashboard
        ).pack(side="right")

    def atualizar(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        headers = ["OS", "Cliente", "Status", ""]
        for col, texto in enumerate(headers):
            ctk.CTkLabel(
                self.tabela,
                text=texto,
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=10, pady=8, sticky="w")

        listagem = listar_os()

        for row, os in enumerate(listagem, start=1):
            self.os_id, nome, status = os

            ctk.CTkLabel(self.tabela, text=self.os_id).grid(row=row, column=0, padx=10, sticky="w")
            ctk.CTkLabel(self.tabela, text=nome).grid(row=row, column=1, padx=10, sticky="w")
            ctk.CTkLabel(self.tabela, text=status).grid(row=row, column=2, padx=10, sticky="w")

            ctk.CTkButton(
                self.tabela,
                text="Ver detalhes",
                width=110,
                command=lambda id=self.os_id: self.mostrar_detalhes(id)
            ).grid(row=row, column=3, padx=10, sticky="e")

        for i in range(4):
            self.tabela.grid_columnconfigure(i, weight=1)

    # ==================================================
    # TELA DETALHES
    # ==================================================
    def _criar_tela_detalhes(self):
        ctk.CTkLabel(
            self.frame_detalhes,
            text="Detalhes da Ordem de Serviço",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        self.container_detalhes = ctk.CTkFrame(self.frame_detalhes)
        self.container_detalhes.pack(fill="both", expand=True, padx=20, pady=10)

        self.frame_cliente = ctk.CTkFrame(self.container_detalhes)
        self.frame_cliente.pack(fill="x", pady=10)

        self.frame_ordem = ctk.CTkFrame(self.container_detalhes)
        self.frame_ordem.pack(fill="x", pady=10)

        self.frame_botoes_detalhes = ctk.CTkFrame(self.frame_detalhes)
        self.frame_botoes_detalhes.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.frame_botoes_detalhes,
            text="Voltar para lista",
            height=40,
            command=self.mostrar_lista
        ).pack(side="right")

       
    def mostrar_detalhes(self, os_id):
        self.frame_lista.pack_forget()
        self.frame_detalhes.pack(fill="both", expand=True)

        for frame in (self.frame_cliente, self.frame_ordem):
            for widget in frame.winfo_children():
                widget.destroy()

        dados = buscar_detalhes_os(os_id)
        if not dados:
            ctk.CTkLabel(self.frame_ordem, text="OS não encontrada").pack()
            return

        (
            nome, telefone, email, obs,
            descricao, data, prioridade, status, responsavel
        ) = dados

        # ---------- CLIENTE ----------
        ctk.CTkLabel(
            self.frame_cliente,
            text="Cliente",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self._linha(self.frame_cliente, "Nome", nome, 1)
        self._linha(self.frame_cliente, "Telefone", telefone, 2)
        self._linha(self.frame_cliente, "Email", email, 3)
        self._linha(self.frame_cliente, "Observações", obs, 4)

        # ---------- ORDEM ----------
        ctk.CTkLabel(
            self.frame_ordem,
            text="Ordem de Serviço",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self._linha(self.frame_ordem, "Descrição", descricao, 1)
        self._linha(self.frame_ordem, "Data", data, 2)
        self._linha(self.frame_ordem, "Prioridade", prioridade, 3)
        self._linha(self.frame_ordem, "Status", status, 4)
        self._linha(self.frame_ordem, "Responsável", responsavel, 5)

        self.frame_cliente.grid_columnconfigure(1, weight=1)
        self.frame_ordem.grid_columnconfigure(1, weight=1)

    # ==================================================
    # UTIL
    # ==================================================
    def _linha(self, frame, titulo, valor, row):
        ctk.CTkLabel(
            frame,
            text=f"{titulo}:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=row, column=0, padx=10, pady=4, sticky="w")

        ctk.CTkLabel(
            frame,
            text=valor if valor else "-"
        ).grid(row=row, column=1, padx=10, pady=4, sticky="w")

    # ==================================================
    # VOLTAR
    # ==================================================
    def mostrar_lista(self):
        self.frame_detalhes.pack_forget()
        self.frame_lista.pack(fill="both", expand=True)

