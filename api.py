from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "maritime"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)


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

if __name__ == "__main__":
    app.run(debug=True)
