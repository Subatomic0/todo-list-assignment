from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from db import validate_key, get_tasks, create_task, create_category, attach_category, get_categories, delete_category, \
    delete_task, update_tasks


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

load_dotenv()

@app.route("/")
def index():
    return {"message": "Hello"}


@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    if request.method == 'GET':
        if user:
            temp_ = get_tasks(user['id'])
            return jsonify(temp_)
        else:
            return jsonify({'error': 'error'})
    if request.method == 'POST':
        req = request.get_json()
        if user and req:
            return create_task(user['id'], req.get('category_id'), req.get('title'), req.get('done'), req.get('due'))
        else:
            return jsonify({'error': 'error'})


@app.put("/tasks/update-task<int:task_id>")
def update_task(task_id):
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    req = request.get_json()
    if user and req:
        return update_tasks(req.get('title'), req.get('done'), req.get('due'), task_id, user['id'])
    else:
        return jsonify({'error': 'error'})


@app.put("/tasks/update-task-category")
def update_task_category():
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    req = request.get_json()
    if user and req:
        return attach_category(req.get('category_id'), req.get('task_id'), user['id'])
    else:
        return jsonify({'error': 'invalid token / no user found'})


@app.delete("/tasks/remove-task<int:task_id>")
def remove_task(task_id):
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    if user:
        return delete_task(user['id'], task_id)
    else:
        return jsonify({'error': 'error'})


@app.delete("/tasks/categories<int:cate_id>")
def categories(cate_id):
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    if user:
        return delete_category(cate_id)
    else:
        return jsonify({'error': 'error'})


@app.route("/tasks/categories", methods=['GET', 'POST'])
def create_new_cat():
    api_key = request.headers.get('Authorization')
    user = validate_key(api_key)
    if user:
        if request.method == 'GET':
            temp = get_categories()
            return jsonify(temp)
        elif request.method == 'POST':
            req = request.get_json()
            return create_category(req.get('category_name'))
    else:
        return jsonify({'error': 'error'})


if __name__ == '__main__':
    app.run(debug=True
            #     host='0.0.0.0', port=PORT, debug=True, ssl_context=(
            #     '/etc/letsencrypt/fullchain.pem',
            #     '/etc/letsencrypt/privkey.pem'
            # )
            )
