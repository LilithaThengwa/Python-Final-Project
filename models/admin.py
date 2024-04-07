import uuid
from flask_login import UserMixin 
from extensions import db

class Admin(UserMixin, db.Model):
     __tablename__ = "Admin"
     AdminID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
     FirstName = db.Column(db.String(50), nullable=False)
     LastName = db.Column(db.String(50), nullable=False)
     EmployeeNumber = db.Column(db.String(50), nullable=False, unique=True)
     Email = db.Column(db.String(50), nullable=False)
     Password = db.Column(db.String(250), nullable=False)
     role = db.Column(db.String(20), default="admin")

     def get_id(self):
        return str(self.AdminID)

     def to_dict(self):
        return {
            "AdminID" : self.AdminID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "EmployeeNumber": self.EmployeeNumber,
            "Password": self.Password,
            "Email": self.Email,
            "Password": self.Password,    
        }
     
