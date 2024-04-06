import uuid 
from extensions import db

class Claims(db.Model):
    __tablename__ = "Claims"

    ClaimID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    PolicyID = db.Column(db.String(50), db.ForeignKey('Policies.PolicyID'))
    CustomerID = db.Column(db.String(50), db.ForeignKey('Customer.CustomerID'))
    DateFiled = db.Column(db.Date, nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    Status = db.Column(db.String(20), default='Pending')

    # Define the relationship with Policies and Customer tables
    policy = db.relationship("Policies", back_populates="claims")
    customer = db.relationship("Customer", back_populates="claims")