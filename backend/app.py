from flask import Flask, request, jsonify
from flask_cors import CORS
from models import get_db_connection, init_db

app = Flask(__name__)
CORS(app)

# Llamar a la función de inicialización de la base de datos directamente
# Esto reemplaza el obsoleto @app.before_first_request
init_db()

@app.route('/retos', methods=['GET'])
def get_retos():
    categoria = request.args.get('categoria')
    dificultad = request.args.get('dificultad')
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT * FROM retos"
    params = []
    filters = []
    if categoria:
        filters.append("categoria = %s")
        params.append(categoria)
    if dificultad:
        filters.append("dificultad = %s")
        params.append(dificultad)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    cur.execute(query, params)
    retos = [
        dict(id=row[0], titulo=row[1], descripcion=row[2], categoria=row[3], dificultad=row[4], estado=row[5])
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return jsonify(retos)

@app.route('/retos', methods=['POST'])
def create_reto():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO retos (titulo, descripcion, categoria, dificultad, estado)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """, (data['titulo'], data['descripcion'], data['categoria'], data['dificultad'], data['estado']))
    reto_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': reto_id}), 201

@app.route('/retos/<int:reto_id>', methods=['PUT'])
def update_reto(reto_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE retos SET estado = %s WHERE id = %s
    """, (data['estado'], reto_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Reto actualizado'})

@app.route('/retos/<int:reto_id>', methods=['DELETE'])
def delete_reto(reto_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM retos WHERE id = %s", (reto_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Reto eliminado'})

if __name__ == '__main__':
    app.run(debug=True)