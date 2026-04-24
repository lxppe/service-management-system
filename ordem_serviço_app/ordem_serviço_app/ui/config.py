import customtkinter as ctk
import tkinter as tk

class TelaConfig(ctk.CTkFrame):
    def __init__(self, master, mostrar_dashboard):
        super().__init__(master)

        label = ctk.CTkLabel(self, text="Configurações",font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        tema_frame = ctk.CTkFrame(self)
        tema_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            tema_frame,
            text='Tema:',
            width=80
        ).pack(side="left", padx=(0,10))

        radios_frame = ctk.CTkFrame(tema_frame)
        radios_frame.pack(side="left", fill="x")

        self.escolha = tk.StringVar(value="op2") 

        ctk.CTkRadioButton(
            radios_frame,
            text="Claro",
            variable=self.escolha,
            value="op1",
            command=lambda: master.mudar_tema(self.escolha)
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            radios_frame,
            text="Escuro",
            variable=self.escolha,
            value="op2",
            command=lambda: master.mudar_tema(self.escolha)
        ).pack(anchor="w", pady=2)


        voltar_dashboard = ctk.CTkButton(self, text="voltar", command=mostrar_dashboard).pack(pady=(1))