import uuid 
from extensions import db
class Policies(db.Model):
    __tablename__ = "Policies"
    
    PolicyID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    CustomerID = db.Column(db.String(50), db.ForeignKey('Customer.CustomerID'))
    PolicyTypeID = db.Column(db.String(50), db.ForeignKey('PolicyType.PolicyTypeID'))
    ItemInsured = db.Column(db.String(255), nullable=False)
    InsuredValue = db.Column(db.DECIMAL(18, 2), nullable=False)
    MonthlyPremium = db.Column(db.DECIMAL(18, 2), nullable=False)
    DateTakenOut = db.Column(db.Date, nullable=False)
    DateActive = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(20), default='Active')

    def to_dict(self):
        return {
            "PolicyID": self.PolicyID,
            "CustomerID": self.CustomerID,
            "PolicyTypeID": self.PolicyTypeID,
            "ItemInsured": self.ItemInsured,
            "InsuredValue": str(self.InsuredValue), 
            "MonthlyPremium": str(self.MonthlyPremium), 
            "DateTakenOut": str(self.DateTakenOut),  
            "DateActive": str(self.DateActive), 
            "Status": self.Status
        }

    customer = db.relationship("Customer", back_populates="policies", foreign_keys=[CustomerID])
    policy_type = db.relationship("PolicyType", back_populates="policies")
    claims = db.relationship("Claims", back_populates="policy")