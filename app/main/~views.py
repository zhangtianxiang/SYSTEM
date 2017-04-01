from flask import render_template, abort, flash, redirect,url_for,session
from flask_login import login_required,current_user
from .forms import QueryForm
from . import main
from ..models import User,Agreement,Room
from .. import db
from datetime import date,datetime,timedelta
from functools import cmp_to_key

def cmp(a,b):
    if a.timeday == b.timeday:
        return a.fromtime-b.fromtime
    else:
        if (a.timeday < b.timeday):
            return -1;
        else:
            return 1;

@main.route('/', methods=['GET', 'POST'])
def index():
    agreements=Agreement.query.all()
    form = QueryForm()
    today = datetime.today()
    event = []
    formdays = []
    theday=today
    for i in range(7):
        formdays.append((i + 7, theday.date()))
        theday += timedelta(1)
    form.select.choices = [(r.id, r.name) for r in Room.query.all()] \
                          + formdays + [(14,"所有借用")]
    days = []
    for i in range(7):
        days.append((today.date(), str(today.date())))
        today += timedelta(1)
    dayL = days[0][1]
    dayR = days[6][1]

    if form.validate_on_submit():
        if form.select.data<=6:
            session['query'] = 'room'
            session['room']=form.select.choices[form.select.data-1][1]
            room_agr = []
            for i in agreements:
                if i.enable == False:
                    continue
                if i.room.name==form.select.choices[form.select.data-1][1] and i.timeday>=dayL and i.timeday<=dayR:
                    room_agr.append(i)
            room_agr.sort(key=cmp_to_key(cmp))

            for i in range(7):
                nowagr = []
                marks = []
                for j in room_agr:
                    if j.timeday == days[i][1]:
                        nowagr.append(j)
                if len(nowagr) == 0:
                    marks.append((False,22-8))
                else:
                    if nowagr[0].fromtime > 8:
                        marks.append((False,nowagr[0].fromtime-8))
                    marks.append((True,nowagr[0]))
                    for j in range(1,len(nowagr)):
                        if nowagr[j].fromtime > nowagr[j-1].totime:
                            marks.append((False,nowagr[j].fromtime-nowagr[j-1].totime))
                        marks.append((True,nowagr[j]))
                    if nowagr[len(nowagr)-1].totime < 22:
                        marks.append((False,22-nowagr[len(nowagr)-1].totime))
                event.append(marks)
        elif form.select.data<=13:
            session['query'] = 'date'
        else:
            session['query'] = 'all'
    return render_template('index.html',agreements=agreements,query=session.get('query'),form=form,room=session.get('room'),event=event,days=days)
