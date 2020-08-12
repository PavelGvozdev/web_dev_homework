import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import todoitem

app = bottle.Bottle()

@enable_cors
@app.route("/api/tasks/", method=["GET", "POST"])
def add_task():
    if bottle.request.method == 'GET':
        tasks = [task.to_dict() for task in todoitem.tasks_db.values()]
        return {"tasks": tasks}
    elif bottle.request.method == "POST":
        desc = bottle.request.json['description']
        is_completed = bottle.request.json.get('is_completed', False)
        if len(desc) > 0:
            new_uid = max(todoitem.tasks_db.keys()) + 1
            t = todoitem.TodoItem(desc, new_uid)
            t.is_completed = is_completed
            todoitem.tasks_db[new_uid] = t
        return "OK"

@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET", "PUT", "DELETE"])
def show_or_modify_task(uid):
    if bottle.request.method == "GET":
        return todoitem.tasks_db[uid].to_dict()
    elif bottle.request.method == "PUT":
        if "description" in bottle.request.json:
            todoitem.tasks_db[uid].description = bottle.request.json['description']
        if "is_completed" in bottle.request.json:
            todoitem.tasks_db[uid].is_completed = bottle.request.json['is_completed']
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        todoitem.tasks_db.pop(uid)
        return f"Deleted task {uid}"

app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)
