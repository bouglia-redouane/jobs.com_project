import mysql.connector
from mysql.connector import Error

# Define the SQL script as a string
sql_script = """
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    mot_de_pass TEXT NOT NULL,
    telephone TEXT NOT NULL,
    description TEXT,
    Domaine_d_expertise TEXT,
    localisation TEXT,
    lien_photo TEXT
);

CREATE TABLE IF NOT EXISTS Diplome (
    id INT AUTO_INCREMENT PRIMARY KEY,
    specialite TEXT,
    intitule TEXT NOT NULL,
    etablissement_d_obtention TEXT NOT NULL,
    annee DATE NOT NULL,
    niveau TEXT
);

CREATE TABLE IF NOT EXISTS Skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS User_Skills (
    id_user INT NOT NULL,
    id_skill INT NOT NULL,
    mastering TEXT,
    PRIMARY KEY (id_user, id_skill),
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_skill) REFERENCES Skill(id)
);

CREATE TABLE IF NOT EXISTS User_Diplomes (
    id_diplome INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id_diplome, id_user),
    FOREIGN KEY (id_diplome) REFERENCES Diplome(id),
    FOREIGN KEY (id_user) REFERENCES user(id)
);
"""

def create_connection(host_name, port, user_name, user_password, db_name):
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port=port,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query):
    """Execute a SQL query."""
    cursor = connection.cursor()
    try:
        # Split the SQL script into individual queries
        queries = query.split(';')
        for q in queries:
            if q.strip():  # Ignore empty queries
                cursor.execute(q.strip())
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
# Main execution
if __name__ == "__main__":
    # Replace these with your actual MySQL credentials
    host = "mysql-3daf98a4-jobs-search-engine.e.aivencloud.com"  # e.g., "localhost"
    port = 28306         # Default MySQL port
    username = "avnadmin"
    database = "jobs_db"

    # Create a connection to the database
    connection = create_connection(host, port, username, password, database)

    if connection:
        # Execute the SQL script to create tables
        execute_query(connection, sql_script)
        connection.close()
        print("MySQL connection is closed")
