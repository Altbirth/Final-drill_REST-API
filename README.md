How to run the CRUD REST API:
Step 1: Download the zip file.
Step 2: Extract the file's.
Step 3: After extracting the file right click on the folder and click Open terminal. Input this code "code -n ." to open it in visual studio code or use what platform you are comfortable with.
Step 4: run the api.py file using f5 or using the run button on the top right corner of visual studio code. Or  python api.py or api.py
Step 5: enjoy

You will see a CRUD - JSON type
Create, Read, Update, and Delete

The security:
Username: User1 or User2.
Password: Password1 or Password2

Below are the https you can use.
HTPPS:
http://127.0.0.1:5000/addresses
http://127.0.0.1:5000/addresses/search/<int:id>
http://127.0.0.1:5000/clients/<int:id>/addresses
http://127.0.0.1:5000/addresses["POST"] - this for insert
http://127.0.0.1:5000/addresses/<int:id> ["PUT"] - this is for update
http://127.0.0.1:5000/addresses/<int:id> ["DELETE"] - this is for delete
