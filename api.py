from flask import Flask, make_response, jsonify, request,  render_template, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "maritime"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = "mysecret1233123"

mysql = MySQL(app)

users = {'user1': 'password1', 'user2': 'password2'}

@app.route("/")
def home():
    return render_template("base.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('search_addresses'))  

    return render_template("login.html")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/addresses", methods=["GET"])
def get_addresses():
    data = data_fetch("""select * from maritime.addresses""")
    return make_response(jsonify(data), 200)


@app.route("/addresses/search/<int:id>", methods=["GET"])
def get_addresses_by_id(id):
    data = data_fetch("""SELECT * FROM maritime.addresses where Address_ID = %s""", (id,))
    return make_response(jsonify(data), 200)


@app.route("/clients/<int:id>/addresses", methods=["GET"])
def get_addresses_by_clients(id):
    data = data_fetch(
        """
        SELECT addresses.City, addresses.Country 
        FROM addresses 
        INNER JOIN clients
        ON addresses.Address_ID = clients.Client_ID 
        INNER JOIN ref_client_categories
        ON clients.Client_ID  = ref_client_categories.Client_Category_Code 
        WHERE addresses.Address_ID = {}
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"Address_ID": id, "count": len(data), "addresses": data}), 200
    )


@app.route("/addresses", methods=["POST"])
def add_addresses():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Line_1 = info["Line_1"]
    Line_2 = info["Line_2"]
    City = info["City"]
    Zip_Postcode = info["Zip_Postcode"]
    State_Country_Region = info["State_Country_Region"]
    Country = info["Country"]
    other_Details = info["other_Details"]

    cur.execute(
        """
        INSERT INTO addresses (Line_1, Line_2, City, Zip_Postcode, State_Country_Region, Country, other_Details)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (Line_1, Line_2, City, Zip_Postcode, State_Country_Region, Country, other_Details),
    )

    mysql.connection.commit()
    print("row(s) affected: {}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()

    return make_response(
        jsonify({"message": "addresses added successfully", "rows_affected": rows_affected}),
        201,
    )


@app.route("/addresses/<int:id>", methods=["PUT"])
def update_addresses(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Line_1 = info["Line_1"]
    Line_2 = info["Line_2"]
    City = info["City"]
    Zip_Postcode = info["Zip_Postcode"]
    State_Country_Region = info["State_Country_Region"]
    Country = info["Country"]
    other_Details = info["other_Details"]
    cur.execute(
        """ UPDATE addresses  SET Line_1 = %s, Line_2 = %s,  City = %s, Zip_Postcode = %s,  State_Country_Region = %s,Country = %s,other_Details = %s WHERE Address_ID = %s """,
       (Line_1, Line_2, City, Zip_Postcode, State_Country_Region, Country, other_Details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "addresses updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/addresses/<int:id>", methods=["DELETE"])
def delete_addresses(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM addresses where Address_ID = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "addresses deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/addresses/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)


if __name__ == "__main__":
    app.run(debug=True)
