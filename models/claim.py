from datetime import datetime
import uuid 
from extensions import db

class Claims(db.Model):
    __tablename__ = "Claims"

    ClaimID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    PolicyID = db.Column(db.String(50), db.ForeignKey("Policies.PolicyID"))
    CustomerID = db.Column(db.String(50), db.ForeignKey("Customer.CustomerID"))
    DateFiled = db.Column(db.Date, default=datetime.now(),nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    Status = db.Column(db.String(20), default="Pending")

    def to_dict(self):
        return {
            "PolicyID": self.PolicyID,
            "CustomerID": self.CustomerID,
            "ClaimID": self.ClaimID,
            "DateFiled": self.DateFiled,
            "Description": self.Description, 
            "Amount": self.Amount, 
            "Status": self.Status
        }

    # Define the relationship with Policies and Customer tables
    policy = db.relationship("Policies", back_populates="claims")
    customer = db.relationship("Customer", back_populates="claims")