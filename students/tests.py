from django.test import TestCase
from pathlib import Path
from sheet_engine.functions import (insert_subjects,
                                    insert_courses,
                                    insert_staff,
                                    insert_classes,
                                    insert_students,
                                    insert_house_masters,
                                    generate_subject_staff_combinations,
                                    insert_subject_staff_combination,
                                    generate_record_sheet,
                                    insert_records,
                                    generate_teacher_remark_sheet,
                                    insert_teacher_remarks,
                                    generate_house_master_remark_sheet,
                                    insert_house_master_remarks)


class StudentsTest(TestCase):
    def setUp(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        
    def insert_subjects_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/subjects.xlsx"
        self.assertEqual(insert_subjects(url), True)

    def insert_courses_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/courses.xlsx"
        self.assertEqual(insert_courses(url), True)

    def insert_staff_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/staff.xlsx"
        self.assertEqual(insert_staff(url), True)

    def insert_classes_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/classes.xlsx"
        self.assertEqual(insert_classes(url), True)

    def insert_students_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/students.xlsx"
        self.assertEqual(insert_students(url), True)

    def insert_subject_staff_combination_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_subject_staff_combinations.xlsx"
        self.assertEqual(insert_subject_staff_combination(url), True)

    def insert_records_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_record_sheet.xlsx"
        self.assertEqual(insert_records(url), True)

    def insert_teacher_remarks_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_teacher_remark_sheet.xlsx"
        self.assertEqual(insert_teacher_remarks(url, "GA11"), True)

    def insert_house_master_remarks(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/house_master_remarks.xlsx"
        self.assertEqual(insert_house_master_remarks(url), True)

    def test_data_insertion_from_sheet(self):
        self.insert_subjects_from_sheet()
        self.insert_courses_from_sheet()
        self.insert_staff_from_sheet()
        self.insert_classes_from_sheet()
        self.insert_students_from_sheet()
        self.insert_subject_staff_combination_from_sheet()
        self.insert_records_from_sheet()
        self.insert_teacher_remarks_from_sheet()
        self.insert_house_master_remarks()