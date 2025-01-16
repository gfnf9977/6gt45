from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)  # Дозволяє крос-доменні запити

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=legion;'
                          'Database=people;'
                          'Trusted_Connection=yes;')
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        users_list = [{'id': user[0], 'username': user[1]} for user in users]
        return jsonify(users_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", user_id)
        conn.commit()
        return jsonify({'message': 'Користувача видалено успішно'})
    except pyodbc.Error as e:
        if 'REFERENCE' in str(e):
            return jsonify({'error': 'Неможливо видалити користувача, оскільки існують пов\'язані записи'}), 409
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при видаленні користувача'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
