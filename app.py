from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session
import jwt
import datetime
import base64
import json
import os
from functools import wraps
import re
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = 'secreto_del_culto'
app.config['JWT_SECRET_KEY'] = 'secreto_jwt_del_culto'

# Almacenamiento de usuarios y mensajes
users_db = {}
messages_db = []

# Clave para el cifrado de texto
cipher_key = b'ZKvw2mJT5gAw5ChMVKkJaULLLdPwT2alqPvMhWqOr0E='
cipher = Fernet(cipher_key)

# Clave del sumo sacerdote (visible en su perfil)
priest_key = "dark3ssUnveiled"

# Decorador para verificar el JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            flash('¡Acceso denegado! Se requiere iniciar sesión', 'error')
            return redirect(url_for('login'))
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except:
            flash('¡Token inválido! Por favor inicia sesión de nuevo', 'error')
            return redirect(url_for('login'))
        return f(current_user, *args, **kwargs)
    return decorated

# Decorador para verificar roles
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            if current_user['role'] != role and (role == 'chosen' and current_user['role'] != 'priest'):
                flash(f'¡Acceso denegado! Se requiere el rol: {role}', 'error')
                return redirect(url_for('dashboard'))
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        users_db[username] = {
            'password': password,
            'role': 'initiate'
        }
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users_db or users_db[username]['password'] != password:
            flash('Credenciales inválidas', 'error')
            return redirect(url_for('login'))
        
        # Asegurarse de usar el rol actualizado del usuario desde users_db
        current_role = users_db[username]['role']
        
        # Crear JWT
        token = jwt.encode({
            'username': username,
            'role': current_role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['JWT_SECRET_KEY'], algorithm="HS256")
        
        # Establecer cookie
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('token', token)
        
        flash('¡Has ingresado con éxito!', 'success')
        return resp
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('token')
    flash('Has cerrado sesión correctamente', 'success')
    return resp

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    # Verificar si el rol del usuario en el token coincide con su rol actual en la base de datos
    username = current_user['username']
    token_role = current_user['role']
    
    if username in users_db:
        db_role = users_db[username]['role']
        # Si hay una discrepancia en los roles, mostrar una notificación
        if token_role != db_role:
            flash(f'¡Tu rol ha sido actualizado a {db_role}! Por favor, cierra sesión e inicia nuevamente para acceder a tus nuevos privilegios.', 'warning')
    
    return render_template('dashboard.html', user=current_user)

@app.route('/mural')
@token_required
def mural(current_user):
    return render_template('mural.html', messages=messages_db, user=current_user)

@app.route('/post-message', methods=['POST'])
@token_required
def post_message(current_user):
    message = request.form['message']
    
    # NO filtrar el mensaje para permitir XSS deliberadamente
    messages_db.append({
        'author': current_user['username'],
        'content': message,
        'timestamp': datetime.datetime.utcnow()
    })
    
    flash('¡Mensaje publicado!', 'success')
    return redirect(url_for('mural'))

@app.route('/promote')
def promote():
    # Verificar si la solicitud proviene del bot simulado
    referrer = request.headers.get('Referer', '')
    is_bot_simulation = session.get('bot_simulation', False)
    
    # Solo permitir promociones si la solicitud viene de la simulación del bot
    # o si ya tienes un rol mayor que 'initiate'
    if 'simulate-bot' not in referrer and not is_bot_simulation:
        return jsonify({'success': False, 'message': 'Acceso directo no permitido'})
    
    token = request.cookies.get('token')
    if token:
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            username = data['username']
            role = data['role']
            
            # Solo permitir promoción si el usuario es 'initiate'
            if username in users_db and username != 'highpriest' and role == 'initiate':
                # Promover al usuario
                users_db[username]['role'] = 'chosen'
                
                # Este token actualizado no se aplicará inmediatamente al usuario
                # pero se puede usar para crear un nuevo token en la respuesta
                new_token = jwt.encode({
                    'username': username,
                    'role': 'chosen',
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, app.config['JWT_SECRET_KEY'], algorithm="HS256")
                
                # El usuario deberá cerrar sesión e iniciar nuevamente para obtener
                # este nuevo token con sus privilegios actualizados
                resp = make_response(jsonify({'success': True, 'message': 'Promoción exitosa. Cierra sesión e inicia nuevamente para activar tus privilegios.'}))
                # Opcionalmente se puede actualizar el token aquí, pero es mejor que el usuario inicie sesión nuevamente
                # resp.set_cookie('token', new_token)
                return resp
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return jsonify({'success': False, 'message': 'Token no encontrado'})

@app.route('/simulate-bot')
def simulate_bot():
    # Simular que el sacerdote lee todos los mensajes
    # Si encuentra un script, lo "ejecuta"
    session['bot_simulation'] = True  # Marca que estamos en una simulación
    promotion_done = False
    promoted_user = None

    for message in messages_db:
        if '<script>' in message['content'] and '</script>' in message['content']:
            # Extraer URL del script
            script_content = re.search(r'<script>(.*?)</script>', message['content'])
            if script_content:
                script = script_content.group(1)
                if 'fetch(\'/promote\')' in script or "fetch('/promote')" in script:
                    # El sacerdote "ejecuta" el script y activa la promoción
                    # para el autor del mensaje
                    author = message['author']
                    if author in users_db and users_db[author]['role'] == 'initiate':
                        # Actualizar el rol en la base de datos
                        users_db[author]['role'] = 'chosen'
                        promotion_done = True
                        promoted_user = author
    
    # Crear un nuevo token para el usuario promovido
    if promotion_done and promoted_user:
        # Esto asegura que el usuario tenga su nuevo rol cuando inicie sesión nuevamente
        # También guardamos esta información en la sesión para mostrarla en la página
        session['promoted_user'] = promoted_user
    
    return render_template('simulate_bot.html')

@app.route('/gallery')
@token_required
@role_required('chosen')
def gallery(current_user):
    # Esta ruta solo está disponible para los "elegidos"
    return render_template('gallery.html', user=current_user)

@app.route('/highpriest/profile')
@token_required
def highpriest_profile(current_user):
    # Perfil público del sumo sacerdote con la clave oculta a simple vista
    return render_template('highpriest.html', priest_key=priest_key, user=current_user)

@app.route('/temple/veil/<path:code>')
@token_required
@role_required('chosen')
def temple_veil(current_user, code):
    if code != '4f5e3':
        return render_template('error.html', message='Sala no encontrada')
    
    # Mensaje cifrado que contiene la FLAG
    encrypted_message = cipher.encrypt(b'FLAG{XSS_D4RKW4LL_M4ST3R}')
    encrypted_message = base64.b64encode(encrypted_message).decode('utf-8')
    
    return render_template('temple.html', encrypted_message=encrypted_message)

@app.route('/decrypt', methods=['POST'])
@token_required
@role_required('chosen')
def decrypt(current_user):
    key = request.form['key']
    encrypted_message = request.form['message']
    step = request.form.get('step', '1')
    
    # Primer paso: verificar la clave del sacerdote
    if step == '1':
        if key != priest_key:
            return jsonify({'success': False, 'message': 'Clave incorrecta'})
        
        # Devolver el hash MD5 en lugar de la FLAG
        return jsonify({
            'success': True, 
            'message': 'MD5:013c44bcd89d8e07603853e6b6edd031',
            'next_step': True
        })
    
    # Segundo paso: verificar la clave descifrada del hash
    elif step == '2':
        if key != 'welcomehacker':
            return jsonify({'success': False, 'message': 'Secuencia incorrecta'})
        
        try:
            # Ahora sí devolvemos la FLAG real
            decrypted = 'FLAG{XSS_D4RKW4LL_M4ST3R}'
            return jsonify({'success': True, 'message': decrypted, 'final': True})
        except:
            return jsonify({'success': False, 'message': 'Error al descifrar'})
    
    return jsonify({'success': False, 'message': 'Solicitud inválida'})

@app.route('/reset-simulation')
def reset_simulation():
    # Limpiar la variable de sesión de simulación
    if 'bot_simulation' in session:
        session.pop('bot_simulation')
    
    # Redirigir al dashboard
    return redirect(url_for('dashboard'))

# Inicializar al sumo sacerdote
@app.before_first_request
def create_highpriest():
    users_db['highpriest'] = {
        'password': 'secretooscuro',
        'role': 'priest'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 