import os
import uuid 
import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient 
from models.user_model import pget_user , pcreate_user,pinsert_user,portfolio_collection


portfolio = Blueprint("portfolio", __name__)

UPLOAD_FOLDER = "static/images" 
default_pfp = "https://files.catbox.moe/n4p5i1.jpg"

@portfolio.route("/template",methods=["GET", "POST"]) 
def template():
    if "user" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth.login"))
    return render_template("templates.html") 

@portfolio.route("/form", methods=["POST"])
def form():
    if "user" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth.login"))
    selected_template = request.form.get("selected_template")
    session["selected_template"] = selected_template 
    return render_template("info.html")

@portfolio.route("/save", methods=["POST"])
def save():
    if "user" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth.login"))

    username = session["user"]
    selected_template = session.get("selected_template")  
    
    name = request.form.get("firstname")
    lastname = request.form.get("lastname")
    school = request.form.get("school")
    college = request.form.get("college")
    phone = request.form.get("phone")
    email = request.form.get("email")
    skills = [
        request.form.get("skill1"),
        request.form.get("skill2"),
        request.form.get("skill3"),
        request.form.get("skill4"),
    ]
    about = request.form.get("about")
    instagram = request.form.get("instagram")
    github = request.form.get("github")
    img_url = request.form.get("img_url")
    
    project_names = request.form.getlist("project_names[]")
    project_links = request.form.getlist("project_links[]")
    project_descriptions = request.form.getlist("project_descriptions[]")
    
    projects = []
    for pname, link, desc in zip(project_names, project_links, project_descriptions):
        if name.strip() and link.strip():  
            projects.append({
                "name": pname.strip(),
                "link": link.strip(),
                "description": desc.strip()
            })
    achievement_names = request.form.getlist("achievement_names[]")
    achievement_images = request.form.getlist("achievement_images[]")
    achievement_descriptions = request.form.getlist("achievement_descriptions[]")
    
    achievements = []
    for aname, image, desc in zip(achievement_names, achievement_images, achievement_descriptions):
        if aname.strip():  
            achievements.append({
                "name": aname.strip(),
                "image": image.strip(),
                "description": desc.strip()
            })


            

    user = pcreate_user(
        username=username,
        firstname=name,
        lastname=lastname,
        email=email,
        phone=phone,
        school=school,
        college=college,
        skills=skills,
        about=about,
        instagram=instagram,
        github=github,
        profile_pic=img_url,
        projects=projects,
        achievements=achievements,  
        template=selected_template 
    )
    pinsert_user(portfolio_collection, user)

    flash("Portfolio data saved successfully!", "success")
    return redirect(url_for("portfolio.view", username=username))

"""@portfolio.route("/save", methods=["POST"])
def save():
    if "user" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth.login"))
    username = session["user"]
    selected_template = session.get("selected_template")  
    name = request.form.get("firstname", "").strip()
    if not re.match(r'^[A-Za-z\s\-]{2,50}$', name):
        flash("Invalid first name! Only letters, spaces and hyphens allowed (2-50 characters).", "error")
        return redirect(url_for("portfolio.form"))
    
    lastname = request.form.get("lastname", "").strip()
    if not re.match(r'^[A-Za-z\s\-]{2,50}$', lastname):
        flash("Invalid last name! Only letters, spaces and hyphens allowed (2-50 characters).", "error")
        return redirect(url_for("portfolio.form"))
    school = request.form.get("school", "").strip()
    if school and not re.match(r'^[A-Za-z0-9\s\-,\.\(\)]{3,100}$', school):
        flash("Invalid school name!", "error")
        return redirect(url_for("portfolio.form"))
    
    college = request.form.get("college", "").strip()
    if college and not re.match(r'^[A-Za-z0-9\s\-,\.\(\)]{3,100}$', college):
        flash("Invalid college name!", "error")
        return redirect(url_for("portfolio.form"))
    phone = request.form.get("phone", "").strip()
    if phone and not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', phone):
        flash("Invalid phone number format!", "error")
        return redirect(url_for("portfolio.form"))
    
    email = request.form.get("email", "").strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        flash("Invalid email address!", "error")
        return redirect(url_for("portfolio.form"))
    skills = [
        request.form.get("skill1", "").strip(),
        request.form.get("skill2", "").strip(),
        request.form.get("skill3", "").strip(),
        request.form.get("skill4", "").strip(),
    ]
    for skill in skills:
        if skill and not re.match(r'^[A-Za-z0-9\s\+#&]{2,30}$', skill):
            flash("Invalid skill format! Only letters, numbers, spaces and basic symbols allowed.", "error")
            return redirect(url_for("portfolio.form"))
    about = request.form.get("about", "").strip()
    if len(about) > 500:
        flash("About section too long! Maximum 500 characters allowed.", "error")
        return redirect(url_for("portfolio.form"))
    instagram = request.form.get("instagram", "").strip()
    if instagram and not re.match(r'^@?[a-zA-Z0-9._]{1,30}$', instagram):
        flash("Invalid Instagram username! Should be 1-30 characters with letters, numbers, dots or underscores.", "error")
        return redirect(url_for("portfolio.form"))
    
    github = request.form.get("github", "").strip()
    if github and not re.match(r'^[a-zA-Z0-9\-]{1,39}$', github):
        flash("Invalid GitHub username! Should be 1-39 characters with letters, numbers or hyphens.", "error")
        return redirect(url_for("portfolio.form"))
    img_url = request.form.get("img_url", "").strip()
    if img_url and not re.match(r'^(https?://)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(/\S*)?(\.(jpg|jpeg|png|gif))?$', img_url, re.I):
        flash("Invalid image URL format!", "error")
        return redirect(url_for("portfolio.form"))

    user = pcreate_user(
        username=username,
        firstname=name,
        lastname=lastname,
        email=email,
        phone=phone,
        school=school,
        college=college,
        skills=skills,
        about=about,
        instagram=instagram,
        github=github,
        profile_pic=img_url,
        template=selected_template 
    )
    pinsert_user(portfolio_collection, user)

    flash("Portfolio data saved successfully!", "success")
    return redirect(url_for("portfolio.view", username=username))"""



"""@portfolio.route("/view/<username>")
def view(username):
    user_data = pget_user(portfolio_collection, username)  
    if not user_data:
        flash("User data not found!", "error")
        return redirect(url_for("portfolio.form"))

    selected_template = user_data.get("template", "Design1.html") 

    return render_template(
        selected_template,  
        dname=user_data.get("firstname", ""),
        dlname=user_data.get("lastname", ""),
        dabout=user_data.get("about", ""),
        dsch=user_data.get("school", ""),
        dcol=user_data.get("college", ""),
        dph=user_data.get("phone", ""),
        demail=user_data.get("email", ""),
        ds1=user_data["skills"][0] if len(user_data["skills"]) > 0 else "",
        ds2=user_data["skills"][1] if len(user_data["skills"]) > 1 else "",
        ds3=user_data["skills"][2] if len(user_data["skills"]) > 2 else "",
        ds4=user_data["skills"][3] if len(user_data["skills"]) > 3 else "",
        insta=user_data.get("instagram", ""),
        git=user_data.get("github", ""),
        img=user_data.get("profile_pic", "deafult_pfp"),  
    )
"""
@portfolio.route("/view/<username>")
def view(username):
    user_data = pget_user(portfolio_collection, username)  
    if not user_data:
        flash("User data not found!", "error")
        return redirect(url_for("portfolio.form"))

    selected_template = user_data.get("template", "Design1.html") 

    return render_template(
        selected_template,  
        fname=user_data.get("firstname", ""),
        dlname=user_data.get("lastname", ""),
        dabout=user_data.get("about", ""),
        dsch=user_data.get("school", ""),
        dcol=user_data.get("college", ""),
        dph=user_data.get("phone", ""),
        demail=user_data.get("email", ""),
        ds1=user_data["skills"][0] if len(user_data["skills"]) > 0 else "",
        ds2=user_data["skills"][1] if len(user_data["skills"]) > 1 else "",
        ds3=user_data["skills"][2] if len(user_data["skills"]) > 2 else "",
        ds4=user_data["skills"][3] if len(user_data["skills"]) > 3 else "",
        insta=user_data.get("instagram", ""),
        git=user_data.get("github", ""),
        img=user_data.get("profile_pic", "default_pfp"),
        projects=user_data.get("projects", []),
        achievements=user_data.get("achievements", [])  
    )