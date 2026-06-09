# 🚀 JobPilot - CRM Pessoal & Disparador de Vagas

O **JobPilot** é uma aplicação desktop nativa construída em Python para otimizar, gerenciar e automatizar o processo de candidatura a vagas de emprego. Mais do que um disparador de e-mails, ele funciona como um CRM pessoal, rastreando respostas de recrutadores e buscando oportunidades remotas em tempo real.

Construído com um Design System customizado usando apenas bibliotecas nativas do Python (com exceção do gerenciador de variáveis de ambiente), o aplicativo é leve, rápido e portátil.

---

## ✨ Funcionalidades Principais

* **⚡ Modo Inteligente (Smart Extract):** Cole o texto padrão de uma vaga. O sistema extrai automaticamente o e-mail do recrutador, o assunto e o corpo da mensagem.
* **✉️ Envio Manual & Anexos Dinâmicos:** Interface limpa para envio de e-mails, com seleção rápida (Toggle) para anexar currículos em Português ou Inglês.
* **📊 Dashboard (CRM Local):** Banco de dados SQLite integrado que registra todas as candidaturas, com métricas de envios semanais e totais.
* **🔄 Radar de Respostas (IMAP):** O aplicativo lê sua caixa de entrada do Gmail de forma segura e cruza os dados com o banco local. Se um recrutador responder, o status da vaga muda de *Aguardando* para *Respondido* automaticamente.
* **🔍 Caçador de Vagas (API Remotive):** Integração com API global para buscar vagas remotas em Desenvolvimento de Software. Com um duplo clique na vaga, o site é aberto diretamente no navegador.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x** (Lógica, UI e Integrações)
* **Tkinter & TTK** (Interface Gráfica + Design System Customizado)
* **SQLite3** (Banco de Dados Local)
* **smtplib & imaplib** (Envio e Leitura de E-mails via Gmail)
* **urllib & JSON** (Consumo de APIs externas)
* **python-dotenv** (Gerenciamento de credenciais seguras)

---

## ⚙️ Pré-requisitos e Configuração da Conta Google

Para que o sistema consiga enviar e ler e-mails de forma segura, você não deve usar sua senha pessoal do Gmail. É necessário criar uma **Senha de Aplicativo**.

1. Acesse as configurações da sua Conta Google ([myaccount.google.com](https://myaccount.google.com/)).
2. Vá em **Segurança** e ative a **Verificação em duas etapas**.
3. Na barra de pesquisa, busque por **Senhas de app**.
4. Crie uma nova senha (ex: "App JobPilot") e copie a senha de 16 letras gerada.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone [https://github.com/SEU_USUARIO/jobpilot.git](https://github.com/SEU_USUARIO/jobpilot.git)
cd jobpilot
```

### 2. Instale a única dependência externa

Como a aplicação utiliza 99% de bibliotecas nativas, você só precisa instalar o gerenciador de variáveis de ambiente:

**Bash**

```
pip install python-dotenv
```

### 3. Configure as Credenciais (.env)

Crie um arquivo chamado **exatamente** `.env` na raiz do projeto e adicione suas credenciais:

**Snippet de código**

```
MEU_EMAIL=seu_email_real@gmail.com
SENHA_APP=suasenhadedezeisseisletras
```

### 4. Adicione seus Currículos

O sistema procura pelos currículos na mesma pasta do código. Adicione seus arquivos em formato PDF com os seguintes nomes exatos (ou altere as variáveis `CV_PT` e `CV_EN` no código `app.py`):

* `Pedro_Wilker_Curriculo_PT.pdf`
* `Pedro_Wilker_Resume_EN.pdf`

### 5. Rode o Aplicativo

**Bash**

```
python app.py
```

## 📦 Como Compilar o Executável (.exe)

Se desejar transformar o código em um aplicativo nativo do Windows de 1 único arquivo (sem precisar rodar via terminal), utilize o  **PyInstaller** .

1. Instale o PyInstaller:

**Bash**

```
pip install pyinstaller
```

2. Compile o código:

**Bash**

```
pyinstaller --noconsole --onefile app.py
```

3. **Passo Final:** Vá até a pasta `dist` que foi gerada, recorte o arquivo `app.exe` e cole na pasta raiz do projeto. O executável precisa estar na mesma pasta que o arquivo `.env`, o banco `vagas.db` e os currículos em `.pdf` para funcionar corretamente.

## 🔒 Segurança e Privacidade

Este projeto foi configurado com um `.gitignore` rigoroso. Se for fazer um *fork* ou clonar, certifique-se de **nunca** commitar o arquivo `.env` contendo suas credenciais de e-mail, nem seus currículos pessoais, mantendo seus dados protegidos.
