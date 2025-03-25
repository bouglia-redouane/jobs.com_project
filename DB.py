import json
import mysql.connector
from mysql.connector import Error
import os
import bcrypt

class DBClass:
    def __init__(self, path="/home/redouane/Downloads/connection_infos.json"):
        self.path = path
        self.cnx = None
        self.establish_connection()

    def establish_connection(self):
        """
        Establish a connection to the MySQL database using credentials from a JSON file.
        """
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError("Connection details file not found")

            with open(self.path, 'r') as file:
                config = json.load(file)

            self.cnx = mysql.connector.connect(
                host=config.get("Host"),
                user=config.get("User"),
                password=config.get("Password"),
                database=config.get("Database_name"),
                port=int(config.get("Port", 28306))
            )
        except Error as e:
            print(f"Error connecting to database: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def user_exists(self, email):
        """
        Check if a user exists in the database by email.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT COUNT(*) FROM user WHERE mail = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking if user exists: {e}")
            return False

    def diplome_exists(self, intitule, etablissement_d_obtention):
        """
        Check if a user exists in the database by email.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT COUNT(*) FROM Diplome WHERE intitule = %s and etablissement_d_obtention = %s"
            cursor.execute(query, (intitule, etablissement_d_obtention))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking if diplome exists: {e}")
            return False

    def execute_query(self, key_word, location):
        """
        Execute a SQL query to fetch job posts based on keyword and location.
        """
        if not self.cnx:
            print("No active database connection.")
            return None

        try:
            cursor = self.cnx.cursor(dictionary=True)
            query = """
                SELECT * FROM offre 
                WHERE job_title LIKE %s or location LIKE %s
            """
            cursor.execute(query, (f"%{key_word}%", f"%{location}%"))
            results = cursor.fetchall()
            cursor.close()
            return json.dumps(results, indent=4, ensure_ascii=False)
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def add_user_infos(self, email, password, nom, prenom, telephone, description=None, domaine_d_expertise=None,
                 localisation=None, lien_photo=None):
        """
        Add a new user to the database with a hashed password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        if self.user_exists(email):
            print("User already exists.")
            return False

        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the user into the database
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO user (nom, prenom, mot_de_pass, telephone, description, Domaine_d_expertise, localisation, lien_photo, mail)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                nom,
                prenom,
                hashed_password.decode('utf-8'),  # Store the hashed password as a string
                telephone,
                description,
                domaine_d_expertise,
                localisation,
                lien_photo,
                email
            )
            cursor.execute(query, values)
            self.cnx.commit()
            id = cursor.lastrowid
            cursor.close()
            print("User added successfully.")
            return True,id
        except Error as e:
            print(f"Error adding user: {e}")
            return False

    def add_diplome(self, intitule, etablissement_d_obtention, annee, specialite=None, niveau=None):
        """
        Add a new diplome to the database with a hashed password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False
        if self.diplome_exists(intitule, etablissement_d_obtention):
            print("Diplome already exists.")
            return False, self.get_diplome_id(intitule, etablissement_d_obtention)
        try:
            # Insert the user into the database
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO Diplome (intitule, etablissement_d_obtention, annee, specialite, niveau)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (intitule, etablissement_d_obtention, annee, specialite, niveau)
            cursor.execute(query, values)
            self.cnx.commit()
            id = cursor.lastrowid
            cursor.close()
            print("Diplome added successfully.")
            return True,id
        except Error as e:
            print(f"Error adding Diplome: {e}")
            return False

    def skill_exists(self, skill):
        """
        Check if a user exists in the database by email.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT COUNT(*) FROM Skill WHERE Skill.skill = %s"
            cursor.execute(query, (skill,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking if skill exists: {e}")
            return False
    def add_skill(self, skill):
        """
        Add a new Skill to the database with a hashed password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False
        if self.skill_exists(skill):
            print("Skill already exists.")
            return False
        try:
            # Insert the user into the database
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO Skill (skill)
                VALUES (%s)
            """
            values = (skill, )
            cursor.execute(query, values)
            self.cnx.commit()
            id = cursor.lastrowid
            cursor.close()
            print("Skill added successfully.")
            return True,cursor.id
        except Error as e:
            print(f"Error adding Skill: {e}")
            return False
    def get_diplome_id(self, intitule, etablissement_d_obtention):

        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT id FROM Diplome WHERE intitule = %s and etablissement_d_obtention = %s"
            cursor.execute(query, (intitule,etablissement_d_obtention))
            result = cursor.fetchone()
            cursor.close()
            return result[0]
        except Error as e:
            print(f"Error: {e}")
            return False