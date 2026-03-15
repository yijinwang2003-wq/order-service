from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/orders')
def get_orders():
    return jsonify([{"id": 1, "item": "Laptop", "status": "Pending"}]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)