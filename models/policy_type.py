import uuid 
from extensions import db

class PolicyType(db.Model):
    __tablename__ = "PolicyType"

    PolicyTypeID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "PolicyTypeID": self.PolicyTypeID,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "img": self.img,
            "alt": self.alt
        }
    
    policies = db.relationship("Policies", back_populates="policy_type")