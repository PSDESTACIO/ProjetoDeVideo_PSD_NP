from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__) # Recebe a aplicação
app.secret_key = 'Chave_secretica_123' # Segurança

# Rotas
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login.html', methods=['POST'])
def rota_usuario():
    session['nome_usuario_input'] = '' # Deixa a sessão com vazia
    return render_template('login.html')

@app.route('/logging', methods=['POST'])
def rota_usuario_logando():
    nomeUsuario = request.form['nome_usuario_input'] # Pega o input do formulario do login
    session['nome_usuario_input'] = nomeUsuario  # Armazenar na sessão
    return redirect(url_for('rota_video'))

@app.route('/videos.html')
def rota_video():
    nomeUsuario = session.get('nome_usuario_input') # Pega o valor da sessão
    return render_template('videos.html',nomeUsuario=nomeUsuario)

@app.route('/editar_videos.html')
def rota_editar_video():
    nomeUsuario = session.get('nome_usuario_input') # Pega o valor da sessão
    return render_template('editar_videos.html',nomeUsuario=nomeUsuario)

# Abre o aplicativo na porta 5000 e o roda.
if __name__ == '__main__':
    app.run(debug = True, port = 5000)

#tutorial Ana