from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

bcrypt = Bcrypt()

# Group all authentification related routes under /api/auth
auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json()

    # Check all required fields are present
    if not data or not data.get("email") or not data.get("password") or not data.get("display_name") or not data.get("academic_year"):
        return jsonify({"error": "All fields are required"}), 400

    # Converts email to lowercase and makes sure to only allow ALU students' and staff email addresses
    email = data["email"].lower()
    if not email.endswith("@alustudent.com") and not email.endswith("@alustaff.com"):
        return jsonify({"error": "You must use your ALU student email to register"}), 400

    # Check email isn't already taken
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    # Hash the password
    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    # Create the user and save to database
    user = User(
        email         = email,
        password_hash = password_hash,
        display_name  = data["display_name"],
        academic_year = int(data["academic_year"]),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created!", "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    
    # Verifies that both the email and password are provided
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    
    # Finds user by email
    user = User.query.filter_by(email=data["email"].lower()).first()
    
    # Checks if user exists and password matches the stored hash and rejects any suspended accounts. 
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account suspended"}), 403

    # Generate token with the user's id inside it
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Logged in!",
        "token":   token,
        "user":    user.to_dict()
    }), 200


@auth_bp.get("/me")
@jwt_required()
def me():

    # Retrieve the user's id from the JWT token
    user_id = get_jwt_identity()

    # Fetch user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200