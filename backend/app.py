from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = 'locagora-secret'
CORS(app)

DB = 'database.db'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------- UPLOAD ----------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------- BANCO ----------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS motos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL,
            regiao TEXT NOT NULL,
            imagem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def seed_motos():
    motos_padrao = [
        "DK 150",
        "DK 160",
        "SHI 175 Carburada ",
        "NK 150",
        "NH 190",
        "Crosser 150",
        "Factor 150",
        "JEF 150",
        "Avelloz AZX 160"
    ]

    conn = get_db()
    for nome in motos_padrao:
        existe = conn.execute(
            'SELECT id FROM motos WHERE nome=?', (nome,)
        ).fetchone()

        if not existe:
            conn.execute(
                'INSERT INTO motos (nome, estado, regiao, imagem) VALUES (?,?,?,?)',
                (
                    nome,
                    '0Km',
                    'Consulte sua região',
                    '/img/foto.jpg'  # imagem padrão
                )
            )

    conn.commit()
    conn.close()

init_db()
seed_motos()

# ---------- FRONT ----------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin.html')
def admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/<path:arquivo>')
def arquivos(arquivo):
    return send_from_directory(app.static_folder, arquivo)

# ---------- API ----------
@app.route('/api/motos')
def listar_motos():
    conn = get_db()
    motos = conn.execute('SELECT * FROM motos').fetchall()
    conn.close()
    return jsonify([dict(m) for m in motos])

@app.route('/api/motos', methods=['POST'])
def adicionar_moto():
    nome = request.form['nome']
    estado = request.form['estado']
    regiao = request.form['regiao']
    imagem = request.files['imagem']

    filename = imagem.filename
    imagem.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = get_db()
    conn.execute(
        'INSERT INTO motos (nome, estado, regiao, imagem) VALUES (?,?,?,?)',
        (nome, estado, regiao, f'/uploads/{filename}')
    )
    conn.commit()
    conn.close()

    return jsonify({'ok': True})

@app.route('/api/motos/<int:id>', methods=['PUT'])
def editar_moto(id):
    nome = request.form['nome']
    estado = request.form['estado']
    regiao = request.form['regiao']

    conn = get_db()

    if 'imagem' in request.files and request.files['imagem'].filename:
        imagem = request.files['imagem']
        filename = imagem.filename
        imagem.save(os.path.join(UPLOAD_FOLDER, filename))
        conn.execute(
            'UPDATE motos SET nome=?, estado=?, regiao=?, imagem=? WHERE id=?',
            (nome, estado, regiao, f'/uploads/{filename}', id)
        )
    else:
        conn.execute(
            'UPDATE motos SET nome=?, estado=?, regiao=? WHERE id=?',
            (nome, estado, regiao, id)
        )

    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/motos/<int:id>', methods=['DELETE'])
def deletar_moto(id):
    conn = get_db()
    conn.execute('DELETE FROM motos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ---------- ADMIN LOGIN ----------
@app.route('/admin/login', methods=['POST'])
def admin_login():
    senha_digitada = request.json.get('senha')

    senha_admin = os.getenv('ADMIN_PASSWORD')

    if not senha_admin:
        return jsonify({'ok': False, 'erro': 'Senha não configurada'}), 500

    if senha_digitada == senha_admin:
        session['admin'] = True
        return jsonify({'ok': True})

    return jsonify({'ok': False})


# ---------- START ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

