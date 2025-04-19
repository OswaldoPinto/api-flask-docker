from flask import Flask, jsonify, request

app = Flask(__name__)

posts = []
post_counter = 1  # Contador global para asignar IDs únicos

@app.route('/')
def home():
    return 'Bienvenido a la API de posts'

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    global post_counter  # Usar el contador global
    data = request.get_json()
    # Agregar un ID único a la publicación
    new_post = {
        "id": post_counter,
        "title": data["title"],
        "content": data["content"]
    }
    posts.append(new_post)
    post_counter += 1  # Incrementar el contador para la siguiente publicación
    return jsonify({'message': 'Post creado correctamente', 'post': new_post}), 201

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    # Buscar la publicación por ID
    post = next((post for post in posts if post["id"] == id), None)
    if post:
        # Actualizar el post
        post["title"] = data["title"]
        post["content"] = data["content"]
        return jsonify({'message': 'Post actualizado correctamente', 'post': post}), 200
    else:
        return jsonify({'message': 'Post no encontrado'}), 404
    
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global posts
    # Buscar si existe un post con ese ID
    post = next((post for post in posts if post["id"] == id), None)
    if post:
        # Filtrar la lista para eliminar el post con ese ID
        posts = [p for p in posts if p["id"] != id]
        return jsonify({'message': 'Post eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'Post no encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

