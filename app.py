import os
import smtplib
import re
import sqlite3
import imaplib
import urllib.request
import json
import webbrowser
from datetime import datetime
from email.message import EmailMessage
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMETENTE = os.getenv("MEU_EMAIL")
SENHA_APP = os.getenv("SENHA_APP")

CV_PT = "Pedro_Wilker_Curriculo_PT.pdf"
CV_EN = "Pedro_Wilker_Resume_EN.pdf"

C = {
    "bg":          "#FFFFFF",
    "bg_secondary":"#F8F8F7",
    "bg_tertiary": "#F1F0EE",
    "sidebar":     "#FFFFFF",

    "indigo":      "#4F46E5",
    "indigo_hover":"#4338CA",
    "indigo_light":"#EEF2FF",
    "indigo_text": "#4F46E5",

    "green":       "#16A34A",
    "green_hover": "#15803D",
    "green_light": "#F0FDF4",
    "green_text":  "#16A34A",

    "border":      "#E5E4E0",
    "border_med":  "#D1D0CC",

    "text":        "#1A1A1A",
    "text_sec":    "#6B7280",
    "text_ter":    "#9CA3AF",

    "amber_bg":    "#FEF3C7",
    "amber_text":  "#92400E",
}

FONT_FAMILY = "Segoe UI"


def label(parent, text, size=13, weight="normal", color=None, anchor="w", **kw):
    return tk.Label(
        parent, text=text,
        font=(FONT_FAMILY, size, weight),
        fg=color or C["text"],
        bg=parent["bg"] if "bg" in parent.keys() else C["bg"],
        anchor=anchor, **kw
    )

def eyebrow(parent, text):
    lbl = tk.Label(
        parent, text=text.upper(),
        font=(FONT_FAMILY, 9, "bold"),
        fg=C["text_ter"],
        bg=parent["bg"] if "bg" in parent.keys() else C["bg"],
        anchor="w"
    )
    return lbl

def separator(parent, color=None):
    return tk.Frame(parent, height=1, bg=color or C["border"])

def card_frame(parent, padx=20, pady=16, bg=None):
    outer = tk.Frame(parent, bg=C["border"], padx=1, pady=1)
    inner = tk.Frame(outer, bg=bg or C["bg"], padx=padx, pady=pady)
    inner.pack(fill="both", expand=True)
    return outer, inner

def pill_badge(parent, text, bg, fg):
    return tk.Label(
        parent, text=text,
        font=(FONT_FAMILY, 10),
        fg=fg, bg=bg,
        padx=8, pady=2
    )

def primary_btn(parent, text, command, color=None, hover_color=None, width=None):
    color = color or C["indigo"]
    hover_color = hover_color or C["indigo_hover"]
    kw = {"width": width} if width else {}
    btn = tk.Button(
        parent, text=text, command=command,
        font=(FONT_FAMILY, 13, "bold"),
        fg="#FFFFFF", bg=color,
        activeforeground="#FFFFFF", activebackground=hover_color,
        relief="flat", cursor="hand2",
        padx=20, pady=11,
        bd=0, **kw
    )
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.configure(bg=color))
    return btn

def text_btn(parent, text, command):
    btn = tk.Button(
        parent, text=text, command=command,
        font=(FONT_FAMILY, 12),
        fg=C["text_sec"], bg=C["bg"],
        activeforeground=C["text"], activebackground=C["bg"],
        relief="flat", cursor="hand2",
        padx=0, pady=0, bd=0
    )
    btn.bind("<Enter>", lambda e: btn.configure(fg=C["text"]))
    btn.bind("<Leave>", lambda e: btn.configure(fg=C["text_sec"]))
    return btn


class ToggleSwitch(tk.Frame):
    def __init__(self, master, text, variable, on_color=None, **kw):
        bg = master["bg"] if "bg" in master.keys() else C["bg"]
        super().__init__(master, bg=bg, **kw)
        self._var = variable
        self._on_color = on_color or C["indigo"]

        self._canvas = tk.Canvas(self, width=36, height=20, bg=bg, highlightthickness=0, cursor="hand2")
        self._canvas.pack(side="left")
        self._canvas.bind("<Button-1>", self._toggle)

        tk.Label(self, text=text, font=(FONT_FAMILY, 12),
                 fg=C["text_sec"], bg=bg, cursor="hand2").pack(side="left", padx=(8, 0))

        variable.trace_add("write", lambda *_: self._draw())
        self._draw()

    def _draw(self):
        c = self._canvas
        c.delete("all")
        on = self._var.get()
        track_color = self._on_color if on else C["border_med"]
        c.create_rounded_rect = self._rounded_rect
        self._rounded_rect(c, 0, 2, 36, 18, radius=8, fill=track_color, outline="")
        thumb_x = 20 if on else 4
        c.create_oval(thumb_x, 4, thumb_x + 12, 16, fill="#FFFFFF", outline="")

    def _rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kw):
        points = [
            x1+radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2,
            x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius,
            x1, y1+radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kw)

    def _toggle(self, _=None):
        self._var.set(not self._var.get())


class RadioPill(tk.Frame):
    def __init__(self, master, options, variable, **kw):
        bg = master["bg"] if "bg" in master.keys() else C["bg"]
        super().__init__(master, bg=bg, **kw)
        self._var = variable
        self._btns = {}

        container = tk.Frame(self, bg=C["border"], padx=1, pady=1)
        container.pack()
        inner = tk.Frame(container, bg=C["bg_secondary"])
        inner.pack()

        for val, text in options:
            btn = tk.Label(
                inner, text=text,
                font=(FONT_FAMILY, 11),
                fg=C["text_sec"], bg=C["bg_secondary"],
                padx=14, pady=6, cursor="hand2"
            )
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, v=val: self._select(v))
            self._btns[val] = btn

        variable.trace_add("write", lambda *_: self._refresh())
        self._refresh()

    def _select(self, val):
        self._var.set(val)

    def _refresh(self):
        val = self._var.get()
        for v, btn in self._btns.items():
            if v == val:
                btn.configure(fg=C["indigo"], bg=C["indigo_light"],
                               font=(FONT_FAMILY, 11, "bold"))
            else:
                btn.configure(fg=C["text_sec"], bg=C["bg_secondary"],
                               font=(FONT_FAMILY, 11))


class SidebarItem(tk.Frame):
    def __init__(self, master, text, icon_char, command, **kw):
        super().__init__(master, bg=C["sidebar"], cursor="hand2", **kw)
        self._command = command
        self._active = False

        self._bar = tk.Frame(self, width=3, bg=C["sidebar"])
        self._bar.pack(side="left", fill="y")

        self._icon = tk.Label(self, text=icon_char, font=(FONT_FAMILY, 14),
                              fg=C["text_ter"], bg=C["sidebar"], width=2)
        self._icon.pack(side="left", padx=(6, 4), pady=10)

        self._lbl = tk.Label(self, text=text, font=(FONT_FAMILY, 12),
                             fg=C["text_sec"], bg=C["sidebar"], anchor="w")
        self._lbl.pack(side="left", fill="x", expand=True, pady=10)

        for w in [self, self._icon, self._lbl, self._bar]:
            w.bind("<Button-1>", lambda e: self._command())
            w.bind("<Enter>", self._hover_on)
            w.bind("<Leave>", self._hover_off)

    def _hover_on(self, _=None):
        if not self._active:
            for w in [self, self._icon, self._lbl]:
                w.configure(bg=C["bg_secondary"])

    def _hover_off(self, _=None):
        if not self._active:
            for w in [self, self._icon, self._lbl]:
                w.configure(bg=C["sidebar"])

    def set_active(self, active):
        self._active = active
        if active:
            self._bar.configure(bg=C["indigo"])
            self._lbl.configure(fg=C["indigo"], bg=C["indigo_light"],
                                 font=(FONT_FAMILY, 12, "bold"))
            self._icon.configure(fg=C["indigo"], bg=C["indigo_light"])
            self.configure(bg=C["indigo_light"])
        else:
            self._bar.configure(bg=C["sidebar"])
            self._lbl.configure(fg=C["text_sec"], bg=C["sidebar"],
                                 font=(FONT_FAMILY, 12))
            self._icon.configure(fg=C["text_ter"], bg=C["sidebar"])
            self.configure(bg=C["sidebar"])


class JobPilot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JobPilot")
        self.geometry("900x650")
        self.minsize(850, 550)
        self.configure(bg=C["bg_tertiary"])
        self.resizable(True, True)

        self.var_idioma = tk.StringVar(value="PT")
        self.var_anexar = tk.BooleanVar(value=True)
        
        # --- Variáveis da Fase 3 ---
        self._urls_vagas = {}
        self._vagas_carregadas = False

        self.pasta_atual = os.path.dirname(os.path.abspath(__file__))
        self.caminho_db = os.path.join(self.pasta_atual, "vagas.db")
        self._init_db()

        self._nav_items = {}
        self._frames = {}
        self._active_key = None

        self._build()
        self._nav_to("inteligente")

    def _init_db(self):
        con = sqlite3.connect(self.caminho_db)
        con.execute('''CREATE TABLE IF NOT EXISTS candidaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_envio TEXT, destinatario TEXT, assunto TEXT, status TEXT
        )''')
        con.commit(); con.close()

    def _registrar(self, dest, assunto):
        try:
            con = sqlite3.connect(self.caminho_db)
            con.execute(
                "INSERT INTO candidaturas (data_envio,destinatario,assunto,status) VALUES(?,?,?,?)",
                (datetime.now().strftime("%d/%m/%Y %H:%M"), dest, assunto, "Aguardando")
            )
            con.commit(); con.close()
        except Exception as e:
            print(e)

    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._sidebar = tk.Frame(self, bg=C["sidebar"], width=200)
        self._sidebar.grid(row=0, column=0, sticky="nsew")
        self._sidebar.grid_propagate(False)

        tk.Frame(self, bg=C["border"], width=1).grid(row=0, column=0, sticky="nse")

        logo_frame = tk.Frame(self._sidebar, bg=C["sidebar"], pady=20)
        logo_frame.pack(fill="x", padx=16)

        logo_pill = tk.Frame(logo_frame, bg=C["indigo"], padx=10, pady=5)
        logo_pill.pack(side="left")
        tk.Label(logo_pill, text="JP", font=(FONT_FAMILY, 12, "bold"),
                 fg="#FFFFFF", bg=C["indigo"]).pack()

        tk.Label(logo_frame, text="JobPilot", font=(FONT_FAMILY, 15, "bold"),
                 fg=C["text"], bg=C["sidebar"]).pack(side="left", padx=(10, 0))

        separator(self._sidebar, C["border"]).pack(fill="x", padx=16, pady=(0, 16))

        self._nav_section("Enviar")
        self._add_nav("inteligente", "⚡", "Inteligente")
        self._add_nav("manual",      "✏", "Manual")

        tk.Frame(self._sidebar, bg=C["sidebar"], height=8).pack()
        separator(self._sidebar, C["border"]).pack(fill="x", padx=16, pady=8)

        # --- Seção Fase 3 ---
        self._nav_section("Oportunidades")
        self._add_nav("buscar", "🔍", "Buscar Vagas")

        tk.Frame(self._sidebar, bg=C["sidebar"], height=8).pack()
        separator(self._sidebar, C["border"]).pack(fill="x", padx=16, pady=8)
        # --------------------

        self._nav_section("Dados")
        self._add_nav("dashboard", "▦", "Histórico")

        tk.Frame(self._sidebar, bg=C["sidebar"]).pack(fill="both", expand=True)
        separator(self._sidebar, C["border"]).pack(fill="x", padx=16)
        tk.Label(self._sidebar, text="Pedro Wilker · v3.0",
                 font=(FONT_FAMILY, 10), fg=C["text_ter"], bg=C["sidebar"]
                 ).pack(anchor="w", padx=20, pady=12)

        self._content_area = tk.Frame(self, bg=C["bg_tertiary"])
        self._content_area.grid(row=0, column=1, sticky="nsew")
        self._content_area.grid_rowconfigure(1, weight=1)
        self._content_area.grid_columnconfigure(0, weight=1)

        self._topbar = tk.Frame(self._content_area, bg=C["bg"], pady=14)
        self._topbar.grid(row=0, column=0, sticky="ew")
        separator(self._content_area, C["border"]).grid(row=0, column=0, sticky="sew")

        self._page_title = tk.Label(self._topbar, text="",
                                     font=(FONT_FAMILY, 15, "bold"),
                                     fg=C["text"], bg=C["bg"], anchor="w")
        self._page_title.pack(side="left", padx=24)

        self._page_sub = tk.Label(self._topbar, text="",
                                   font=(FONT_FAMILY, 11),
                                   fg=C["text_ter"], bg=C["bg"], anchor="w")
        self._page_sub.pack(side="left", padx=(0, 24))

        self._action_btn_frame = tk.Frame(self._topbar, bg=C["bg"])
        self._action_btn_frame.pack(side="right", padx=24)

        self._pages_container = tk.Frame(self._content_area, bg=C["bg_tertiary"])
        self._pages_container.grid(row=1, column=0, sticky="nsew")
        self._pages_container.grid_rowconfigure(0, weight=1)
        self._pages_container.grid_columnconfigure(0, weight=1)

        self._frames["inteligente"] = self._build_inteligente()
        self._frames["manual"]      = self._build_manual()
        self._frames["dashboard"]   = self._build_dashboard()
        self._frames["buscar"]      = self._build_buscar() # Frame Fase 3

    def _nav_section(self, text):
        tk.Label(self._sidebar, text=text.upper(),
                 font=(FONT_FAMILY, 9, "bold"), fg=C["text_ter"],
                 bg=C["sidebar"], anchor="w"
                 ).pack(fill="x", padx=20, pady=(4, 2))

    def _add_nav(self, key, icon, label_text):
        item = SidebarItem(self._sidebar, label_text, icon,
                           command=lambda k=key: self._nav_to(k))
        item.pack(fill="x", padx=10, pady=1)
        self._nav_items[key] = item

    def _nav_to(self, key):
        for k, item in self._nav_items.items():
            item.set_active(k == key)

        for frame in self._frames.values():
            frame.grid_forget()

        self._frames[key].grid(row=0, column=0, sticky="nsew")
        self._active_key = key

        titles = {
            "inteligente": ("Modo inteligente", "Cole o bloco da vaga, extraímos tudo"),
            "manual":      ("Modo manual",       "Preencha os campos manualmente"),
            "dashboard":   ("Histórico",          "Todas as candidaturas registradas"),
            "buscar":      ("Vagas Globais",      "Oportunidades remotas em tempo real"), # Título Fase 3
        }
        t, s = titles[key]
        self._page_title.configure(text=t)
        self._page_sub.configure(text=s)

        for w in self._action_btn_frame.winfo_children():
            w.destroy()

        if key == "inteligente":
            primary_btn(self._action_btn_frame, "⚡  Extrair e enviar",
                        self._processar_inteligente).pack()
        elif key == "manual":
            primary_btn(self._action_btn_frame, "✉  Enviar agora",
                        self._processar_manual,
                        color=C["green"], hover_color=C["green_hover"]).pack()
        elif key == "dashboard":
            primary_btn(self._action_btn_frame, "🔄 Sincronizar Respostas", 
                        self._sincronizar_respostas, color=C["indigo"]).pack()
            self._carregar_dashboard()
        # --- Botão Fase 3 ---
        elif key == "buscar":
            primary_btn(self._action_btn_frame, "🔄 Atualizar Vagas", 
                        self._carregar_vagas, color=C["indigo"]).pack()
            if not self._vagas_carregadas:
                self.after(200, self._carregar_vagas)

    def _build_inteligente(self):
        frame = tk.Frame(self._pages_container, bg=C["bg_tertiary"])
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        outer, inner = card_frame(frame, padx=20, pady=16)
        outer.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))

        eyebrow(inner, "Texto da vaga").pack(anchor="w", pady=(0, 8))
        self.texto_inteligente = tk.Text(
            inner, height=11, wrap="word",
            font=(FONT_FAMILY, 12), fg=C["text"], bg=C["bg_secondary"],
            relief="flat", bd=0,
            insertbackground=C["indigo"],
            selectbackground=C["indigo_light"],
            padx=12, pady=10,
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["indigo"]
        )
        self.texto_inteligente.pack(fill="both", expand=True)

        outer2, inner2 = card_frame(frame, padx=20, pady=16)
        outer2.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        eyebrow(inner2, "Configurações de envio").pack(anchor="w", pady=(0, 12))

        opts = tk.Frame(inner2, bg=C["bg"])
        opts.pack(fill="x")

        ToggleSwitch(opts, "Anexar currículo", self.var_anexar).pack(side="left")

        tk.Frame(opts, bg=C["bg"], width=24).pack(side="left")

        RadioPill(opts, [("PT", "Português"), ("EN", "Inglês")],
                  self.var_idioma).pack(side="left")

        return frame

    def _build_manual(self):
        frame = tk.Frame(self._pages_container, bg=C["bg_tertiary"])
        frame.grid_columnconfigure(0, weight=1)

        outer, inner = card_frame(frame, padx=20, pady=16)
        outer.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        inner.grid_columnconfigure(0, weight=1)

        def field_entry(parent, label_text, placeholder):
            eyebrow(parent, label_text).pack(anchor="w", pady=(0, 4))
            e = tk.Entry(
                parent, font=(FONT_FAMILY, 12),
                fg=C["text"], bg=C["bg_secondary"],
                relief="flat", bd=0,
                insertbackground=C["green"],
                highlightthickness=1, highlightbackground=C["border"],
                highlightcolor=C["green"]
            )
            e.pack(fill="x", ipady=8, pady=(0, 14))
            
            e.insert(0, placeholder)
            e.configure(fg=C["text_ter"])
            e.bind("<FocusIn>", lambda ev, en=e, ph=placeholder: (
                en.delete(0, "end") if en.get() == ph else None,
                en.configure(fg=C["text"])
            ))
            e.bind("<FocusOut>", lambda ev, en=e, ph=placeholder: (
                (en.insert(0, ph), en.configure(fg=C["text_ter"])) if not en.get() else None
            ))
            return e

        self.entry_dest   = field_entry(inner, "Destinatário", "recrutador@empresa.com")
        self.entry_assunto = field_entry(inner, "Assunto", "Candidatura — Desenvolvedor Backend")

        eyebrow(inner, "Corpo do e-mail").pack(anchor="w", pady=(0, 4))
        self.texto_manual = tk.Text(
            inner, height=7, wrap="word",
            font=(FONT_FAMILY, 12), fg=C["text"], bg=C["bg_secondary"],
            relief="flat", bd=0,
            insertbackground=C["green"],
            padx=12, pady=10,
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["green"]
        )
        self.texto_manual.pack(fill="both")

        outer2, inner2 = card_frame(frame, padx=20, pady=16)
        outer2.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        eyebrow(inner2, "Configurações de envio").pack(anchor="w", pady=(0, 12))
        opts = tk.Frame(inner2, bg=C["bg"])
        opts.pack(fill="x")
        ToggleSwitch(opts, "Anexar currículo", self.var_anexar,
                     on_color=C["green"]).pack(side="left")
        tk.Frame(opts, bg=C["bg"], width=24).pack(side="left")
        RadioPill(opts, [("PT", "Português"), ("EN", "Inglês")],
                  self.var_idioma).pack(side="left")

        return frame

    def _build_dashboard(self):
        frame = tk.Frame(self._pages_container, bg=C["bg_tertiary"])
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        stats_frame = tk.Frame(frame, bg=C["bg_tertiary"])
        stats_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._stat_vals = []
        stat_defs = [
            ("Total enviadas", C["indigo"]),
            ("Esta semana",    C["green"]),
            ("Aguardando",     "#D97706"),
        ]
        for i, (lbl_text, accent) in enumerate(stat_defs):
            padx = (0, 10) if i < 2 else 0
            outer = tk.Frame(stats_frame, bg=C["border"], padx=1, pady=1)
            outer.grid(row=0, column=i, sticky="ew", padx=padx)
            inner = tk.Frame(outer, bg=C["bg"], padx=18, pady=14)
            inner.pack(fill="both", expand=True)

            tk.Frame(inner, bg=accent, width=3, height=36).pack(side="left", padx=(0, 12))

            col = tk.Frame(inner, bg=C["bg"])
            col.pack(side="left")

            val_lbl = tk.Label(col, text="—", font=(FONT_FAMILY, 22, "bold"),
                               fg=C["text"], bg=C["bg"])
            val_lbl.pack(anchor="w")
            tk.Label(col, text=lbl_text, font=(FONT_FAMILY, 11),
                     fg=C["text_ter"], bg=C["bg"]).pack(anchor="w")
            self._stat_vals.append(val_lbl)

        outer_t, inner_t = card_frame(frame, padx=0, pady=0)
        outer_t.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        eyebrow(inner_t, "Registros").pack(anchor="w", padx=20, pady=(14, 10))
        separator(inner_t, C["border"]).pack(fill="x")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("JP.Treeview",
                        background=C["bg"],
                        foreground=C["text"],
                        fieldbackground=C["bg"],
                        rowheight=36,
                        borderwidth=0,
                        font=(FONT_FAMILY, 11))
        style.map("JP.Treeview",
                  background=[("selected", C["indigo_light"])],
                  foreground=[("selected", C["indigo"])])
        style.configure("JP.Treeview.Heading",
                        background=C["bg"],
                        foreground=C["text_ter"],
                        font=(FONT_FAMILY, 10, "bold"),
                        borderwidth=0, relief="flat")
        style.layout("JP.Treeview", [("JP.Treeview.treearea", {"sticky": "nsew"})])

        cols = ("ID", "Data", "Destinatário", "Assunto", "Status")
        self.tabela = ttk.Treeview(inner_t, columns=cols, show="headings",
                                   height=10, style="JP.Treeview")

        config = [("ID", 40, "center"), ("Data", 120, "center"),
                  ("Destinatário", 190, "w"), ("Assunto", 260, "w"),
                  ("Status", 100, "center")]
        for col, w, a in config:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=w, anchor=a, minwidth=w)

        self.tabela.tag_configure("aguardando", foreground="#B45309")
        self.tabela.tag_configure("respondido", foreground=C["green"])

        sb = ttk.Scrollbar(inner_t, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=sb.set)
        self.tabela.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 8))
        sb.pack(side="right", fill="y", padx=(0, 8), pady=(0, 8))

        return frame

    # --- INÍCIO DA TELA FASE 3 ---
    def _build_buscar(self):
        frame = tk.Frame(self._pages_container, bg=C["bg_tertiary"])
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        outer_t, inner_t = card_frame(frame, padx=0, pady=0)
        outer_t.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        top_bar = tk.Frame(inner_t, bg=C["bg"])
        top_bar.pack(fill="x", padx=20, pady=(14, 10))
        
        eyebrow(top_bar, "API Remotive - Vagas Dev").pack(side="left")
        tk.Label(top_bar, text="(Dica: Duplo clique na vaga para abri-la no navegador)", 
                 font=(FONT_FAMILY, 9, "italic"), fg=C["text_ter"], bg=C["bg"]).pack(side="right")
        separator(inner_t, C["border"]).pack(fill="x")

        self.tabela_vagas = ttk.Treeview(inner_t, columns=("Empresa", "Título da Vaga", "Tipo", "Publicação"), 
                                         show="headings", height=15, style="JP.Treeview")
        
        config = [("Empresa", 160, "w"), ("Título da Vaga", 300, "w"), 
                  ("Tipo", 100, "center"), ("Publicação", 100, "center")]
        
        for col, w, a in config:
            self.tabela_vagas.heading(col, text=col)
            self.tabela_vagas.column(col, width=w, anchor=a, minwidth=w)

        sb = ttk.Scrollbar(inner_t, orient="vertical", command=self.tabela_vagas.yview)
        self.tabela_vagas.configure(yscrollcommand=sb.set)
        self.tabela_vagas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 8))
        sb.pack(side="right", fill="y", padx=(0, 8), pady=(0, 8))

        self.tabela_vagas.bind("<Double-1>", self._abrir_link_vaga)
        return frame
    # --- FIM DA TELA FASE 3 ---

    def _carregar_dashboard(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        try:
            con = sqlite3.connect(self.caminho_db)
            cur = con.cursor()
            cur.execute("SELECT id, data_envio, destinatario, assunto, status FROM candidaturas ORDER BY id DESC")
            linhas = cur.fetchall()
            con.close()

            total = len(linhas)
            aguardando = sum(1 for r in linhas if r[4] == "Aguardando")
            hoje = datetime.now()
            semana = sum(1 for r in linhas if self._dias_atras(r[1]) <= 7)

            self._stat_vals[0].configure(text=str(total))
            self._stat_vals[1].configure(text=str(semana))
            self._stat_vals[2].configure(text=str(aguardando))

            for row in linhas:
                if row[4] == "Aguardando":
                    tag = ("aguardando",)
                elif row[4] == "Respondido":
                    tag = ("respondido",)
                else:
                    tag = ()
                self.tabela.insert("", "end", values=row, tags=tag)
        except Exception as e:
            print(e)

    def _dias_atras(self, data_str):
        try:
            return (datetime.now() - datetime.strptime(data_str, "%d/%m/%Y %H:%M")).days
        except:
            return 999

    # --- MÉTODOS DE LÓGICA FASE 3 ---
    def _carregar_vagas(self):
        for w in self._action_btn_frame.winfo_children():
            w.configure(text="Buscando API...", state="disabled")
        self.update()

        for item in self.tabela_vagas.get_children():
            self.tabela_vagas.delete(item)

        try:
            url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=40"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                dados = json.loads(response.read().decode())
            
            jobs = dados.get("jobs", [])
            for job in jobs:
                empresa = job.get("company_name", "Desconhecida")
                titulo = job.get("title", "Sem título")
                tipo = job.get("job_type", "").replace("_", " ").title()
                
                data_raw = job.get("publication_date", "")
                if data_raw:
                    ano, mes, dia = data_raw[:10].split("-")
                    data_fmt = f"{dia}/{mes}/{ano}"
                else:
                    data_fmt = ""
                
                iid = self.tabela_vagas.insert("", "end", values=(empresa, titulo, tipo, data_fmt))
                self._urls_vagas[iid] = job.get("url", "")

            self._vagas_carregadas = True
            
        except Exception as e:
            messagebox.showerror("Erro de Rede", f"Não foi possível buscar as vagas:\n{e}")
        
        finally:
            self._nav_to("buscar")

    def _abrir_link_vaga(self, event):
        selecao = self.tabela_vagas.selection()
        if selecao:
            iid = selecao[0]
            url = self._urls_vagas.get(iid)
            if url:
                webbrowser.open(url)
    # --------------------------------

    def _processar_inteligente(self):
        texto = self.texto_inteligente.get("1.0", "end-1c").strip()
        if not texto:
            messagebox.showwarning("Campo vazio", "Cole o texto da vaga antes de enviar.")
            return

        m_email  = re.search(r'Email do recrutador:\s*([^\n]+)', texto, re.IGNORECASE)
        m_assunto = re.search(r'Assunto:\s*([^\n]+)', texto, re.IGNORECASE)

        if not m_email or not m_assunto:
            messagebox.showwarning("Não encontrado",
                "Não foi possível identificar 'Email do recrutador:' ou 'Assunto:' no texto.")
            return

        dest    = m_email.group(1).strip()
        assunto = m_assunto.group(1).strip()
        linha   = m_assunto.group(0)
        corpo   = texto[texto.find(linha) + len(linha):].strip()

        self._enviar(dest, assunto, corpo,
                     callback_ok=lambda: self.texto_inteligente.delete("1.0", "end"))

    def _processar_manual(self):
        dest    = self.entry_dest.get().strip()
        assunto = self.entry_assunto.get().strip()
        corpo   = self.texto_manual.get("1.0", "end-1c").strip()

        placeholders = ["recrutador@empresa.com", "Candidatura — Desenvolvedor Backend"]
        if dest in placeholders: dest = ""
        if assunto in placeholders: assunto = ""

        if not dest or not assunto:
            messagebox.showwarning("Campos incompletos", "Preencha o destinatário e o assunto.")
            return

        def limpar():
            self.entry_dest.delete(0, "end")
            self.entry_assunto.delete(0, "end")
            self.texto_manual.delete("1.0", "end")

        self._enviar(dest, assunto, corpo, callback_ok=limpar)
        
    def _sincronizar_respostas(self):
        try:
            con = sqlite3.connect(self.caminho_db)
            cur = con.cursor()
            cur.execute("SELECT id, destinatario FROM candidaturas WHERE status = 'Aguardando'")
            aguardando = cur.fetchall()
            
            if not aguardando:
                messagebox.showinfo("Sincronização", "Você não tem candidaturas 'Aguardando' resposta.")
                con.close()
                return

            for w in self._action_btn_frame.winfo_children():
                w.configure(text="Sincronizando...", state="disabled")
            self.update()

            destinatarios_aguardando = {row[1].lower(): row[0] for row in aguardando}

            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(EMAIL_REMETENTE, SENHA_APP)
            mail.select("inbox")

            atualizados = 0

            for dest, req_id in destinatarios_aguardando.items():
                status, mensagens = mail.search(None, f'FROM "{dest}"')
                if status == "OK":
                    ids_mensagens = mensagens[0].split()
                    if ids_mensagens:  
                        cur.execute("UPDATE candidaturas SET status = 'Respondido' WHERE id = ?", (req_id,))
                        atualizados += 1

            con.commit()
            con.close()
            mail.logout()

            self._carregar_dashboard()
            
            if atualizados > 0:
                messagebox.showinfo("Sucesso!", f"Radar concluído! {atualizados} novas respostas detectadas na sua caixa de entrada.")
            else:
                messagebox.showinfo("Sincronização", "Nenhuma resposta nova dos recrutadores ainda.")

        except Exception as e:
            messagebox.showerror("Erro no Radar", f"Falha ao ler os e-mails:\n{e}")
            
        finally:
            self._nav_to("dashboard")

    def _enviar(self, dest, assunto, corpo, callback_ok=None):
        idioma = self.var_idioma.get()
        anexar = self.var_anexar.get()
        try:
            msg = EmailMessage()
            msg["Subject"] = assunto
            msg["From"]    = EMAIL_REMETENTE
            msg["To"]      = dest
            msg.set_content(corpo)

            if anexar:
                arquivo = CV_PT if idioma == "PT" else CV_EN
                caminho = os.path.join(self.pasta_atual, arquivo)
                if not os.path.exists(caminho):
                    messagebox.showerror("Arquivo não encontrado",
                                         f"Currículo não encontrado:\n{arquivo}")
                    return
                with open(caminho, "rb") as f:
                    msg.add_attachment(f.read(), maintype="application",
                                       subtype="pdf", filename=arquivo)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)

            self._registrar(dest, assunto)
            messagebox.showinfo("Enviado!", f"Candidatura enviada para {dest} e registrada.")
            if callback_ok:
                callback_ok()

        except Exception as e:
            messagebox.showerror("Erro ao enviar", str(e))


if __name__ == "__main__":
    app = JobPilot()
    app.mainloop()