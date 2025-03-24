from flask import Flask, request, jsonify
from flask_cors import CORS
from optimization.solver import solve_problem

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/optimize', methods=['POST'])
def optimize():
    data = None
    try:
        data = request.get_json()
        print("Dados recebidos no app.py:", data)
        result = solve_problem(data)
        return jsonify(result)
    except Exception as e:
        print("Erro no app.py:", str(e))
        from utils.error_handler import handle_error
        return handle_error(e, data)

if __name__ == '__main__':
    app.run(debug=True)