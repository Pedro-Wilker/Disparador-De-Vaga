import smtplib
from email.message import EmailMessage

remetente = "x"
senha_app = "x" 
destinatario = "x@gmail.com"

msg = EmailMessage()
msg['Subject'] = "Teste do meu Mini App em Python!"
msg['From'] = remetente
msg['To'] = destinatario
msg.set_content("Fala dev! Se você está lendo isso, a conexão do Python com o Gmail funcionou perfeitamente!")

print("Conectando ao servidor do Gmail...")

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha_app)
        smtp.send_message(msg)
    print("✅ Sucesso! O e-mail foi enviado. Verifique sua caixa de entrada.")
except Exception as e:
    print(f"❌ Ops, deu erro na conexão: {e}")