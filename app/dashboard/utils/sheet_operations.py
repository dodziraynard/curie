from collections import defaultdict
from pathlib import Path

import pandas as pd

from accounts.models import User
from dashboard.models import Course, House, Klass, Student
from setup.models import Track

SHEET_SKIP_ROWS = 1
BASE_DIR = Path(__file__).resolve().parent.parent


def insert_students(url):
    errors = defaultdict(list)
    index = 0
    try:
        data = pd.read_excel(url,
                             sheet_name="students",
                             skiprows=SHEET_SKIP_ROWS,
                             dtype=str)
        df = pd.DataFrame(data)
        for index, row in df.iterrows():
            student_id = row['STUDENT_ID']
            surname = row['SURNAME']
            other_names = row['OTHER_NAMES']
            gender = row['GENDER']
            phone = row['SMS_NUMBER']
            class_id = row['CLASS_ID']
            electives = row['ELECTIVE_SUBJECT_IDS'].strip().split()
            house = row['HOUSE']
            track = row['TRACK']
            course_code = row['COURSE_CODE']
            gender = row['GENDER']
            father = row['FATHER']
            mother = row['MOTHER']
            dob = row['DOB']

            if not all([
                    student_id, surname, other_names, gender, phone, class_id,
                    electives, house, track, course_code
            ]):
                errors[index].append("Invalid entry.")
                continue

            if not phone.startswith("0") and len(phone) != 10:
                errors[index].append(
                    f"Invalid phone number: {phone}. Phone number must be a valid ten digit number starting with 0."
                )
                continue

            klass = Klass.objects.filter(class_id=class_id).first()
            if not klass:
                errors[index].append("Class does not exist: " + class_id)
                continue
            house = House.objects.filter(code=house).first()
            if not house:
                errors[index].append("House does not exist: " + house)
                continue
            track = Track.objects.filter(id=track).first()
            if not track:
                errors[index].append("Track does not exist: " + str(track))
                continue
            course = Course.objects.filter(code=course_code).first()
            if not course:
                errors[index].append("Course does not exist: " +
                                     str(course_code))
                continue
            try:
                dob = pd.to_datetime(dob)
            except ValueError:
                errors[index].append(
                    f"Invalid date of birth: {dob}. Date of birth must be in the format YYYY-MM-DD."
                )
                continue

            electives = klass.course.subjects.filter(code__in=electives,
                                                     is_elective=True)

            if electives.count() != len(electives):
                errors[index].append(
                    f"Student ID: {student_id}: Course  and Subject mismatch.")
                continue

            user, _ = User.objects.get_or_create(username=student_id)
            student, _ = Student.objects.get_or_create(student_id=student_id,
                                                       user=user)

            student.electives.set(electives)
            student.house = house
            student.course = course
            student.track = track
            student.dob = dob
            student.gender = gender
            student.father = father
            student.mother = mother
            student.klass = klass
            student.save()

            user.surname = surname
            user.other_names = other_names
            user.gender = gender
            user.dob = dob
            user.phone = phone
            user.save()

    except Exception as e:
        errors[index].append("An exception occurred: " + str(e))
    errors.default_factory = None
    return errors
