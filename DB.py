import json
import time
import mysql.connector
from mysql.connector import Error
import os
import bcrypt
from datetime import datetime, timedelta
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

    def add_diplome(self, val):
        """
        Add a new diplome to the database with a hashed password.
        """
        intitule = val.intitule
        etablissement_d_obtention = val.etablissement
        annee = val.annee
        specialite = val.specialite
        niveau = val.niveau
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
            return False, self.get_skill_id(skill)
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
            return True, id
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

    def get_skill_id(self, skill):

        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT id FROM Skill WHERE skill = %s"
            cursor.execute(query, (skill, ))
            result = cursor.fetchone()
            cursor.close()
            return result[0]
        except Error as e:
            print(f"Error: {e}")
            return False
    def sing_up(self, form_data):
        res = self.add_user_infos(
                                    nom=form_data.nom,
                                    prenom=form_data.prenom,
                                    password=form_data.motDePass,
                                    email=form_data.mail,
                                    telephone=form_data.telephone,
                                    description=form_data.description,
                                    domaine_d_expertise=form_data.domaineExpertise,
                                    localisation=form_data.localisation,
                                    lien_photo=form_data.photo
                                )
        if not res: return res
        response, user_id = res
        diplome_res = [self.add_diplome(val) for val in form_data.diplomes]
        diplome_stats, diplomes_id = [1 if val[0] else 0 for val in diplome_res], [val[1] for val in diplome_res]
        skill_res = [self.add_skill(val) for val in form_data.competences]
        skill_stats, skills_id = [1 if val[0] else 0 for val in skill_res], [val[1] for val in skill_res]
        user_diplome_stats = [1 if self.add_user_diplome(user_id, val) else 0 for val in diplomes_id]
        user_skill_stats = [1 if self.add_user_skill(user_id, val) else 0 for val in skills_id]
        return  {
            "Newly added user": 1,
            "Newly added diploma": sum(diplome_stats),
            "Newly added skill": sum(skill_stats),
            "Newly added user skills": sum(user_skill_stats),
            "Newly added user diplomas": sum(user_diplome_stats)
        }

    def add_user_skill(self, user_id, skill_id, mastering=None):
        """
        Add a new Skill to the database with a hashed password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False
        try:
            # Insert the user into the database
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO User_Skills (id_user, id_skill, mastering)
                VALUES (%s, %s, %s)
            """
            values = (user_id, skill_id, mastering)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            print("User skill added successfully.")
            return True
        except Error as e:
            print(f"Error adding user Skill: {e}")
            return False

    def add_user_diplome(self, user_id, diplome_id):
        """
        Add a new Skill to the database with a hashed password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False
        try:
            # Insert the user into the database
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO User_Diplomes (id_user, id_diplome)
                VALUES (%s, %s)
            """
            values = (user_id, diplome_id)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            print("User diplome added successfully.")
            return True
        except Error as e:
            print(f"Error adding user diplome: {e}")
            return False

    def verify_password(self, email, password):
        """
        Verify the user's password.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "SELECT mot_de_pass FROM user WHERE mail = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                hashed_password = result[0].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            return False
        except Error as e:
            print(f"Error verifying password: {e}")
            return False

    def generate_token(self):
        """
        Generate a unique token and store it in the database with an expiration time of 1 hour.
        """
        if not self.cnx:
            print("No active database connection.")
            return None

        token = hex(int(time.time() * 1000))[2:].zfill(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        try:
            cursor = self.cnx.cursor()
            query = """
                INSERT INTO tokens (token, expires_at)
                VALUES (%s, %s)
            """
            cursor.execute(query, (token, expires_at))
            self.cnx.commit()
            cursor.close()
            return token
        except Error as e:
            print(f"Error generating token: {e}")
            return None

    def validate_token(self, token):
        """
        Check if the token exists in the database.
        Returns True if the token exists, False otherwise.
        """
        if not self.cnx:
            print("No active database connection.")
            return False

        try:
            cursor = self.cnx.cursor()
            query = """
                SELECT 1 FROM tokens WHERE token = %s
            """
            cursor.execute(query, (token,))
            result = cursor.fetchone()  # Fetch the result (if any)
            cursor.close()

            # Return True if the token exists, False otherwise
            return bool(result)
        except Error as e:
            print(f"Error validating token: {e}")
            return False