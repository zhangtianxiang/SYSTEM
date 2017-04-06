from flask import render_template, redirect, request, url_for, flash
from .. import db
from .forms import AgreementForm
from . import commit
from flask_login import current_user
from ..models import Permission,Agreement,Commit,Room
from datetime import datetime,timedelta
@commit.route('/manage', methods=['GET', 'POST'])
def manage():
    form = AgreementForm()
    form.room.choices = [(r.id,r.name) for r in Room.query.all()]
    today = datetime.today()
    day = timedelta(1)
    days=[]
    for i in range(7):
        days.append((i+1,today.date()))
        today=today+day
    form.timeday.choices=days
    if current_user.can(Permission.ADD) and form.validate_on_submit():
        agreement=Agreement(org=form.org.data,
                            tel=form.tel.data,
                            number=form.number.data,
                            room_id=form.room.data,
                            timeday=days[form.timeday.data-1][1],
                            fromtime=form.fromtime.data+8,
                            totime=form.totime.data+8)
        db.session.add(agreement)
        db.session.commit()
        commit=Commit(agreement_id=agreement.id,user_id=current_user.id)
        db.session.add(commit)
        flash("增加借用成功！")
        return redirect(url_for('commit.manage'))
    commits=Commit.query.all()
    agrs=Agreement.query.all()
    return render_template('commit/manage.html',form=form,commits=commits,agrs=agrs)