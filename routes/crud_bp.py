import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models.customer import Customer
from models.policy import Policies
from models.claim import Claims
from models.policy_type import PolicyType

crud_bp = Blueprint("crud_bp", __name__)

@crud_bp.get("/")
def get_users():
    user_list = Customer.query.all() 
    data = [user.to_dict() for user in user_list] 
    return jsonify(data)

@crud_bp.get("/<id>")
def get_user(id):
    user = Customer.query.get(id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@crud_bp.delete("/<id>")
def delete_user(id):
   user = Customer.query.get(id) 
   if not user:
        return jsonify({"message": "User not found"}), 404
   try:
       db.session.delete(user)
       db.session.commit() 
       return jsonify({"message": "User deleted successfully", "data": user.to_dict()}), 200
   except Exception as e:
      db.session.rollback() 
      return jsonify({"message": str(e)}), 500
    
@crud_bp.post("/")
def create_user():
    data = request.json
    new_user = Customer(**data)
    try:
        db.session.add(new_user)
        db.session.commit()
        result = {"message": "Added successfully", "data": new_user.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500

@crud_bp.put("/<id>")
def update_user_by_id(id):
    user = Customer.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    body = request.json  
 
    try:
        for key, value in body.items():
            if hasattr(user, key):
                setattr(user, key, value)
 
        db.session.commit()
        return jsonify(
            {"message": "User updated successfully!", "data": user.to_dict()}
        )
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500
    
@crud_bp.get("/policy-type")
def get_all_policy_types():
    policy_type_list = PolicyType.query.all() 
    data = [policy_type.to_dict() for policy_type in policy_type_list] 
    return jsonify(data)

@crud_bp.get("/policy-type/<id>")
def get_policy_type(id):
    policy_type = PolicyType.query.get(id)
    if policy_type is None:
        return jsonify({"error": "policy_type not found"}), 404
    return jsonify(policy_type.to_dict())

@crud_bp.delete("/policy-type/<id>")
def delete_policy_type(id):
   policy_type = PolicyType.query.get(id) 
   if not policy_type:
        return jsonify({"message": "policy_type not found"}), 404
   try:
       db.session.delete(policy_type)
       db.session.commit() 
       return jsonify({"message": "policy_type deleted successfully", "data": policy_type.to_dict()}), 200
   except Exception as e:
      db.session.rollback() 
      return jsonify({"message": str(e)}), 500
    
@crud_bp.post("/policy-type")
def create_policy_type():
    data = request.json
    new_policy_type = PolicyType(**data)
    try:
        db.session.add(new_policy_type)
        db.session.commit()
        result = {"message": "Added successfully", "data": new_policy_type.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500

@crud_bp.put("/policy-type/<id>")
def update_policy_type(id):
    policy_type = PolicyType.query.get(id)
    if not policy_type:
        return jsonify({"message": "policy_type not found"}), 404
    body = request.json  
 
    try:
        for key, value in body.items():
            if hasattr(policy_type, key):
                setattr(policy_type, key, value)
 
        db.session.commit()
        return jsonify(
            {"message": "policy_type updated successfully!", "data": policy_type.to_dict()}
        )
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500
    
@crud_bp.get("/policies")
def get_all_policies():
    policies = Policies.query.all() 
    data = [policy.to_dict() for policy in policies] 
    return jsonify(data)

@crud_bp.get("/policies/<id>")
def get_policy(id):
    policy = Policies.query.get(id)
    if policy is None:
        return jsonify({"error": "policy not found"}), 404
    return jsonify(policy.to_dict())

@crud_bp.delete("/policies/<id>")
def delete_policy(id):
   policy = Policies.query.get(id) 
   if not policy:
        return jsonify({"message": "policy not found"}), 404
   try:
       db.session.delete(policy)
       db.session.commit() 
       return jsonify({"message": "policy deleted successfully", "data": policy.to_dict()}), 200
   except Exception as e:
      db.session.rollback() 
      return jsonify({"message": str(e)}), 500
    
@crud_bp.post("/policies")
def create_policy():
    data = request.json
    new_policy = Policies(**data)
    try:
        db.session.add(new_policy)
        db.session.commit()
        result = {"message": "Added successfully", "data": new_policy.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500

@crud_bp.put("/policies/<id>")
def update_policy(id):
    policy = Policies.query.get(id)
    if not policy:
        return jsonify({"message": "policy not found"}), 404
    body = request.json  
 
    try:
        for key, value in body.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
 
        db.session.commit()
        return jsonify(
            {"message": "policy updated successfully!", "data": policy.to_dict()}
        )
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500

@crud_bp.get("/claims")
def get_all_claims():
    claims = Claims.query.all() 
    data = [claims.to_dict() for claims in claims] 
    return jsonify(data)

@crud_bp.get("/claims/<id>")
def get_claim(id):
    claim = Claims.query.get(id)
    if claim is None:
        return jsonify({"error": "claim not found"}), 404
    return jsonify(claim.to_dict())

@crud_bp.delete("/claims/<id>")
def delete_claim(id):
   claim = Claims.query.get(id) 
   if not claim:
        return jsonify({"message": "claim not found"}), 404
   try:
       db.session.delete(claim)
       db.session.commit() 
       return jsonify({"message": "claim deleted successfully", "data": claim.to_dict()}), 200
   except Exception as e:
      db.session.rollback() 
      return jsonify({"message": str(e)}), 500
    
@crud_bp.post("/claims")
def create_claim():
    data = request.json
    new_claim = Claims(**data)
    try:
        db.session.add(new_claim)
        db.session.commit()
        result = {"message": "Added successfully", "data": new_claim.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500

@crud_bp.put("/claim/<id>")
def update_claim(id):
    claim = Claims.query.get(id)
    if not claim:
        return jsonify({"message": "claim not found"}), 404
    body = request.json  
 
    try:
        for key, value in body.items():
            if hasattr(claim, key):
                setattr(claim, key, value)
 
        db.session.commit()
        return jsonify(
            {"message": "claim updated successfully!", "data": claim.to_dict()}
        )
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e)}), 500