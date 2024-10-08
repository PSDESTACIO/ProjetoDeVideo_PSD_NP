from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
import os
import uuid
import sqlite3

app = Flask(__name__)

# Responsável pela segurança de formulários
app.secret_key = 'Chave_secretica_123' # Segurança
# Pasta no qual vai ser direcionado
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Tamanho MAX do Video.
app.config['MAX_CONTENT_LENGTH'] = 50 * 1048576  


#Responsável pela extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv'}



def render_videolist():
    # Design feito a partir do projeto anterior do Belém.
    # Verifica se o vídeo e o título foram enviados no formulário

    # Lista todos os arquivos no diretório de uploads
    video_files = os.listdir(app.config['UPLOAD_FOLDER']) 

    # Filtra apenas os arquivos de vídeo permitidos
    video_files = [f for f in video_files if allowed_file(f)]

    # Ordena os arquivos por data de criação, do mais recente ao mais antigo
    video_files.sort(key=lambda x: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True) 
    
    # Cria uma lista para armazenar os vídeos e seus títulos
    videos = []  
    for video_file in video_files:
        
        local_file = video_file[:-4]

        title_file = local_file + '.title.txt' # Gera o nome do arquivo de título correspondente ao vídeo
        description_file = local_file + '.desc.txt' # Gera o nome do arquivo de descrição correspondente ao vídeo

        # Constrói o caminho completo do arquivo de título
        title_path = os.path.join(app.config['UPLOAD_FOLDER'], title_file) 
        description_path = os.path.join(app.config['UPLOAD_FOLDER'], description_file)

        title = "Sem Título" # Define o título padrão como "Sem Título"
        description = "Sem Descrição" # Define a descrição padrão como "Sem Título"

        # Se o arquivo de título existir, lê o título do arquivo
        if os.path.exists(title_path):
            with open(title_path, 'r') as f:
                title = f.read().strip()

        # Se o arquivo de descrição existir, lê a descrição do arquivo
        if os.path.exists(description_path):
            with open(description_path, 'r') as f:
                description = f.read().strip()

        # Adiciona o vídeo e seu título à lista
        videos.append({'filename': video_file, 'title': title, 'description': description})
    
    return videos

def init_db():
    with sqlite3.connect('videos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()



def save_metadata_to_db(filename, title, description):
    with sqlite3.connect('videos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO videos (filename, title, description)
        VALUES (?, ?, ?)
        ''', (filename, title, description))
        conn.commit()



def delete_metadata_from_db(filename):
    with sqlite3.connect('videos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM videos WHERE filename = ?', (filename,))
        conn.commit()



# Rotas
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login.html', methods=['POST'])
def rota_usuario():
    # Deixa a sessão com vazia
    session['nome_usuario_input'] = '' 
    
    return render_template('login.html')

@app.route('/logging', methods=['POST'])
def rota_usuario_logando():
    # Pega o input do formulario do login
    nomeUsuario = request.form['nome_usuario_input'] 
    # Armazenar na sessão
    session['nome_usuario_input'] = nomeUsuario 

    return redirect(url_for('rota_video'))

@app.route('/videos.html')
def rota_video():
    # Pega o valor da sessão
    nomeUsuario = session.get('nome_usuario_input') 
    videos = render_videolist()
    return render_template('videos.html', nomeUsuario=nomeUsuario, videos=videos)

@app.route('/editar_videos.html')
def rota_adicionar_video():
    # Pega o valor da sessão
    nomeUsuario = session.get('nome_usuario_input') 
    videos = render_videolist()
    return render_template('editar_videos.html', nomeUsuario=nomeUsuario, videos=videos)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Verifica se o vídeo e o título foram enviados no formulário
    if 'video' not in request.files or 'video_title' not in request.form:
        return redirect('/video.html')

    file = request.files['video']
    title = request.form['video_title']
    description = request.form['video_description']

    # Se o nome do arquivo estiver vazio, redireciona de volta para a página de vídeos
    if file.filename == '':
        return redirect('/video.html')
    
    # Se o arquivo for permitido, processa o upload
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        local_file = filename[:-4]

        title_filename = local_file + '.title.txt' # Gera o nome do arquivo do título correspondente ao vídeo
        description_filename = local_file + '.desc.txt' # Gera o nome do arquivo da descrição correspondente ao vídeo
        
        # Salva o título do vídeo em um arquivo de texto
        with open(os.path.join(app.config['UPLOAD_FOLDER'], title_filename), 'w') as f:
            f.write(title)

        # Salva a descrição do vídeo em um arquivo de texto
        with open(os.path.join(app.config['UPLOAD_FOLDER'], description_filename), 'w') as f:
            f.write(description)

        #duration, width, height = get_video_metadata(file_path)
        #save_metadata_to_db(filename, title, description, duration, width, height)

        save_metadata_to_db(filename, title, description)
        return redirect(url_for('rota_adicionar_video'))
    else:
        return redirect(request.url)
    
@app.route('/delete_video/<filename>', methods=['POST'])
def delete_video(filename):
    try:
        # Constrói o caminho completo do arquivo de vídeo a ser deletado
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        local_path = file_path[:-4]

        # Gera os caminhos dos arquivos de título e descrição correspondentes ao vídeo
        title_file_path = local_path + '.title.txt'
        description_file_path = local_path + '.desc.txt'
        
        # Se o arquivo de vídeo existir, deleta o arquivo de vídeo, título e descrição
        if os.path.exists(file_path):
            os.remove(file_path)

            if os.path.exists(title_file_path):
                os.remove(title_file_path)

            if os.path.exists(description_file_path):
                os.remove(description_file_path)

            delete_metadata_from_db(filename)
            print(f"Arquivo '{filename}' deletado com sucesso.")

        else:
            print(f"Arquivo '{filename}' não encontrado para deletar.")
    except Exception as e:
        print(f"Erro ao deletar arquivo '{filename}': {str(e)}")
    
    return redirect(url_for('rota_adicionar_video'))

@app.route('/editar_video.html/<filename>', methods=['POST'])
def editar_video(filename):

    new_title = request.form['video_title']
    new_file = request.files['video']
    new_description = request.form['video_description']

    local_file = filename[:-4]

    if new_file and allowed_file(new_file.filename):

        new_local_file = new_file.filename[:-4]

        new_title_file = filename.rsplit('_')[0] + "_" + new_local_file + '.title.txt'
        new_description_file = filename.rsplit('_')[0] + "_" + new_local_file + '.desc.txt'

        new_file_transition = secure_filename(f"{filename.rsplit('_')[0]+'_'+new_file.filename}")

        if new_file and allowed_file(new_file.filename):
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], local_file+'.title.txt'), os.path.join(app.config['UPLOAD_FOLDER'], new_title_file))
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], local_file+'.desc.txt'), os.path.join(app.config['UPLOAD_FOLDER'], new_description_file))
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], new_file_transition))
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_transition))
    else:
        new_title_file = local_file + '.title.txt'
        new_description_file = local_file + '.desc.txt'

    with open(os.path.join(app.config['UPLOAD_FOLDER'], new_title_file), 'w') as f:
        f.write(new_title)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], new_description_file), 'w') as f:
        f.write(new_description)

    return redirect(url_for('rota_adicionar_video'))

# Abre o aplicativo na porta 5000 e o roda.
if __name__ == '__main__':
    init_db()
    app.run(debug = True, port = 5000)