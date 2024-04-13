import uuid
from flask_login import UserMixin 
from extensions import db

class Customer(UserMixin, db.Model):
     __tablename__ = "Customer"
     CustomerID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
     FirstName = db.Column(db.String(50), nullable=False)
     LastName = db.Column(db.String(50), nullable=False)
     Username = db.Column(db.String(50), nullable=False, unique=True)
     PhoneNumber = db.Column(db.String(50), nullable=False)
     Email = db.Column(db.String(50), nullable=False)
     Password = db.Column(db.String(250), nullable=False)
     role = db.Column(db.String(20), default="user")

     def get_id(self):
        return str(self.CustomerID)

     def to_dict(self):
        return {
            "CustomerID" : self.CustomerID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Username": self.Username,
            "Password": self.Password,
            "PhoneNumber": self.PhoneNumber,
            "Email": self.Email,
            "Password": self.Password,    
        }
     
     policies = db.relationship("Policies", back_populates="customer")
     claims = db.relationship("Claims", back_populates="customer")