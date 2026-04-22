#Список мест работы с указанием общего стажа
#Поля ввода: наименование места работы, срок работы в месяцах
#БД: company, term

import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask('Employers information', template_folder=os.path.join(base_dir, 'templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(300))
    term = db.Column(db.Integer, nullable=False)
    role_in_company = db.Column(db.String(300))
    number_of_company = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Person: {self.id}. Workplace: {self.company}'

@app.route('/')
def main():
    experiences = WorkExperience.query.all()
    total_months = sum(exp.term for exp in experiences)
    years = total_months // 12
    months = total_months % 12
    total_time_str = f"{years} г. {months} мес." if years > 0 else f"{months} мес."

    return render_template('lab9.html', experiences=experiences, total_time=total_time_str)

@app.route('/add', methods=['POST'])
def add_experience():
    if request.is_json:
        data = request.json
        company = data.get('company')
        term = data.get('term')
        role = data.get('role_in_company')
        number = data.get('number_of_company')
    else:
        company = request.form.get('company')
        term = request.form.get('term')
        role = request.form.get('role_in_company')
        number = request.form.get('number_of_company')

    if company and term and number:
        new_place = WorkExperience(
                company=company, 
                term=int(term), 
                role_in_company=role, 
                number_of_company=int(number)
            )
        db.session.add(new_place)
        db.session.commit()

    return redirect(url_for('main'))

@app.route('/clear', methods=['POST'])
def clear_experiences():
    try:
        db.session.query(WorkExperience).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('main'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)