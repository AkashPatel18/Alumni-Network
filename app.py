from flask import Flask, render_template, request, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///jobs.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Jobs(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    job_name=db.Column(db.String(20),nullable=False)
    company_name = db.Column(db.String(20),nullable = False)
    stipend = db.Column(db.Integer)
    location = db.Column(db.String(20))
    apply_link = db.Column(db.String(200))

    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/')
def Home():
    # job = Jobs(job_name="job_name", company_name="company_name",
    #            stipend="stipend", location="location", apply_link="apply_link")
    # db.session.add(job)
    # db.session.commit()
    if request.method=="POST":
        job_name = request.form['job_name']
        company_name = request.form['company_name']
        stipend = request.form['stipend']
        location=request.form['location']
        apply_link = request.form['apply_link']

        job = Jobs(job_name=job_name,company_name=company_name, stipend=stipend, location=location, apply_link=apply_link)
        db.session.add(job)
        db.session.commit()

    alljobs = Jobs.query.all()
    return render_template("index.html",alljobs = alljobs)


@app.route('/postjob', methods=['GET', 'POST'])
def postjob():
    if request.method == "POST":
        job_name = request.form['job_name']
        company_name = request.form['company_name']
        stipend = request.form['stipend']
        location = request.form['location']
        apply_link = request.form['apply_link']

        job = Jobs(job_name=job_name, company_name=company_name,
                   stipend=stipend, location=location, apply_link=apply_link)
        db.session.add(job)
        db.session.commit()
    return redirect("/saved")



@app.route('/saved',methods=['GET','POST'])
def saved():
    return render_template("thanks.html")



if __name__=="__main__":
    app.run(debug=True)
