import json
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

class DBClass:
    def __init__(self, path="connection_infos.json"):
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
            query = "SELECT COUNT(*) FROM users WHERE mail = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking if user exists: {e}")
            return False

    def add_user(self, nom, prenom, motDePass, mail, telephone=None, description=None,
                 domaineExpertise=None, localisation=None, diplomes=None, competences=None, photo=None):
        """
        Add a new user to the database, including their diplomas and skills.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(motDePass.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor = self.cnx.cursor()

            # Step 1: Insert the user into the users table
            query_users = """
                INSERT INTO users (nom, prenom, motDePass, mail, telephone, description, 
                                   domaineExpertise, localisation,photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
            """
            cursor.execute(query_users, (nom, prenom, hashed_password, mail, telephone, description,
                                         domaineExpertise, localisation,photo))

            # Get the ID of the newly inserted user
            user_id = cursor.lastrowid

            # Step 2: Insert diplomas into the Diplome table and link them to User_Diplomas
            if diplomes:
                for diploma in diplomes:
                    # Insert diploma into the Diplome table
                    query_diplome = """
                        INSERT INTO Diplome (specialite, intitule, etablissement_d_obtention, annee, niveau)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_diplome, (
                        diploma.specialite,  # Specialization
                        diploma.intitule,  # Title
                        diploma.etablissement_d_obtention,  # Institution
                        diploma.annee,  # Year
                        diploma.niveau  # Level
                    ))

                    # Get the ID of the newly inserted diploma
                    diplome_id = cursor.lastrowid

                    # Link the user to the diploma in the User_Diplomas table
                    query_user_diplomas = """
                        INSERT INTO User_Diplomas (id_user, id_diplome)
                        VALUES (%s, %s)
                    """
                    cursor.execute(query_user_diplomas, (user_id, diplome_id))

            # Step 3: Insert skills into the Skill table and link them to User_Skill
            if competences:
                for competence in competences:
                    # Insert skill into the Skill table
                    query_skill = """
                        INSERT INTO Skill (skill, description)
                        VALUES (%s, %s)
                    """
                    cursor.execute(query_skill, (
                        competence.skill,  # Skill name
                        competence.description  # Description
                    ))

                    # Get the ID of the newly inserted skill
                    skill_id = cursor.lastrowid

                    # Link the user to the skill in the User_Skill table
                    query_user_skills = """
                        INSERT INTO User_Skill (id_user, id_skill)
                        VALUES (%s, %s)
                    """
                    cursor.execute(query_user_skills, (user_id, skill_id))

            # Commit all changes to the database
            self.cnx.commit()
            cursor.close()
            print("User, diplomas, and skills successfully added.")
            return True

        except Error as e:
            print(f"Error adding user: {e}")
            self.cnx.rollback()  # Rollback in case of error
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

    def user_exists(self, email):
        """
        Check if a user exists in the database by email.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT COUNT(*) FROM users WHERE mail = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Error as e:
            print(f"Error checking if user exists: {e}")
            return False

