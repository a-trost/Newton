import requests
from variables import quickschools_apikey
import json
# from brain.models import StudentRoster

def get_students():
    # 344832: 744737 ==============================
# Couldn't find: 744738 ==============================
# Couldn't find: 742824
    # url = 'https://api.quickschools.com/sms/v1/students?itemsPerPage=500'
    # url = 'https://api.quickschools.com/sms/v1/homerooms'
    # url = 'https://api.quickschools.com/sms/v1/students?classId=580289&itemsPerPage=50'
    # url = 'https://api.quickschools.com/sms/v1/students?classId=580289'
    # url = 'https://api.quickschools.com/sms/v1/homerooms/201486'
    url = 'https://api.quickschools.com/sms/v1/students/744738'

    # url = 'https://api.quickschools.com/sms/v1/attendance?beginDate=2017-08-28'


    params = {'apiKey': quickschools_apikey,}
    results = requests.get(url, params=params)
    results = results.json()
    print(results)
    return results
# {'homeroomTeacherId': '111894', 'homeroomTeacherName': 'Alex Trost', 'classId': '580289', 'id': '201482', 'abbreviation': 'Alex Trost', 'name': 'Alex Trost'},

from django.db.models import Q

def find_student_by_name(query_name):
    qs = StudentRoster.objects.all()
    for term in query_name.split():
        qs = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
    return qs

def update_student_ids(student_json_file):
    # dataReader = json.load(student_json_file)
    # print("Got Datareader!")
    students = student_json_file['list']
    for student in students:
        full_name = student['fullName']
        quickschools_id = student['id']
        student = find_student_by_name(full_name).first()
        if student:
            print(student)
        # print("{}, {}".format(full_name, quickschools_id))



# P: Present
# A: Absent
# T: Tardy
# EA: Excused Absense
# ET: Excused Tardy

student_json_file = get_students()
# update_student_ids(student_json_file)