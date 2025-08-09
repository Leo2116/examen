from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from models import get_db_connection, init_db

app = Flask(__name__)
CORS(app)

# Inicializamos la base de datos al arrancar la app
init_db()

@app.get("/")
def root():
    return jsonify({"ok": True, "service": "retos-api"})

@app.get("/health")
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

@app.get('/retos')
def get_retos():
    params = []
    where = []
    categoria = request.args.get('categoria')
    dificultad = request.args.get('dificultad')
    estado = request.args.get('estado')
    buscar = request.args.get('q')

    if categoria:
        where.append("categoria = %s")
        params.append(categoria)
    if dificultad:
        where.append("dificultad = %s")
        params.append(dificultad)
    if estado:
        where.append("estado = %s")
        params.append(estado)
    if buscar:
        where.append("(LOWER(titulo) LIKE LOWER(%s) OR LOWER(descripcion) LIKE LOWER(%s))")
        like = f"%{buscar}%"
        params.extend([like, like])

    sql = """SELECT id, titulo, descripcion, categoria, dificultad, estado, creado_en, actualizado_en
             FROM retos"""
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC"

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200

@app.post('/retos')
def create_reto():
    data = request.get_json(force=True) or {}
    titulo = data.get('titulo')
    if not titulo:
        return jsonify({'error': 'titulo es requerido'}), 400

    descripcion = data.get('descripcion')
    categoria = data.get('categoria')
    dificultad = data.get('dificultad')
    estado = data.get('estado') or 'pendiente'

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO retos (titulo, descripcion, categoria, dificultad, estado)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, titulo, descripcion, categoria, dificultad, estado, creado_en, actualizado_en
    """, (titulo, descripcion, categoria, dificultad, estado))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(row), 201

@app.put('/retos/<int:reto_id>')
def update_reto(reto_id):
    data = request.get_json(force=True) or {}
    allowed = ['titulo', 'descripcion', 'categoria', 'dificultad', 'estado']
    sets = []
    params = []

    for k in allowed:
        if k in data and data[k] is not None:
            sets.append(f"{k} = %s")
            params.append(data[k])

    if not sets:
        return jsonify({'error': 'Nada para actualizar'}), 400

    sets.append("actualizado_en = NOW()")
    params.append(reto_id)

    sql = f"""UPDATE retos SET {', '.join(sets)}
              WHERE id = %s
              RETURNING id, titulo, descripcion, categoria, dificultad, estado, creado_en, actualizado_en"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql, params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not row:
        return jsonify({'error': 'Reto no encontrado'}), 404
    return jsonify(row), 200

@app.delete('/retos/<int:reto_id>')
def delete_reto(reto_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM retos WHERE id = %s", (reto_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({'error': 'Reto no encontrado'}), 404
    return jsonify({'message': 'Reto eliminado'}), 200

if __name__ == '__main__':
    print("URL MAP:", app.url_map)
    app.run(host='127.0.0.1', port=5000, debug=True)
