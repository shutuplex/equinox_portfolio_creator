from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash, redirect, render_template, request, session, url_for , Blueprint
from models.user_model import create_user ,get_user,username_exists 

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for("auth.login"))
            
        if len(username) > 20:
            flash("Username too long (max 20 characters)", "error")
            return redirect(url_for("auth.login"))
            
        if ' ' in username:
            flash("Username cannot contain spaces", "error")
            return redirect(url_for("auth.login"))
            
        user = get_user(username)
        
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            flash("Login Successful!", "success")
            return redirect(url_for("home"))  
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login"))
    
    if "user" in session:  
        flash("Already logged in", "info")
        return redirect(url_for("home"))
    
    return render_template("login.html")

@auth.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for("auth.register"))
            
        if len(username) < 4:
            flash("Username must be at least 4 characters", "error")
            return redirect(url_for("auth.register"))
            
        if len(username) > 20:
            flash("Username too long (max 20 characters)", "error")
            return redirect(url_for("auth.register"))
            
        if ' ' in username:
            flash("Username cannot contain spaces", "error")
            return redirect(url_for("auth.register"))
            
        if len(password) < 8:
            flash("Password must be at least 8 characters", "error")
            return redirect(url_for("auth.register"))
            
        if not any(char.isdigit() for char in password):
            flash("Password must contain at least one number", "error")
            return redirect(url_for("auth.register"))
            
        if not any(char.isalpha() for char in password):
            flash("Password must contain at least one letter", "error")
            return redirect(url_for("auth.register"))
        
        if username_exists(username):
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))
        
        create_user(username,password)
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template('register.html')

@auth.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("auth.login"))