from flask import render_template, abort, flash, redirect,url_for,session
from flask_login import login_required,current_user
# from .forms import QueryForm
from . import main
from ..models import User,Agreement,Room
from .. import db
from datetime import date,datetime,timedelta
from functools import cmp_to_key

#整个‘/’页面是给没有管理权限的人提供的，不提供借用单的展示，以防止泄露个人信息。
#建议新加‘/magage’页面给管理员进行借用单的查询与删除

@main.route('/', methods=['GET', 'POST'])
def index():
    all_agr = Agreement.query.all()
    all_room = Room.query.all()
    all_day = []
    now_day = datetime.today()
    for i in range(7):
        all_day.append((now_day.date(), str(now_day.date())))
        now_day += timedelta(1)
    dayL = all_day[0][1]
    dayR = all_day[6][1]
    #下面实现每个房间借用情况查询
    all_room_mark = []
    for now_room in all_room:
        now_room_mark = []
        for i in range(7):
            now_day_agr = Agreement.query.filter_by(room=now_room,timeday=all_day[i][1]).order_by(Agreement.fromtime).all()
            now_day_mark = []
            if len(now_day_agr) == 0:
                now_day_mark.append((False,22-8))
            else:
                if now_day_agr[0].fromtime > 8:
                    now_day_mark.append((False,now_day_agr[0].fromtime-8))
                now_day_mark.append((True,now_day_agr[0]))
                for j in range(1,len(now_day_agr)):
                    if now_day_agr[j].fromtime > now_day_agr[j-1].totime:
                        now_day_mark.append((False,now_day_agr[j].fromtime-now_day_agr[j-1].totime))
                    now_day_mark.append((True,now_day_agr[j]))
                if now_day_agr[len(now_day_agr)-1].totime < 22:
                    now_day_mark.append((False,22-now_day_agr[len(now_day_agr)-1].totime))
            now_room_mark.append(now_day_mark)
        all_room_mark.append((now_room,now_room_mark))
    return render_template('index.html',marks=all_room_mark,days=all_day,agrs=all_agr)