# app.py  — Topic 05 (Peewee) wired to Topic 04-style templates
from flask import Flask, render_template, request, redirect, url_for
from database import initialize, Kind, Pet

app = Flask(__name__)

# Initialize Peewee / SQLite 
initialize("pets.db")

# -------------------------
# Helpers: model -> dict(s)
# -------------------------
def kind_to_dict(k: Kind):
    return {"id": k.id, "name": k.kind_name, "food": k.food, "sound": k.noise}

def pet_to_dict(p: Pet):
    return {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "owner": p.owner,
        "kind_name": p.kind.kind_name if p.kind else None,
        "food": p.kind.food if p.kind else None,
        "sound": p.kind.noise if p.kind else None,
        "kind_id": p.kind.id if p.kind else None,
    }

# -------------------------
# Home
# -------------------------
@app.get("/")
def home():
    return redirect(url_for("pet_list"))

# -------------------------
# PETS (child)
# -------------------------
@app.get("/list")
def pet_list():
    pets_qs = Pet.select().join(Kind)
    pets = [pet_to_dict(p) for p in pets_qs]
    return render_template("list.html", pets=pets)

@app.get("/create")
def pet_create_form():
    kinds = [kind_to_dict(k) for k in Kind.select().order_by(Kind.id)]
    return render_template("create.html", kinds=kinds)

@app.post("/create")
def pet_create():
    name = request.form["name"]
    age = request.form.get("age") or None
    owner = request.form.get("owner") or None
    kind_id = int(request.form["kind_id"])
    Pet.create(name=name, age=age, owner=owner, kind=Kind.get_by_id(kind_id))
    return redirect(url_for("pet_list"))

@app.get("/update/<int:id>")
def pet_update_form(id: int):
    p = Pet.get_or_none(Pet.id == id)
    if not p:
        return redirect(url_for("pet_list"))
    pet = pet_to_dict(p)
    kinds = [kind_to_dict(k) for k in Kind.select().order_by(Kind.id)]
    return render_template("update.html", pet=pet, kinds=kinds)

@app.post("/update/<int:id>")
def pet_update(id: int):
    p = Pet.get_by_id(id)
    p.name = request.form["name"]
    p.age = request.form.get("age") or None
    p.owner = request.form.get("owner") or None
    p.kind = Kind.get_by_id(int(request.form["kind_id"]))
    p.save()
    return redirect(url_for("pet_list"))

@app.get("/delete/<int:id>")
def pet_delete(id: int):
    Pet.get_by_id(id).delete_instance()
    return redirect(url_for("pet_list"))

# -------------------------
# KINDS (parent / reference)
# -------------------------
@app.get("/kind")
def kind_index():
    # nice alias so /kind works
    return redirect(url_for("kind_list"))

@app.get("/kind/list")
def kind_list():
    kinds = [kind_to_dict(k) for k in Kind.select().order_by(Kind.id)]
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
def kind_update_form(id: int):
    k = Kind.get_or_none(Kind.id == id)
    if not k:
        return redirect(url_for("kind_list"))
    return render_template("kind_update.html", kind=kind_to_dict(k))

@app.post("/kind/update/<int:id>")
def kind_update(id: int):
    k = Kind.get_by_id(id)
    k.kind_name = request.form["name"]
    k.food = request.form.get("food") or None
    k.noise = request.form.get("sound") or None
    k.save()
    return redirect(url_for("kind_list"))

@app.get("/kind/delete/<int:id>")
def kind_delete(id: int):
    # Will raise if pets reference this kind (RESTRICT)
    Kind.get_by_id(id).delete_instance()
    return redirect(url_for("kind_list"))

# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
