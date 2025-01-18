import re
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Database connection
def get_db_connection():
    return pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db='mydb')

def is_valid_uk_postcode(postcode):
    pattern = r"^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][ABD-HJLNP-UW-Z]{2}$"  # UK postcode regex
    match = re.match(pattern, postcode.upper())
    return bool(match)

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Email regex
    match = re.match(pattern, email)
    return bool(match)

def create_email_message(user_data):
    try:
        return f"""Subject: DevOps - Release Pipeline Requirement

Dear {user_data['name']},

Thank you for logging your development requirements. We will provision the servers and create the automated pipelines for your nightly builds and release pipelines.

Age: {user_data['age']}
Name: {user_data['name']}
Address: {user_data['address']}
Postcode: {user_data['postcode']}
Email: {user_data['email']}

Sincerely,

DevOps Team
"""
    except KeyError as e:
        return f"Error creating email: Missing key {e} in user details."

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            name = request.form["name"]
            address = request.form["address"]
            postcode = request.form["postcode"]
            email = request.form["email"]

            # Validation checks
            if age < 0:
                raise ValueError("Age cannot be negative.")
            if not name.strip():
                raise ValueError("Name cannot be empty.")
            if not address.strip():
                raise ValueError("Address cannot be empty.")
            if not is_valid_uk_postcode(postcode):
                raise ValueError("Invalid UK postcode.")
            if not is_valid_email(email):
                raise ValueError("Invalid email address.")

            user_data = {
                "age": age,
                "name": name,
                "address": address,
                "postcode": postcode,
                "email": email
            }

            # Insert user data into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_statement = """
            INSERT INTO registration (name, age, address, postcode, email)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_statement, (name, age, address, postcode, email))
            conn.commit()  # Commit the transaction

            cursor.close()
            conn.close()

            message = create_email_message(user_data)
            return render_template("email.html", message=message)
        except ValueError as e:
            error = str(e)
        except KeyError as e:
            error = f"Error: Missing field {e}"
        except Exception as e:  # This is the line you asked about
            error = f"An unexpected error occurred: {str(e)}"  # Enhanced error visibility

    return render_template("form.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)