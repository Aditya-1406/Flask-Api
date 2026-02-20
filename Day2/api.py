from flask import Flask,request,jsonify
from helper import * 

app = Flask(__name__)
db = Helper()

@app.route("/")
def home():
    return jsonify({"message" : "Hello World"})

@app.route("/notes",methods=["GET", "POST"])
def notes(): 
    if request.method == "POST":
        data  = request.get_json()

        title = data.get("title")
        description = data.get("description")

        note_id = db.post_notes(title,description)

        return jsonify({"message" : "note created successfully","id": note_id })

    data = db.get_notes()
    return jsonify(data)

@app.route("/notes/<int:id>")
def get_note_id(id):
    data = db.get_note(id)
    if not data:
        return jsonify({"error" : "data not found"})
    
    return jsonify(data)

@app.route("/notes/<int:id>",methods=["PUT"])
def put_note_id(id):
    data = request.get_json()
    note = db.get_note(id)

    title = data.get("title",note["title"])
    description = data.get("description", note["description"])
    if not data:
        return jsonify({"error" : "data not found"})
    
    db.update_note(id,title,description)
    
    return jsonify({"message" : "note updated successfully"})

@app.route("/notes/<int:id>",methods=["DELETE"])
def delete_note(id):
    db.delete_note(id)
    return jsonify({"message" : "note Deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)