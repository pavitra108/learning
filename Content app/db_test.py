from flask import Flask, render_template, request
import psycopg2

# Replace these values with your PostgreSQL connection details
dbname = "db-name"
user = "postgres"
password = "psw"
host = "host"
port = 5431

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)


def make_table():
    hello = "<table>no data</table>"
    final_data = ""

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    cursor.execute("SELECT age, name FROM pro_schema.user;")
    rows = cursor.fetchall()
    for each_row in rows:
        for one_item in each_row:
            final_data += f"<tr><td> {one_item[1]} </td><td> {one_item[0]} </td></tr>"
    output = hello.replace('no data', final_data)
    print (output)
    return render_template(output)


    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
