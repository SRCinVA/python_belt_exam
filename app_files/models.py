from django.db import models
import re, bcrypt
from datetime import datetime, date


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+.-_]+@[a-zA-Z0-9+.-_]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self,data):       
        errors = {}                 
        
        if len(data['name']) < 1:
            errors['name'] = "You must enter a name"
        elif len(data['name']) < 3:
            errors['name'] = "Your name must be at least 3 characters"

        if len(data['alias']) < 1:
            errors['alias'] = "You must enter an alias"
        elif len(data['alias']) < 3:
            errors['alias'] = "Your alias must be at least 3 characters long"

        if len(data['email']) < 1:
            errors['email'] = "An email is required"
        elif not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email, dude"
        else:
            users = User.objects.filter(email=data['email'])
            if len(users) > 0:
                errors['email'] = "Email is already in use"

        if len(data['password']) < 1:
            errors['password'] = "You must enter a password"
        elif len(data['password']) < 8:
            errors['password'] = "Your password must be 8 characters or longer"

        if data['password'] != data['confirm_password']:
            errors['confirm_password'] = "The passwords do not match!"

        if len(data['date_of_birth']) < 1:
            errors['date_of_birth'] = "Please enter your date of birth"
        else:
            d = datetime.strptime(data['date_of_birth'],"%Y-%m-%d")
            if d > datetime.now():
                errors['date_of_birth'] = "You've already been born, so COME ON now..."

        if len(errors) == 0:
            return User.objects.create(    
                name = data['name'],
                alias = data['alias'],
                email = data['email'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode(),
                date_of_birth = data['date_of_birth'],
                )
        else:
            return errors

    def login(self, data): # arguments of self and data passed in by "form" in the HTML.
        print("in our models", data)
        errors = {}

        if len(data['email']) < 1:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email"
        else:
            list_of_users_with_this_email = User.objects.filter(email=data['email'])
            if len(list_of_users_with_this_email) < 1:
                errors['email'] = "Email is not in use"

        if len(data['password']) < 8:
            errors['password'] = "Password must be 8 characters or longer"

        if len(errors) == 0:
            stored_password = list_of_users_with_this_email[0].password 
            if not bcrypt.checkpw(data['password'].encode(), stored_password.encode()):  
                errors['password'] = "Incorrect Password"                                 
                return errors                                                              
            else:
                return list_of_users_with_this_email[0]
        else:
            return errors

class User(models.Model):   
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

class QuoteManager(models.Manager): 
    def add_quote(self, data, user_id):
        print(data)

        if len(data["author"]) < 1:
            return {"author": "Who gave us this brilliant gem??"}
        elif len(data["author"]) < 3:
            return {"author": "Is this person's name *seriously* shorter than 3 letters?"}

        if len(data["quote"]) < 1:
            return {"quote": "If you're hitting this button, then at least try to enter something :)"}
        elif len(data["quote"]) < 10:
            return {"quote": "The quote needs to be at least 10 characters long ..."}
        else:
            return Quote.objects.create(
                #author = data['author'],
                quote = data['quote'],
                user_id = user_id
            )

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="quotes", on_delete = models.CASCADE)
    favs = models.ManyToManyField(User, related_name="fav_quotes")

    objects = QuoteManager()