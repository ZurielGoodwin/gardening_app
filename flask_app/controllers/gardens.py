from datetime import date, datetime, timedelta
from flask_app.models.user import User
from flask_app.models.garden import Garden
from flask import request, render_template, redirect, session, flash
from flask_app import app



@app.route("/garden")
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }


    return render_template("dashboard.html", user=User.get_by_id(data), gardens=Garden.get_all())


#route to show add
@app.route("/garden/new")
def add_garden():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("add_to_garden.html")


# Create
@app.route('/garden/create',methods=['POST'])
def create_garden():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Garden.validate_garden(request.form):
        return redirect('/garden/new')
    data = {
        "crop": request.form["crop"],
        "variety": request.form["variety"],
        "date_planted": request.form["date_planted"],
        "days_to_harvest": request.form["days_to_harvest"],
        "notes": request.form["notes"],
        "user_id": session["user_id"]
    }
    Garden.create(data)
    return redirect('/garden')


# Read
@app.route('/garden/<int:id>')
def show_garden(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("display.html",garden=Garden.get_one(data),user=User.get_by_id(user_data))


# Update
@app.route("/garden/<int:id>/edit")
def edit_garden(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_garden.html", edit=Garden.get_one(data), user=User.get_by_id(user_data))


@app.route("/garden/edit", methods=["POST"])
def update_garden():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Garden.validate_garden(request.form):
        return redirect('/garden/new')
    data = {
        "crop": request.form["crop"],
        "variety": request.form["variety"],
        "date_planted": request.form["date_planted"],
        "days_to_harvest": request.form["days_to_harvest"],
        "notes": request.form["notes"],
        "id": session["user_id"],
    }
    Garden.update(data)
    return redirect('/garden')




# Delete
@app.route("/garden/<int:id>/delete")
def delete_garden(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Garden.delete(data)
    return redirect("/garden")



#Calculate Days to Harvest
@app.route ("/garden/date")
def calculate_harvest():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "date_planted": request.form["date_planted"],
        "days_to_harvest": request.form["days_to_harvest"],
    }
    date_planted = (Garden.date_planted)
    today_date = datetime.now()
    td = timedelta(days=Garden.days_to_harvest)
    harvest_date=(date_planted+td)
    time_left = (today_date-harvest_date)
    return(time_left)
