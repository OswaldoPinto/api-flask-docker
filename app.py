from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables desde el entorno
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Inicializar Flask
app = Flask(__name__)

# Configurar la base de datos usando las variables
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Crear modelo de Post en la base de datos
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Post({self.id}, {self.title}, {self.content})"

# Ruta de inicio
@app.route('/')
def home():
    return 'Bienvenido a la API de posts'

# Obtener todos los posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])

# Crear un nuevo post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Faltan campos requeridos: title o content'}), 400

    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post creado correctamente', 'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content}}), 201

# Actualizar un post
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if post:
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Post actualizado correctamente', 'post': {'id': post.id, 'title': post.title, 'content': post.content}}), 200
    else:
        return jsonify({'message': 'Post no encontrado'}), 404

# Eliminar un post
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Post no encontrado'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        print(" Tablas creadas (o ya existentes)")
    app.run(host='0.0.0.0', port=5000, debug=True)



