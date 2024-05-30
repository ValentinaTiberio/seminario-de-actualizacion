from flask import Flask, request, jsonify
from db import db

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        id = request.args.get('id')
        action = request.args.get('action')
        if id:
            return get_user(int(id))
        elif action:
            if action == 'get_groups':
                return get_groups()
            elif action == 'get_actions':
                return get_actions()
            elif action == 'get_group_action':
                return get_group_action()
            else:
                return get_users()
        else:
            return get_users()
    elif request.method == 'POST':
        action = request.args.get('action')
        if action:
            if action == 'create_user':
                return create_user()
            elif action == 'create_group':
                return create_group()
            elif action == 'create_action':
                return create_action()
            elif action == 'assign_action_to_group':
                return assign_action_to_group()
            elif action == 'get_groups_with_actions_and_users':
                return get_groups_with_actions_and_users()
            else:
                return jsonify({'status': 0, 'message': 'Acción no válida'})
        else:
            return jsonify({'status': 0, 'message': 'No se especificó ninguna acción'})
    else:
        return jsonify({'status': 0, 'message': 'Método HTTP no válido'})

def get_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

def get_groups():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupos")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

def get_actions():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM acciones")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

def get_groups_with_actions_and_users():
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT g.id AS grupo_id,
           g.nombre AS nombre_grupo,
           a.id AS accion_id,
           a.nombre AS nombre_accion,
           u.id AS usuario_id,
           u.nombre AS nombre_usuario
    FROM grupo_acciones ga
    JOIN grupos g ON ga.grupo_id = g.id
    JOIN acciones a ON ga.accion_id = a.id
    JOIN usuarios u ON g.id = u.grupo_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    response = {}
    for row in rows:
        grupo_id = row['grupo_id']
        if grupo_id not in response:
            response[grupo_id] = {
                'nombre_grupo': row['nombre_grupo'],
                'acciones': [],
                'usuarios': []
            }
        if row['accion_id']:
            response[grupo_id]['acciones'].append({
                'id': row['accion_id'],
                'nombre': row['nombre_accion']
            })
        if row['usuario_id']:
            response[grupo_id]['usuarios'].append({
                'id': row['usuario_id'],
                'nombre': row['nombre_usuario']
            })
    cursor.close()
    return jsonify(list(response.values()))

def create_user():
    cursor = db.cursor()
    data = request.get_json()
    nombre = data['nombre']
    grupo_id = data['grupo_id']
    query = "INSERT INTO usuarios (nombre, grupo_id) VALUES (%s, %s)"
    cursor.execute(query, (nombre, grupo_id))
    db.commit()
    response = {'status': 1, 'status_message': 'User created successfully.'} if cursor.rowcount == 1 else {'status': 0, 'status_message': 'User creation failed.'}
    cursor.close()
    return jsonify(response)

def create_group():
    cursor = db.cursor()
    data = request.get_json()
    nombre = data['nombre']
    query = "INSERT INTO grupos (nombre) VALUES (%s)"
    cursor.execute(query, (nombre,))
    db.commit()
    response = {'status': 1, 'status_message': 'Group created successfully.'} if cursor.rowcount == 1 else {'status': 0, 'status_message': 'Group creation failed.'}
    cursor.close()
    return jsonify(response)

def create_action():
    cursor = db.cursor()
    data = request.get_json()
    nombre = data['nombre']
    query = "INSERT INTO acciones (nombre) VALUES (%s)"
    cursor.execute(query, (nombre,))
    db.commit()
    response = {'status': 1, 'status_message': 'Action created successfully.'} if cursor.rowcount == 1 else {'status': 0, 'status_message': 'Action creation failed.'}
    cursor.close()
    return jsonify(response)

def assign_action_to_group():
    cursor = db.cursor()
    data = request.get_json()
    grupo_id = data['grupo_id']
    accion_id = data['accion_id']
    query = "INSERT INTO grupo_acciones (grupo_id, accion_id) VALUES (%s, %s)"
    cursor.execute(query, (grupo_id, accion_id))
    db.commit()
    response = {'status': 1, 'status_message': 'Action assigned to group successfully.'} if cursor.rowcount == 1 else {'status': 0, 'status_message': 'Action assignment failed.'}
    cursor.close()
    return jsonify(response)

def get_user(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    row = cursor.fetchone()
    cursor.close()
    return jsonify(row if row else {})

def get_group_action():
    grupo_id = request.args.get('grupo_id')
    if not grupo_id:
        return jsonify({'status': 0, 'message': 'No se especificó grupo_id'})

    cursor = db.cursor(dictionary=True)
    query = """
    SELECT a.id AS accion_id, a.nombre AS nombre_accion
    FROM grupo_acciones ga
    JOIN acciones a ON ga.accion_id = a.id
    WHERE ga.grupo_id = %s
    """
    cursor.execute(query, (grupo_id,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
