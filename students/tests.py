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

    def test_insert_subjects_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/subjects.xlsx"
        self.assertTrue(insert_subjects(url))

    def test_insert_courses_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/courses.xlsx"
        self.assertTrue(insert_courses(url))

    def test_insert_staff_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/staff.xlsx"
        self.assertTrue(insert_staff(url))

    def test_insert_classes_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/classes.xlsx"
        self.assertTrue(insert_classes(url))

    def test_insert_students_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/students.xlsx"
        self.assertTrue(insert_students(url))

    def test_insert_subject_staff_combination_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_subject_staff_combinations.xlsx"
        self.assertTrue(insert_subject_staff_combination(url))

    def test_insert_records_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_record_sheet.xlsx"
        self.assertTrue(insert_records(url))

    def test_insert_teacher_remarks_from_sheet(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/generated_teacher_remark_sheet.xlsx"
        self.assertTrue(insert_teacher_remarks(url, "GA11"))

    def test_insert_house_master_remarks(self):
        url = self.BASE_DIR / "sheet_engine/test_sheets/house_master_remarks.xlsx"
        self.assertTrue(insert_house_master_remarks(url))
