from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
import datetime as dt

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")


views = Blueprint('views',__name__) # see flask documentation.


def make_image_int(timestamp, val):
    plt.clf()
    plt.tight_layout()
    plt.grid(True)
    plt.plot(timestamp, val)
    plt.ylabel("Values")
    plt.xlabel("Time Stamp")
    plt.xticks(rotation=337.5,ha='left')
    plt.subplots_adjust(bottom=0.20,right=0.80)
    plt.savefig('website_code/static/output.jpg')
    plt.close()


def make_image_time(timestamp, val):
    plt.clf()
    plt.tight_layout()
    plt.grid(True)
    plt.plot(timestamp, val)
    plt.ylabel("Hours")
    plt.xlabel("Time Stamp")
    plt.xticks(rotation=337.5,ha='left')
    plt.subplots_adjust(bottom=0.20,right=0.80)
    plt.savefig('website_code/static/output.jpg')
    plt.close()

def make_image_mcq(fre):
    plt.clf()
    plt.tight_layout()
    d = dict()
    for a in fre:
        if a not in d:
            d[a]=0
        d[a]+=1
    sort_fre=[x for x in sorted(d.items(), key=lambda x:x[1])]
    plt.hist(fre)
    plt.yticks([x[1] for x in sort_fre])
    plt.ylabel("Frequency")
    plt.xlabel("Options")
    plt.xticks(rotation=337.5,ha='left')
    plt.subplots_adjust(bottom=0.20,right=0.80)
    plt.savefig('website_code/static/output.jpg')
    plt.close()


@views.route("/",methods=["GET","POST"])  # this '@views is the variable 'views' not the one inside the Blueprint.
@login_required
def home():        # we have created a blueprint. Now we need to register it in __init__.py file.
    if request.method=="GET":
        trackers = Tracker.query.filter(Tracker.user_id == current_user.user_id).all()
        last_track = []
        for tracker in trackers:
            tracker_datetime = Log.query.filter(Log.tracker_id==tracker.tracker_id).order_by(Log.time.desc()).first()
            if tracker_datetime:
                last_track.append(dt.datetime.strptime(tracker_datetime.time,"%Y-%m-%dT%H:%M").date().strftime("%b/%d/%Y"))
            else:
                last_track.append(None)
        return render_template("home.html", user=current_user, tracker=trackers, last_track = last_track)


@views.route("/tracker/<action>",methods=["GET","POST"])
@login_required
def create_tracker(action):
    if request.method=="POST":
        if action=="create":
            name = request.form['name']
            description = request.form['desc']
            tracker_type = request.form['tracker_type']
            setting = request.form['setting']

            tracker = Tracker.query.filter(Tracker.name == name).first()
            if tracker != None:
                flash("Tracker already exist! user Another name",category="error")
            else:
                new_tracker = Tracker(name=name,description=description,type=tracker_type,setting=setting,user_id=current_user.user_id)
                db.session.add(new_tracker)
                db.session.commit()

                return redirect(url_for('views.home'))

    return render_template('create_tracker.html', user=current_user)


@views.route("/tracker/<tracker_id>/<action>",methods=["GET","POST"])
@login_required
def modify_tracker(tracker_id,action):
    if request.method=="GET":
         if action=='add':
             tracker = Tracker.query.filter(Tracker.tracker_id==tracker_id).first()
             current_time = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")
             if tracker.setting:
                 tracker.setting = tracker.setting.split(",")

             return render_template('add_log.html', user=current_user,tracker=tracker,current_time=current_time)

         elif action=="delete":
             tracker = Tracker.query.filter(Tracker.tracker_id == tracker_id).first()
             logs = Log.query.filter(Log.tracker_id==tracker_id).all()
             for log in logs:
                 db.session.delete(log)
             db.session.delete(tracker)
             db.session.commit()

             return redirect(url_for('views.home'))

         elif action=="edit":
             tracker = Tracker.query.filter(Tracker.tracker_id==tracker_id).first()

             return render_template('edit_tracker.html', user=current_user, tracker=tracker)

         elif action=="details":
             tracker = Tracker.query.filter(Tracker.tracker_id == tracker_id).first()
             logs = Log.query.filter(Log.tracker_id==tracker_id).order_by(Log.time.asc()).all()
             if tracker.type=="numerical":
                 val = [float(log.log_track) for log in logs]
                 timestamp = [log.time for log in logs]

                 make_image_int(timestamp,val)

             elif tracker.type=="multiple_choice":
                 val = [log.log_track for log in logs]
                 make_image_mcq(val)

             elif tracker.type=="time_duration":
                 val = [float(log.log_track.replace(":",".")) for log in logs]
                 timestamp = [log.time for log in logs]
                 make_image_time(timestamp,val)


         return render_template('details_tracker.html', user=current_user, log=logs, tracker=tracker, plot=url_for('static', filename="output.jpg"))




    else:
        if action=='add':
            time = request.form['time']
            val = request.form['val']
            note = request.form['note']

            new_log = Log(tracker_id=tracker_id, log_track=val, note=note, time=time)
            db.session.add(new_log)
            db.session.commit()

            return redirect(url_for('views.home'))

        elif action == 'edit':
            name = request.form['name']
            description = request.form['desc']

            exist_tracker = Tracker.query.filter(Tracker.name == name).first()
            if exist_tracker != None and exist_tracker.tracker_id != tracker_id:
                flash("Tracker already exist! user Another name", category="error")
                tracker = Tracker.query.filter(Tracker.tracker_id == tracker_id).first()
                return render_template('edit_tracker.html', user=current_user, tracker=tracker)

            else:
                change_tracker = Tracker.query.filter(Tracker.tracker_id==tracker_id).first()
                change_tracker.name = name
                change_tracker.description = description

                db.session.commit()

                return redirect(url_for('views.home'))


@views.route("/log/<tracker_id>/<log_id>/<action>", methods=["GET", "POST"])
@login_required
def modify_logs(tracker_id,log_id,action):
    if request.method=="GET":
        if action=="delete":
            log = Log.query.filter(Log.log_id==log_id).delete()
            db.session.commit()

            return redirect(url_for("views.modify_tracker", tracker_id=tracker_id, action='details'))

        elif action == "edit":
            log_data = Log.query.filter(Log.log_id == log_id).first()
            tracker = Tracker.query.filter(Tracker.tracker_id == tracker_id).first()
            if tracker.setting:
                tracker.setting = tracker.setting.split(",")

            return render_template("edit_log.html", user=current_user,tracker=tracker, log_data=log_data)

    else:
        if action=="edit":
            time = request.form['time']
            value = request.form['val']
            note = request.form['note']

            log_data = Log.query.filter(Log.log_id == log_id).first()

            log_data.time = time
            log_data.log_track = value
            log_data.note = note

            db.session.commit()

            return redirect(url_for("views.modify_tracker", tracker_id=tracker_id, action='details'))

