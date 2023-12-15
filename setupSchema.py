import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    user='root', password='', host='localhost')
cursor = connection.cursor()

# Data Definition
f = open("SpotifyData.sql", "r")
schema_string = f.read()

try:
    for result in cursor.execute(schema_string, multi=True):
        pass
except mysql.connector.Error as error_descriptor:
    if error_descriptor.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists: {}".format(error_descriptor))
    else:
        print("Failed creating schema: {}".format(error_descriptor))
    exit(1)

try:
    cursor.execute("USE {}".format("SpotifyData"))
except mysql.connector.Error as error_descriptor:
    print("Failed using database: {}".format(error_descriptor))
    exit(1)

cursor.close()
connection.close()
