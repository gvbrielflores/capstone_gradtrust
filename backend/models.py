from app import db

class issuers(db.Model):
    #id = blockchain address
    id = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255))
    signature = db.Column(db.String(300))

    def __repr__(self):
        return f'Issuer with ID {self.id} and Name {self.name}'

class accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(255), nullable = False, unique=True)
    password = db.Column(db.String(255))

    def __repr__(self):
        return f'Account with ID {self.id} and Name {self.email}'
