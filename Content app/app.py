
from flask import Flask, render_template, request, send_file
import psycopg2
import requests
import json
import boto3
import io
import os


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

# The application code
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/user', methods=['POST'])
def abc():
    """Process student details and insert them into the database.

        This function retrieves student details from the request, processes them,
        and inserts them into the database. It also calculates department, batch,
        and HOD name based on the course and batch information. Finally, it renders
        a template named 'courses.html'.

        Returns:
            flask.Response: A response containing the rendered 'courses.html' template.
        """
    global department, batch, hod_name

    # Retrieve student details from the request
    name = request.values.get('name')
    age = request.values.get('age')
    course_name = request.values.get('course_name')
    batch = request.values.get('batch')

    # Create a dictionary to store student details
    details = {"Name": name,
               "Age": age,
               "Course": course_name,
               "Batch": batch}

    # Generate course ID and student ID
    courseid = f"{course_name}{batch}"
    studentid = f"{course_name}{courseid}"

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Insert student details into the 'user' table and retrieve the autogenerated ID
    insert_query = "INSERT INTO pro_schema.user (name, age) VALUES (%s, %s) RETURNING id;"
    cursor.execute(insert_query, (details["Name"], details["Age"]))
    autogenerated_id = cursor.fetchone()[0]

    def dept(id):
        """# Define a function to determine department, batch, and HOD name based on the course ID."""
        if courseid in ('ME1', 'BE1'):
            d = 'Engineering'
            b = 'One'
            hod = 'Mrs. Olive'
        elif courseid in ('ME2', 'BE2'):
            d = 'Engineering'
            b = 'Two'
            hod = 'Mr. Thomas'
        elif courseid in ('MA1', 'BA1'):
            d = 'Arts'
            b = 'One'
            hod = 'Mrs. Edna'
        elif courseid in ('MA2', 'BA2'):
            d = 'Arts'
            b = 'Two'
            hod = 'Mrs. Irene'
        elif courseid == 'MBA1':
            d = 'Management'
            b = 'One'
            hod = 'Mr. Diego'
        elif courseid == 'MBA2':
            d = 'Management'
            b = 'Two'
            hod = 'Mr. Calvin'
        else:
            d = 'Unknown'
            b = 'Unknown'
            hod = 'Unknown'
        return d, b, hod

    def course_check(val):
        """ Define a function to check the course type (Masters or Bachelors)."""
        c = None
        if course_name.startswith('M'):
            c = 'Masters'
        elif course_name.startswith('B'):
            c = 'Bachelors'
        return c

    result = dept(courseid)
    if result:
        department, batch, hod_name = result
    course = course_check(course_name)

    insert_query = ("INSERT INTO id_details (student_ids, department, batch, course, hod_name ) "
                    "VALUES (%s, %s, %s, %s, %s);")
    cursor.execute(insert_query, (autogenerated_id, department, batch, course, hod_name))

    # Commit the changes to the database
    connection.commit()

    return render_template('courses.html')


# Select courses- inprogress
@app.route('/courses')
def course_filter():
    return render_template('courses.html')


# Calculate average age of members
@app.route('/avg-age')
def age():
    """Calculate the average age of members whose data is collected."""
    cursor = connection.cursor()
    cursor.execute("SELECT Round(AVG(age)) AS average_age FROM pro_schema.user;")
    result = cursor.fetchone()

    if result:
        average_age = result[0]
    else:
        average_age = "N/A"

    return render_template('average-age.html', average_age=average_age)


@app.route('/members')
def members_table():
    """Shows the list of all the user data collected till date."""

    hello = "no data"
    final_data = ""

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    cursor.execute("SELECT age, name FROM pro_schema.user;")
    rows = cursor.fetchall()
    for each_row in rows:
        final_data += f"<tr><td> {each_row[1]} </td><td> {each_row[0]} </td></tr>"
    output = hello.replace('no data', final_data)
    return render_template('member-list.html', output=output)


@app.route('/answers')
def get_question():
    return render_template('answers.html')


@app.route('/ask', methods=['POST'])
def ask_question():
    """Submit a question and get answer from openAI."""

    question = request.form['question']
    print(question)
    api_key = os.getenv('API_KEY')
    endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }
    if 'rephrase' in request.form:
        print("Rephrase button clicked")
        rephrase_data = json.dumps({
            "model": "gpt-3.5-turbo-0613",
            "messages": [
                {
                    "role": "system",
                    "content": f" Rephrase {question}"

                }
            ]
        })
        response1 = requests.request("POST", endpoint, headers=headers, data=rephrase_data)
        result1 = response1.json()
        generated_text1 = result1['choices'][0]['message']['content']
        return render_template('response.html', response=generated_text1)

    elif 'convert' in request.form:
        print("Convert button clicked")
        bullets_data = json.dumps({
            "model": "gpt-3.5-turbo-0613",
            "messages": [
                {
                    "role": "system",
                    "content": f" Generate content within 120 words for: {question}"
                }
            ]
        })
        response2 = requests.request("POST", endpoint, headers=headers, data=bullets_data)
        result2 = response2.json()
        print(result2)
        generated_text2 = result2['choices'][0]['message']['content']
        return render_template('response-bullets.html', response=generated_text2)


@app.route('/browse')
def get_file():
    return render_template('browse.html')


bucket_name = "hallmark1"


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload the file to the relevant folder in the S3 database bucket."""

    files = request.files.getlist('file_list')
    if files:
        s3 = boto3.client('s3')
        print(files)
        for file in files:
            filename = file.filename
            file_ext = filename.rsplit('.', 1)[-1]
            print(filename)
            print(file_ext)
            print(bucket_name)
            if file_ext in ('png', 'jpg'):
                folder_location = f"pavi_images/{filename}"
                s3.upload_fileobj(file, bucket_name, folder_location)

            elif file_ext in ('pdf', 'txt', 'docx', 'doc'):
                folder_location = f"pavi_files/{filename}"
                s3.upload_fileobj(file, bucket_name, folder_location)
            else:
                s3.upload_fileobj(file, bucket_name, file.filename)

        return 'File uploaded successfully'
    else:
        return 'No file provided'


@app.route('/search')
def search_file():
    """Search the database for matching keywords nnd get the results as the files."""

    s3 = boto3.client('s3')
    search_query = request.args.get('keyword', '').lower()
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = []
    for each_item in response.get('Contents'):
        key = each_item['Key']
        if search_query in key.lower():
            files.append(key)
    return render_template('browse.html', files=files)


@app.route('/download')
def download():
    """Provide the option to download the files from teh database onto the local directory."""

    s3 = boto3.client('s3')
    filename = request.args.get('file')
    s3_object = s3.get_object(Bucket=bucket_name, Key=filename)
    file_data = s3_object['Body'].read()

    # Serve the file to the client
    return send_file(io.BytesIO(file_data), download_name=filename, as_attachment=True)


app.run(debug=True, host="0.0.0.0")

# Close the cursor and connection
connection.close()
