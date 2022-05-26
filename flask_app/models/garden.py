from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Garden:
    db= 'garden'
    def __init__ (self, data):
        self.id = data ['id']
        self.crop = data ['crop']
        self.variety = data ['variety']
        self.date_planted = data ['date_planted']
        self.days_to_harvest = data ['days_to_harvest']
        self.notes = data ['notes']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        self.user = user.User.get_by_id({"id": data['user_id']})

    @staticmethod
    def validate_garden(form_data):
        is_valid = True
        if len(form_data['crop']) < 2:
            is_valid = False
            flash ("Crop name must be at least two characters")
        if len(form_data['variety']) < 2:
            is_valid = False
            flash ("Crop variety must be at least 2 characters")
        if (form_data ["date_planted"]) == "":
            is_valid = False
            flash("Please enter a plant date")
        if float(form_data['days_to_harvest']) < 1:
            is_valid = False
            flash("Days to harvest must be set greater than zero")
        return is_valid


    @classmethod
    def create(cls, data):
        query = 'INSERT INTO gardens (crop, variety, date_planted, days_to_harvest, notes, user_id) VALUES (%(crop)s,%(variety)s,%(date_planted)s, %(days_to_harvest)s, %(notes)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_all_by_id(cls, data):
        query = "SELECT * FROM gardens WHERE user_id = gardens.user_id;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results 
    

    #@classmethod
    #def get_all(cls, data):
        query = "SELECT * from users JOIN gardens WHERE users.id = gardens.user_id;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gardens;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_gardens = []
        for row in results:
            all_gardens.append( cls(row) )
        return all_gardens


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM gardens WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE gardens SET crop=%(crop)s, variety=%(variety)s, date_planted=%(date_planted)s, days_to_harvest=%(days_to_harvest)s, notes=%(notes)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM gardens WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    #@classmethod
    #def all_entries(cls):
        query = 'SELECT * FROM gardens JOIN user on garden.user_id = user_id;'
        results = connectToMySQL(cls.db).query_db(query)
        return results

        
