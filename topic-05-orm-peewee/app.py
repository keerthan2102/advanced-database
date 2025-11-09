# app.py  (topic-05-orm-peewee)
from flask import Flask, render_template, request, redirect, url_for
from database import initialize, Kind, Pet

app = Flask(__name__)

# Use the Peewee DB for this topic
initialize("pets.db")   # safe to call multiple times 

@app.get("/")
def home():
    return redirect(url_for("pet_list"))

# ----- PETS -----

@app.get("/list")
def pet_list():
    # Peewee JOIN: load pets with their kind
    pets = Pet.select().join(Kind)
    return render_template("list.html", pets=pets)

@app.get("/create")
def pet_create_form():
    kinds = Kind.select().order_by(Kind.id)
    return render_template("create.html", kinds=kinds)

@app.post("/create")
def pet_create():
    name = request.form["name"]
    age = request.form.get("age") or None
    owner = request.form.get("owner") or None
    kind_id = int(request.form["kind_id"])
    kind = Kind.get_by_id(kind_id)
    Pet.create(name=name, age=age, owner=owner, kind=kind)
    return redirect(url_for("pet_list"))

@app.get("/update/<int:id>")
def pet_update_form(id):
    pet = Pet.get_or_none(Pet.id == id)
    kinds = Kind.select().order_by(Kind.id)
    return render_template("update.html", pet=pet, kinds=kinds)

@app.post("/update/<int:id>")
def pet_update(id):
    pet = Pet.get_by_id(id)
    pet.name = request.form["name"]
    pet.age = request.form.get("age") or None
    pet.owner = request.form.get("owner") or None
    pet.kind = Kind.get_by_id(int(request.form["kind_id"]))
    pet.save()
    return redirect(url_for("pet_list"))

@app.get("/delete/<int:id>")
def pet_delete(id):
    Pet.get_by_id(id).delete_instance()
    return redirect(url_for("pet_list"))

# ----- KINDS -----

@app.get("/kind/list")
def kind_list():
    kinds = Kind.select().order_by(Kind.id)
    return render_template("kind_list.html", kinds=kinds)

@app.get("/kind/create")
def kind_create_form():
    return render_template("kind_create.html")

@app.post("/kind/create")
def kind_create():
    Kind.create(
        kind_name=request.form["name"],
        food=request.form.get("food") or None,
        noise=request.form.get("sound") or None,
    )
    return redirect(url_for("kind_list"))

@app.get("/kind/update/<int:id>")
def kind_update_form(id):
    kind = Kind.get_by_id(id)
    return render_template("kind_update.html", kind=kind)

@app.post("/kind/update/<int:id>")
def kind_update(id):
    kind = Kind.get_by_id(id)
    kind.kind_name = request.form["name"]
    kind.food = request.form.get("food") or None
    kind.noise = request.form.get("sound") or None
    kind.save()
    return redirect(url_for("kind_list"))

@app.get("/kind/delete/<int:id>")
def kind_delete(id):
    # Will raise if pets still reference this kind (RESTRICT)
    Kind.get_by_id(id).delete_instance()
    return redirect(url_for("kind_list"))

if __name__ == "__main__":
    app.run(debug=True)
