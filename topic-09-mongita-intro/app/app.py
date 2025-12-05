from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongitaClientDisk()          
db = client["petsdb"]
pets = db["pets"]

def as_view(doc):
    return {
        "_id": str(doc.get("_id")),
        "name": doc.get("name", ""),
        "age": doc.get("age", ""),
        "owner": doc.get("owner", ""),
        "color": doc.get("color", ""),  # <-- new field
    }

@app.get("/")
def home():
    return redirect(url_for("pet_list"))

@app.get("/list")
def pet_list():
    items = [as_view(p) for p in pets.find({}).sort("name", 1)]
    return render_template("list.html", pets=items)

@app.get("/create")
def create_form():
    return render_template("create.html")

@app.post("/create")
def create():
    doc = {
        "name":  request.form.get("name","").strip(),
        "age":   request.form.get("age","").strip(),
        "owner": request.form.get("owner","").strip(),
        "color": request.form.get("color","").strip(),  # <-- new
    }
    pets.insert_one(doc)
    return redirect(url_for("pet_list"))

@app.get("/update/<id>")
def update_form(id):
    p = pets.find_one({"_id": ObjectId(id)})
    if not p:
        return redirect(url_for("pet_list"))
    return render_template("update.html", pet=as_view(p))

@app.post("/update/<id>")
def update(id):
    pets.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "name":  request.form.get("name","").strip(),
            "age":   request.form.get("age","").strip(),
            "owner": request.form.get("owner","").strip(),
            "color": request.form.get("color","").strip(),  # <-- new
        }}
    )
    return redirect(url_for("pet_list"))

@app.get("/delete/<id>")
def delete(id):
    pets.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("pet_list"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
