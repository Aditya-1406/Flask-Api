from flask import Flask,jsonify,request
from datetime import datetime

app = Flask(__name__)

notes = [
    {
        "id" : 1,
        "title" : "Python flask",
        "description" : "Learning to create api using Flask",
        "created_at" : datetime.now(),
    },
    {
        "id" : 2,
        "title" : "Python Django",
        "description" : "Learned to create app using django",
        "created_at" : datetime.now(),
    },
]

@app.route("/")
def hello():
    return "Hello World"

@app.route("/notes",methods=["GET","POST"])
def add_note():
    if request.method == "POST":
        data = request.json
        if notes:
            new_id = notes[-1]["id"] + 1
        else:
            new_id = 1

        data["id"] = new_id
        data["created_at"] = datetime.now()
        notes.append(data)
        return jsonify({"message": "Note Added", "data": data})


    return jsonify(notes)

@app.route("/note/<int:id>",methods=["GET"])
def get_note_by_id(id):
    data = next((d for d in notes if d["id"] == id),None)
    return jsonify(data)
    
@app.route("/note/<int:id>",methods=["PUT"])
def put_note_by_id(id):
    data = next((d for d in notes if d["id"] == id),None)
    if data is None:
        return jsonify({"error" : "record not found"})
    update = request.json
    if not update:
        return jsonify({"error" : "Nothing to update"})
    
    if "title" in update:
        data["title"] = update["title"]
    if "description" in update:
        data["description"] = update["description"]
    return jsonify(data)


@app.route("/note/<int:id>", methods=["DELETE"])
def delete_note(id):
    data = next(d for d in notes if d["id"] == id)
    if data:
        notes.remove(data)
        return jsonify(data)
    else:
        return jsonify({"error" : "Data not found"})

if __name__ == "__main__":
    app.run(debug=True)