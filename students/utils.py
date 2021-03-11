from students.models import Student

def promote_students(year):
    students = Student.objects.filter(last_promotion_date__year__lt=year, completed=False)
    for student in students:
        student.promote()
        print(student.get_full_name())
    print("Promotion done")