from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------

def get_db():
    conn = sqlite3.connect("realestate.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- CREATE TABLES ----------

def init_db():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS owners(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS agents(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS locations(id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS properties(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, owner_id INTEGER, location_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS tenants(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS rentals(id INTEGER PRIMARY KEY AUTOINCREMENT, property_id INTEGER, tenant_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS payments(id INTEGER PRIMARY KEY AUTOINCREMENT, rental_id INTEGER, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS maintenance(id INTEGER PRIMARY KEY AUTOINCREMENT, property_id INTEGER, description TEXT)")



    conn.commit()
    conn.close()


init_db()

# ---------- HOME ----------

@app.route("/")
def home():
    return render_template("home.html")


# ---------- OWNERS ----------

@app.route("/owners", methods=["GET","POST"])
def owners():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        cur.execute("INSERT INTO owners(name) VALUES(?)",(name,))
        conn.commit()

    cur.execute("SELECT * FROM owners")
    owners = cur.fetchall()

    conn.close()

    return render_template("owners.html", owners=owners)


@app.route("/delete_owner/<int:id>")
def delete_owner(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM owners WHERE id=?",(id,))
    conn.commit()

    conn.close()

    return redirect("/owners")


@app.route("/edit_owner/<int:id>", methods=["GET","POST"])
def edit_owner(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cur.execute(
            "UPDATE owners SET name=? WHERE id=?",
            (name,id)
        )

        conn.commit()
        conn.close()

        return redirect("/owners")

    cur.execute("SELECT * FROM owners WHERE id=?", (id,))
    owner = cur.fetchone()

    conn.close()

    return render_template("edit_owner.html", owner=owner)

# ---------- AGENTS ----------

@app.route("/agents", methods=["GET","POST"])
def agents():

    conn = get_db()
    cur = conn.cursor()

    # ADD AGENT
    if request.method == "POST":
        name = request.form["name"]

        cur.execute(
            "INSERT INTO agents(name) VALUES(?)",
            (name,)
        )

        conn.commit()

    # SHOW AGENTS
    cur.execute("SELECT * FROM agents")
    agents = cur.fetchall()

    conn.close()

    return render_template("agents.html", agents=agents)


# ---------- EDIT AGENT ----------

@app.route("/edit_agent/<int:id>", methods=["GET","POST"])
def edit_agent(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cur.execute(
            "UPDATE agents SET name=? WHERE id=?",
            (name, id)
        )

        conn.commit()
        conn.close()

        return redirect("/agents")

    cur.execute("SELECT * FROM agents WHERE id=?", (id,))
    agent = cur.fetchone()

    conn.close()

    return render_template("edit_agent.html", agent=agent)


# ---------- DELETE AGENT ----------

@app.route("/delete_agent/<int:id>")
def delete_agent(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM agents WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/agents")

# ---------- LOCATIONS ----------

@app.route("/locations", methods=["GET","POST"])
def locations():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        city = request.form["city"]
        cur.execute("INSERT INTO locations(city) VALUES(?)",(city,))
        conn.commit()

    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()

    conn.close()

    return render_template("locations.html", locations=locations)


@app.route("/delete_location/<int:id>")
def delete_location(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM locations WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/locations")


@app.route("/edit_location/<int:id>", methods=["GET","POST"])
def edit_location(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        city = request.form["city"]

        cur.execute(
            "UPDATE locations SET city=? WHERE id=?",
            (city, id)
        )

        conn.commit()
        conn.close()

        return redirect("/locations")

    cur.execute("SELECT * FROM locations WHERE id=?", (id,))
    location = cur.fetchone()

    conn.close()

    return render_template("edit_location.html", location=location)

# ---------- PROPERTIES ----------

@app.route("/properties", methods=["GET","POST"])
def properties():

    conn = get_db()
    cur = conn.cursor()

    # ADD PROPERTY
    if request.method == "POST":

        name = request.form["name"]
        owner_id = request.form["owner_id"]
        location_id = request.form["location_id"]

        cur.execute(
            "INSERT INTO properties(name, owner_id, location_id) VALUES(?,?,?)",
            (name, owner_id, location_id)
        )

        conn.commit()

    # SHOW PROPERTIES
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()

    # OWNERS DROPDOWN
    cur.execute("SELECT * FROM owners")
    owners = cur.fetchall()

    # LOCATIONS DROPDOWN
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()

    conn.close()

    return render_template(
        "properties.html",
        properties=properties,
        owners=owners,
        locations=locations
    )


# ---------- EDIT PROPERTY ----------

@app.route("/edit_property/<int:id>", methods=["GET","POST"])
def edit_property(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        owner_id = request.form["owner_id"]
        location_id = request.form["location_id"]

        cur.execute(
            "UPDATE properties SET name=?, owner_id=?, location_id=? WHERE id=?",
            (name, owner_id, location_id, id)
        )

        conn.commit()
        conn.close()

        return redirect("/properties")

    # GET PROPERTY
    cur.execute("SELECT * FROM properties WHERE id=?", (id,))
    property = cur.fetchone()

    # GET OWNERS
    cur.execute("SELECT * FROM owners")
    owners = cur.fetchall()

    # GET LOCATIONS
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()

    conn.close()

    return render_template(
        "edit_property.html",
        property=property,
        owners=owners,
        locations=locations
    )


# ---------- DELETE PROPERTY ----------

@app.route("/delete_property/<int:id>")
def delete_property(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM properties WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/properties")

# ---------- TENANTS ----------

@app.route("/tenants", methods=["GET","POST"])
def tenants():

    conn = get_db()
    cur = conn.cursor()

    # ADD TENANT
    if request.method == "POST":
        name = request.form["name"]

        cur.execute(
            "INSERT INTO tenants(name) VALUES(?)",
            (name,)
        )

        conn.commit()

    # SHOW TENANTS
    cur.execute("SELECT * FROM tenants")
    tenants = cur.fetchall()

    conn.close()

    return render_template("tenants.html", tenants=tenants)


# ---------- EDIT TENANT ----------

@app.route("/edit_tenant/<int:id>", methods=["GET","POST"])
def edit_tenant(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]

        cur.execute(
            "UPDATE tenants SET name=? WHERE id=?",
            (name, id)
        )

        conn.commit()
        conn.close()

        return redirect("/tenants")

    # Get tenant data
    cur.execute("SELECT * FROM tenants WHERE id=?", (id,))
    tenant = cur.fetchone()

    conn.close()

    return render_template("edit_tenant.html", tenant=tenant)


# ---------- DELETE TENANT ----------

@app.route("/delete_tenant/<int:id>")
def delete_tenant(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tenants WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/tenants")

# ---------- RENTALS ----------

@app.route("/rentals", methods=["GET","POST"])
def rentals():

    conn = get_db()
    cur = conn.cursor()

    # ADD RENTAL
    if request.method == "POST":

        property_id = request.form["property_id"]
        tenant_id = request.form["tenant_id"]

        cur.execute(
            "INSERT INTO rentals(property_id, tenant_id) VALUES(?,?)",
            (property_id, tenant_id)
        )

        conn.commit()

    # SHOW RENTALS
    cur.execute("SELECT * FROM rentals")
    rentals = cur.fetchall()

    # GET PROPERTIES FOR DROPDOWN
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()

    # GET TENANTS FOR DROPDOWN
    cur.execute("SELECT * FROM tenants")
    tenants = cur.fetchall()

    conn.close()

    return render_template(
        "rentals.html",
        rentals=rentals,
        properties=properties,
        tenants=tenants
    )


# ---------- EDIT RENTAL ----------

@app.route("/edit_rental/<int:id>", methods=["GET","POST"])
def edit_rental(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        property_id = request.form["property_id"]
        tenant_id = request.form["tenant_id"]

        cur.execute(
            "UPDATE rentals SET property_id=?, tenant_id=? WHERE id=?",
            (property_id, tenant_id, id)
        )

        conn.commit()
        conn.close()

        return redirect("/rentals")

    # GET RENTAL
    cur.execute("SELECT * FROM rentals WHERE id=?", (id,))
    rental = cur.fetchone()

    # GET PROPERTIES
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()

    # GET TENANTS
    cur.execute("SELECT * FROM tenants")
    tenants = cur.fetchall()

    conn.close()

    return render_template(
        "edit_rental.html",
        rental=rental,
        properties=properties,
        tenants=tenants
    )


# ---------- DELETE RENTAL ----------

@app.route("/delete_rental/<int:id>")
def delete_rental(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM rentals WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/rentals")
# ---------- PAYMENTS ----------
# ---------- PAYMENTS ----------

@app.route("/payments", methods=["GET","POST"])
def payments():

    conn = get_db()
    cur = conn.cursor()

    # ADD PAYMENT
    if request.method == "POST":

        rental_id = request.form["rental_id"]
        amount = request.form["amount"]

        cur.execute(
            "INSERT INTO payments(rental_id, amount) VALUES(?,?)",
            (rental_id, amount)
        )

        conn.commit()

    # GET PAYMENTS
    cur.execute("SELECT * FROM payments")
    payments = cur.fetchall()

    # GET RENTALS FOR DROPDOWN
    cur.execute("SELECT * FROM rentals")
    rentals = cur.fetchall()

    conn.close()

    return render_template(
        "payments.html",
        payments=payments,
        rentals=rentals
    )


# ---------- EDIT PAYMENT ----------

@app.route("/edit_payment/<int:id>", methods=["GET","POST"])
def edit_payment(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        rental_id = request.form["rental_id"]
        amount = request.form["amount"]

        cur.execute(
            "UPDATE payments SET rental_id=?, amount=? WHERE id=?",
            (rental_id, amount, id)
        )

        conn.commit()
        conn.close()

        return redirect("/payments")

    # GET PAYMENT
    cur.execute("SELECT * FROM payments WHERE id=?", (id,))
    payment = cur.fetchone()

    # GET RENTALS
    cur.execute("SELECT * FROM rentals")
    rentals = cur.fetchall()

    conn.close()

    return render_template(
        "edit_payment.html",
        payment=payment,
        rentals=rentals
    )


# ---------- DELETE PAYMENT ----------

@app.route("/delete_payment/<int:id>")
def delete_payment(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM payments WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/payments")
# ---------- MAINTENANCE ----------

@app.route("/maintenance", methods=["GET","POST"])
def maintenance():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        property_id = request.form["property_id"]
        description = request.form["description"]

        cur.execute(
            "INSERT INTO maintenance(property_id, description) VALUES(?,?)",
            (property_id, description)
        )

        conn.commit()

    # show maintenance records
    cur.execute("SELECT * FROM maintenance")
    maintenance = cur.fetchall()

    # properties for dropdown
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()

    conn.close()

    return render_template(
        "maintenance.html",
        maintenance=maintenance,
        properties=properties
    )


# ---------- EDIT MAINTENANCE ----------

@app.route("/edit_maintenance/<int:id>", methods=["GET","POST"])
def edit_maintenance(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        property_id = request.form["property_id"]
        description = request.form["description"]

        cur.execute(
            "UPDATE maintenance SET property_id=?, description=? WHERE id=?",
            (property_id, description, id)
        )

        conn.commit()
        conn.close()

        return redirect("/maintenance")

    # get selected record
    cur.execute("SELECT * FROM maintenance WHERE id=?", (id,))
    record = cur.fetchone()

    # get properties
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()

    conn.close()

    return render_template(
        "edit_maintenance.html",
        record=record,
        properties=properties
    )


# ---------- DELETE MAINTENANCE ----------

@app.route("/delete_maintenance/<int:id>")
def delete_maintenance(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM maintenance WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/maintenance")

# ---------- QUERIES ----------

@app.route("/queries")
def queries():
    return render_template("queries.html")


# Query 1 - Properties with Owners
@app.route("/query1")
def query1():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT properties.name, owners.name
    FROM properties
    JOIN owners ON properties.owner_id = owners.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Properties with Owners")


# Query 2 - Properties with Locations
@app.route("/query2")
def query2():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT properties.name, locations.city
    FROM properties
    JOIN locations ON properties.location_id = locations.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Properties with Locations")


# Query 3 - Rentals with Tenants
@app.route("/query3")
def query3():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT rentals.id, tenants.name
    FROM rentals
    JOIN tenants ON rentals.tenant_id = tenants.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Rentals with Tenants")


# Query 4 - Total Payments
@app.route("/query4")
def query4():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM payments")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Payments")


# Query 5 - Maintenance Records
@app.route("/query5")
def query5():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT property_id, description FROM maintenance")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Maintenance Records")


# Query 6 - Properties per Owner
@app.route("/query6")
def query6():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT owners.name, COUNT(properties.id)
    FROM owners
    LEFT JOIN properties ON owners.id = properties.owner_id
    GROUP BY owners.name
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Properties per Owner")


# Query 7 - Properties per Location
@app.route("/query7")
def query7():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT locations.city, COUNT(properties.id)
    FROM locations
    LEFT JOIN properties ON locations.id = properties.location_id
    GROUP BY locations.city
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Properties per Location")
#Query 8 -total tenants
@app.route("/query8")
def query8():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tenants")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Tenants")

#Query 9 - total agents
@app.route("/query9")
def query9():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM agents")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Agents")

#query 10 - all rentals
@app.route("/query10")
def query10():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM rentals")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="All Rentals")
#query 11- payments with rental
@app.route("/query11")
def query11():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT payments.id, rentals.id, payments.amount
    FROM payments
    JOIN rentals ON payments.rental_id = rentals.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Payments with Rentals")
#query 12- avg payment
@app.route("/query12")
def query12():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT AVG(amount) FROM payments")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Average Payment")

# query 13 - highest payment
@app.route("/query13")
def query13():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT MAX(amount) FROM payments")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Highest Payment")

#query 14 - lowest payment
@app.route("/query14")
def query14():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT MIN(amount) FROM payments")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Lowest Payment")

#query 15 -total properties
@app.route("/query15")
def query15():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM properties")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Properties")

#query 16 - properties without rentals
@app.route("/query16")
def query16():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT name FROM properties
    WHERE id NOT IN (SELECT property_id FROM rentals)
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Properties Without Rentals")

#query 17 -tenants with properties
@app.route("/query17")
def query17():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT tenants.name, properties.name
    FROM rentals
    JOIN tenants ON rentals.tenant_id = tenants.id
    JOIN properties ON rentals.property_id = properties.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Tenants with Properties")

#query 18- maintenace with property
@app.route("/query18")
def query18():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT maintenance.description, properties.name
    FROM maintenance
    JOIN properties ON maintenance.property_id = properties.id
    """)

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Maintenance with Property")

#query 19 - total maintenance
@app.route("/query19")
def query19():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM maintenance")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Maintenance Records")

#query 20 - total rentals
@app.route("/query20")
def query20():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM rentals")

    result = cur.fetchall()

    conn.close()

    return render_template("queries.html", result=result, title="Total Rentals")




# ---------- RUN APP ----------

if __name__ == "__main__":
    app.run(debug=True)