import customtkinter as ctk
from database.db import buscar_aberto, buscar_andamento, buscar_concluido


class TelaDashboard(ctk.CTkFrame):
    def __init__(self, master, mostrar_cadastro, mostrar_detos, mostrar_listar, mostrar_config):
        super().__init__(master)

        # ================== TÍTULO ==================
        ctk.CTkLabel(
            self,
            text="Gestão de Ordens de Serviço",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Resumo geral do sistema",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 20))

        # ================== STATUS (CARDS) ==================
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(pady=10)

        self.card_aberto = self._criar_card(status_frame, "Abertas", "0")
        self.card_and = self._criar_card(status_frame, "Em andamento", "0")
        self.card_conclu = self._criar_card(status_frame, "Concluídas", "0")

        self.card_aberto.grid(row=0, column=0, padx=10)
        self.card_and.grid(row=0, column=1, padx=10)
        self.card_conclu.grid(row=0, column=2, padx=10)

        # ================== AÇÕES ==================
        acoes_frame = ctk.CTkFrame(self)
        acoes_frame.pack(pady=25)

        ctk.CTkButton(
            acoes_frame,
            text="+ Criar nova ordem de serviço",
            width=260,
            height=40,
            command=mostrar_cadastro
        ).pack(pady=6)

        ctk.CTkButton(
            acoes_frame,
            text="📋 Ordens de serviço",
            width=260,
            height=40,
            command=mostrar_detos
        ).pack(pady=6)

        ctk.CTkButton(
            acoes_frame,
            text="👤 Histórico de clientes",
            width=260,
            height=40,
            command=mostrar_listar
        ).pack(pady=6)

        ctk.CTkButton(
            acoes_frame,
            text="⚙️ Configurações",
            width=260,
            height=40,
            command=mostrar_config
        ).pack(pady=6)

        # atualiza os números
        self.status_atualizar()

    # ================== CARD DE STATUS ==================
    def _criar_card(self, master, titulo, valor):
        card = ctk.CTkFrame(master, width=160, height=90)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=13)
        ).pack(pady=(10, 0))

        label_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=26, weight="bold")
        )
        label_valor.pack(pady=(5, 10))

        card.label_valor = label_valor
        return card

    # ================== ATUALIZAR STATUS ==================
    def status_atualizar(self):
        qtd_aberto = len(buscar_aberto())
        qtd_and = len(buscar_andamento())
        qtd_conclu = len(buscar_concluido())

        self.card_aberto.label_valor.configure(text=str(qtd_aberto))
        self.card_and.label_valor.configure(text=str(qtd_and))
        self.card_conclu.label_valor.configure(text=str(qtd_conclu))
