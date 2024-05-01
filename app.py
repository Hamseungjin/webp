from bson import ObjectId
from flask import Flask,render_template
from pymongo import MongoClient


app = Flask(__name__)

client=MongoClient('localhost',27017)
db=client['studentDB']
collect=db.grades

gradesData=[
    {"studentID":"2018001",'Grade':80},
    {"studentID":"2018002",'Grade':70},
    {"studentID":"2018003",'Grade':65},
    {"studentID":"2018004",'Grade':85},
    {"studentID":"2018005",'Grade':90},
    {"studentID":"2018006",'Grade':58},
    {"studentID":"2018007",'Grade':76},
    {"studentID":"2018008",'Grade':95},
    {"studentID":"2018009",'Grade':88},
    {"studentID":"2018010",'Grade':63},
]

collect.insert_many(gradesData)

@app.route('/students')
def students():
    students=collect.find()
    return render_template('home.html',data=students)

@app.route('/students/grade_detail/<id>')
def grade_detail(id):
    object_id = ObjectId(id)
    student = collect.find_one({'_id': object_id})
    if not student:
        return 'student Not found',404

    score=student['Grade']
    grade_letter = getGradeLetter(score)

    # add new key "Letter" and assign the letter value
    setUpdated = {"$set": {"letter": grade_letter}}

    # update_one based on key_id
    collect.update_one({'_id': student["_id"]}, setUpdated, upsert=False)
    student = collect.find_one({'_id': object_id})
    return render_template('grade_detail.html', student=student)
def getGradeLetter(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


if __name__ == '__main__':
    app.run()