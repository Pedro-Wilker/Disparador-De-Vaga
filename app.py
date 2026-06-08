import os
import smtplib
import re
from email.message import EmailMessage
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMETENTE = os.getenv("MEU_EMAIL")
SENHA_APP = os.getenv("SENHA_APP")

CV_PT = "Pedro_Wilker_Curriculo_PT.pdf"
CV_EN = "Pedro_Wilker_Resume_EN.pdf"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DisparadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Disparador de Vagas")
        self.geometry("600x650")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.var_idioma = ctk.StringVar(value="PT")
        self.var_anexar = ctk.BooleanVar(value=True)

        self.frame_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_inteligente = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_manual = ctk.CTkFrame(self, fg_color="transparent")

        self.montar_tela_menu()
        self.montar_tela_inteligente()
        self.montar_tela_manual()

        self.mostrar_tela(self.frame_menu)

    def mostrar_tela(self, frame_destino):
        self.frame_menu.grid_forget()
        self.frame_inteligente.grid_forget()
        self.frame_manual.grid_forget()
        frame_destino.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def montar_tela_menu(self):
        titulo = ctk.CTkLabel(self.frame_menu, text="Escolha o Modo de Envio", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(100, 40))

        btn_inteligente = ctk.CTkButton(
            self.frame_menu, text="Modo Inteligente (Colar Padrão)", 
            font=ctk.CTkFont(size=15, weight="bold"), height=50, width=300,
            command=lambda: self.mostrar_tela(self.frame_inteligente)
        )
        btn_inteligente.pack(pady=10)

        btn_manual = ctk.CTkButton(
            self.frame_menu, text="Modo Manual", 
            font=ctk.CTkFont(size=15, weight="bold"), height=50, width=300, fg_color="#4CAF50", hover_color="#45a049",
            command=lambda: self.mostrar_tela(self.frame_manual)
        )
        btn_manual.pack(pady=10)

    def montar_tela_inteligente(self):
        btn_voltar = ctk.CTkButton(self.frame_inteligente, text="← Voltar", width=80, fg_color="transparent", border_width=1, command=lambda: self.mostrar_tela(self.frame_menu))
        btn_voltar.pack(anchor="w", pady=(0, 10))

        lbl_titulo = ctk.CTkLabel(self.frame_inteligente, text="Cole o Padrão da Vaga", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_titulo.pack(anchor="w", pady=(0, 10))

        self.texto_padrao = ctk.CTkTextbox(self.frame_inteligente, width=560, height=300)
        self.texto_padrao.pack(pady=(0, 15))

        frame_opcoes = ctk.CTkFrame(self.frame_inteligente, fg_color="transparent")
        frame_opcoes.pack(fill="x", pady=10)

        switch_anexo = ctk.CTkSwitch(frame_opcoes, text="Enviar com Anexo?", variable=self.var_anexar, font=ctk.CTkFont(weight="bold"))
        switch_anexo.pack(side="left", padx=(0, 20))

        radio_pt = ctk.CTkRadioButton(frame_opcoes, text="CV Português", variable=self.var_idioma, value="PT")
        radio_pt.pack(side="left", padx=10)
        
        radio_en = ctk.CTkRadioButton(frame_opcoes, text="CV Inglês", variable=self.var_idioma, value="EN")
        radio_en.pack(side="left", padx=10)

        self.btn_enviar_inteligente = ctk.CTkButton(self.frame_inteligente, text="Extrair e Enviar", height=45, font=ctk.CTkFont(weight="bold"), command=self.processar_envio_inteligente)
        self.btn_enviar_inteligente.pack(pady=20, fill="x")

    def processar_envio_inteligente(self):
        texto_cru = self.texto_padrao.get("1.0", "end-1c").strip()
        if not texto_cru:
            messagebox.showwarning("Atenção", "Cole o texto padrão antes de enviar!")
            return

        destinatario = ""
        assunto = ""
        corpo_email = ""

        match_email = re.search(r'Email do recrutador:\s*([^\n]+)', texto_cru, re.IGNORECASE)
        if match_email:
            destinatario = match_email.group(1).strip()
  
        match_assunto = re.search(r'Assunto:\s*([^\n]+)', texto_cru, re.IGNORECASE)
        if match_assunto:
            assunto = match_assunto.group(1).strip()

        if match_assunto:
            linha_assunto_completa = match_assunto.group(0)
            indice_inicio_corpo = texto_cru.find(linha_assunto_completa) + len(linha_assunto_completa)
            corpo_email = texto_cru[indice_inicio_corpo:].strip()
        else:
            corpo_email = texto_cru 

        if not destinatario or not assunto:
            messagebox.showwarning("Atenção", "Não foi possível identificar o 'Email do recrutador:' ou o 'Assunto:' no texto colado. Verifique o padrão.")
            return

        self.btn_enviar_inteligente.configure(state="disabled", text="Enviando...")
        self.update()
        self.executar_envio(destinatario, assunto, corpo_email, self.btn_enviar_inteligente, "Extrair e Enviar")
        self.texto_padrao.delete("1.0", "end")

    def montar_tela_manual(self):
        btn_voltar = ctk.CTkButton(self.frame_manual, text="← Voltar", width=80, fg_color="transparent", border_width=1, command=lambda: self.mostrar_tela(self.frame_menu))
        btn_voltar.pack(anchor="w", pady=(0, 10))

        lbl_titulo = ctk.CTkLabel(self.frame_manual, text="Preenchimento Manual", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        self.entry_destinatario = ctk.CTkEntry(self.frame_manual, placeholder_text="E-mail do Recrutador", width=560)
        self.entry_destinatario.pack(pady=(0, 10))

        self.entry_assunto = ctk.CTkEntry(self.frame_manual, placeholder_text="Assunto do E-mail", width=560)
        self.entry_assunto.pack(pady=(0, 10))

        self.texto_manual = ctk.CTkTextbox(self.frame_manual, width=560, height=200)
        self.texto_manual.pack(pady=(0, 15))

        frame_opcoes = ctk.CTkFrame(self.frame_manual, fg_color="transparent")
        frame_opcoes.pack(fill="x", pady=5)

        switch_anexo = ctk.CTkSwitch(frame_opcoes, text="Enviar com Anexo?", variable=self.var_anexar, font=ctk.CTkFont(weight="bold"))
        switch_anexo.pack(side="left", padx=(0, 20))

        radio_pt = ctk.CTkRadioButton(frame_opcoes, text="CV Português", variable=self.var_idioma, value="PT")
        radio_pt.pack(side="left", padx=10)
        
        radio_en = ctk.CTkRadioButton(frame_opcoes, text="CV Inglês", variable=self.var_idioma, value="EN")
        radio_en.pack(side="left", padx=10)

        self.btn_enviar_manual = ctk.CTkButton(self.frame_manual, text="Enviar Manualmente", fg_color="#4CAF50", hover_color="#45a049", height=45, font=ctk.CTkFont(weight="bold"), command=self.processar_envio_manual)
        self.btn_enviar_manual.pack(pady=20, fill="x")

    def processar_envio_manual(self):
        destinatario = self.entry_destinatario.get().strip()
        assunto = self.entry_assunto.get().strip()
        corpo_email = self.texto_manual.get("1.0", "end-1c").strip()

        if not destinatario or not assunto:
            messagebox.showwarning("Atenção", "Preencha o destinatário e o assunto!")
            return

        self.btn_enviar_manual.configure(state="disabled", text="Enviando...")
        self.update()
        self.executar_envio(destinatario, assunto, corpo_email, self.btn_enviar_manual, "Enviar Manualmente")
        self.entry_destinatario.delete(0, "end")
        self.entry_assunto.delete(0, "end")
        self.texto_manual.delete("1.0", "end")

    def executar_envio(self, destinatario, assunto, corpo_email, botao_referencia, texto_botao_original):
        idioma = self.var_idioma.get()
        anexar = self.var_anexar.get()

        try:
            msg = EmailMessage()
            msg['Subject'] = assunto
            msg['From'] = EMAIL_REMETENTE
            msg['To'] = destinatario
            msg.set_content(corpo_email)

            if anexar:
                arquivo_escolhido = CV_PT if idioma == "PT" else CV_EN
                pasta_atual = os.path.dirname(os.path.abspath(__file__))
                caminho_pdf = os.path.join(pasta_atual, arquivo_escolhido)

                if not os.path.exists(caminho_pdf):
                    messagebox.showerror("Erro de Arquivo", f"Não foi possível encontrar o arquivo:\n{arquivo_escolhido}\nCertifique-se que ele está na mesma pasta do app.")
                    botao_referencia.configure(state="normal", text=texto_botao_original)
                    return

                with open(caminho_pdf, 'rb') as f:
                    dados_pdf = f.read()
                
                msg.add_attachment(dados_pdf, maintype='application', subtype='pdf', filename=arquivo_escolhido)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)
                
            mensagem_sucesso = f"Candidatura enviada para {destinatario}!"
            if anexar:
                mensagem_sucesso += f"\nAnexo: {arquivo_escolhido}"
            else:
                mensagem_sucesso += "\n(Sem anexo)"
                
            messagebox.showinfo("Sucesso!", mensagem_sucesso)

        except Exception as e:
            messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao conectar com o Gmail:\n{e}")
        
        finally:
            botao_referencia.configure(state="normal", text=texto_botao_original)

if __name__ == "__main__":
    app = DisparadorApp()
    app.mainloop()