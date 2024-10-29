from flask import Flask, redirect, request, url_for
from transbank.webpay.webpay_plus.transaction import Transaction

# Configuración para el entorno de pruebas de Transbank
Transaction.commerce_code = '597055555532'           # Código de comercio de prueba
Transaction.api_key = '597055555532-LlaveApi'        # API Key de prueba
Transaction.environment = 'INTEGRACION'              # Modo de integración

app = Flask(__name__)

@app.route('/iniciar_pago')
def iniciar_pago():
    # Crear transacción
    response = Transaction.create(
        buy_order="orden12345",
        session_id="sesion1234",
        amount=10000,
        return_url=url_for('confirmar_pago', _external=True)  # URL de retorno
    )
    
    # Verificación de URL y token para depuración
    print("https://webpay3gint.transbank.cl/webpayserver/initTransaction", response.url)
    print("e9d555262db0f989e49d724b4db0b0af367cc415cde41f500a776550fc5fddd3", response.token)
    
    # Redirigir al usuario a Webpay para completar el pago
    return redirect(f"{response.url}?token_ws={response.token}")

@app.route('/confirmar_pago')
def confirmar_pago():
    # Obtener el token de la URL de retorno
    token = request.args.get('token_ws')
    response = Transaction.commit(token)
    
    if response.status == 'AUTHORIZED':
        return "Pago exitoso"
    else:
        return "Pago fallido"

if __name__ == '__main__':
    app.run(debug=True)