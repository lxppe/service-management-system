import customtkinter as ctk
from database.db import cadastrar_cliente_e_os
from datetime import datetime


class TelaCadastro(ctk.CTkFrame):
    def __init__(self, master, mostrar_dashboard):
        super().__init__(master)

        # ================== TÍTULO ==================
        ctk.CTkLabel(
            self,
            text="Cadastro de Ordem de Serviço",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        # ================== CONTAINER PRINCIPAL ==================
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # ================== CLIENTE ==================
        self.frame_cliente = ctk.CTkFrame(self.container)
        self.frame_cliente.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.frame_cliente,
            text="Dados do Cliente",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="w")

        self.nome_add = self._campo(self.frame_cliente, "Nome *", 1)
        self.tel_add = self._campo(self.frame_cliente, "Telefone *", 2)
        self.tel_add.bind("<KeyRelease>", self.validar_tel)

        self.email_add = self._campo(self.frame_cliente, "Email", 3)
        self.obs_add = self._campo(self.frame_cliente, "Observações", 4)

        # ================== ORDEM DE SERVIÇO ==================
        self.frame_os = ctk.CTkFrame(self.container)
        self.frame_os.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            self.frame_os,
            text="Ordem de Serviço",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="w")

        self.desc_add = self._campo(self.frame_os, "Descrição *", 1)
        self.data_add = self._campo(self.frame_os, "Data de abertura *", 2)
        self.data_add.bind("<KeyRelease>", self.validar_data)

        # prioridade
        ctk.CTkLabel(self.frame_os, text="Prioridade *").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.prior_val = ctk.StringVar(value="Baixa")
        self.prior_add = ctk.CTkComboBox(
            self.frame_os,
            values=["Baixa", "Media", "Alta"],
            variable=self.prior_val
        )
        self.prior_add.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # status
        ctk.CTkLabel(self.frame_os, text="Status *").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.status_val = ctk.StringVar(value="Aberto")
        self.status_add = ctk.CTkComboBox(
            self.frame_os,
            values=["Aberto", "Em andamento", "Concluido"],
            variable=self.status_val
        )
        self.status_add.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.resp_add = self._campo(self.frame_os, "Responsável", 5)

        # ================== AÇÕES ==================
        self.frame_acoes = ctk.CTkFrame(self)
        self.frame_acoes.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.frame_acoes,
            text="Salvar Ordem",
            height=40,
            command=self.cadastrar
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.frame_acoes,
            text="Voltar",
            height=40,
            command=mostrar_dashboard
        ).pack(side="right", padx=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=5)

        self._configurar_grid()

    # ================== UTIL ==================
    def _campo(self, frame, texto, row):
        ctk.CTkLabel(frame, text=texto).grid(
            row=row, column=0, padx=10, pady=5, sticky="w"
        )
        entry = ctk.CTkEntry(frame)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry

    def _configurar_grid(self):
        for frame in (self.frame_cliente, self.frame_os):
            frame.grid_columnconfigure(1, weight=1)

    # ================== AÇÃO CADASTRAR ==================
    def cadastrar(self):
        nome = self.nome_add.get()
        tel = self.tel_add.get()
        email = self.email_add.get()
        obs = self.obs_add.get()

        desc = self.desc_add.get()
        data = self.data_add.get()
        prior = self.prior_val.get()
        status = self.status_val.get()
        resp = self.resp_add.get()

        if not nome or not tel or not desc or not data:
            self.status_label.configure(
                text="Preencha todos os campos obrigatórios.",
                text_color="red"
            )
            return

        if not self.data_valida(data):
            self.status_label.configure(
                text="Data inválida (dd/mm/aaaa)",
                text_color="red"
            )
            return

        cadastrar_cliente_e_os(
            nome, tel, email, obs,
            desc, data, prior, status, resp
        )

        self.status_label.configure(
            text="Ordem de serviço cadastrada com sucesso!",
            text_color="green"
        )

        self._limpar_campos()

    def _limpar_campos(self):
        for campo in (
            self.nome_add, self.tel_add, self.email_add,
            self.obs_add, self.desc_add, self.data_add, self.resp_add
        ):
            campo.delete(0, "end")

    # ================== VALIDAÇÕES ==================
    def validar_tel(self, event):
        texto = event.widget.get()
        numeros = "".join(c for c in texto if c.isdigit())

        novo = ""
        for i, c in enumerate(numeros):
            if i == 0:
                novo += "("
            if i == 2:
                novo += ") "
            if i == 7:
                novo += "-"
            novo += c

        event.widget.delete(0, "end")
        event.widget.insert(0, novo[:15])

    def validar_data(self, event):
        texto = event.widget.get()
        numeros = "".join(c for c in texto if c.isdigit())

        novo = ""
        for i, c in enumerate(numeros):
            if i in (2, 4):
                novo += "/"
            novo += c

        event.widget.delete(0, "end")
        event.widget.insert(0, novo[:10])

    def data_valida(self, data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False
