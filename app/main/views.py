from flask import render_template, abort, flash, redirect,url_for
from flask_login import login_required,current_user
from . import main
from ..models import User,Agreement
from .. import db

from functools import cmp_to_key

from datetime import date,datetime,timedelta

def cmp(a,b):
    if a.timeday == b.timeday:
        return a.fromtime-b.fromtime
    else:
        if (a.timeday < b.timeday):
            return -1;
        else:
            return 1;

@main.route('/')
def index():
    agreements=Agreement.query.all()

    today = datetime.today()
    days = []
    for i in range(7):
        days.append((today.date(),str(today.date())))
        today += timedelta(1)
    dayL = days[0][1]
    dayR = days[6][1]

    #茶室
    chashi_agr = []
    for i in agreements:
        if i.enable == False:
            continue
        if i.room.name=='茶室' and i.timeday>=dayL and i.timeday<=dayR:
            chashi_agr.append(i)
    chashi_agr.sort(key=cmp_to_key(cmp))
    chashi_event = []
    for i in range(7):
        nowagr = []
        marks = []
        for j in chashi_agr:
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
        chashi_event.append(marks)

    #ok

    return render_template('index.html',agreements=agreements,event=chashi_event,days=days)
