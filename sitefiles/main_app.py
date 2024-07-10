from flask import Flask, render_template # type: ignore

app = Flask(__name__) # Recebe a aplicação

# Rotas
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login.html')
def rota_usuario():
    return render_template('login.html')

@app.route('/videos.html')
def rota_video():
    return render_template('videos.html')

@app.route('/editar_videos.html')
def rota_editar_video():
    return render_template('editar_videos.html')

# Abre o aplicativo na porta 5500 e o roda.
if __name__ == '__main__':
    app.run(debug = True, port = 5000) 