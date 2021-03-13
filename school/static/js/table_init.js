const loadStudentsIntoTable = () => {
    // Load all students into the table
    $('#student_table')?.DataTable({
        ajax: {
            url: "/ajax/students",
            dataSrc: 'students'
        },
        columns: [
            {
                data: 'student_id',
                render: function (data, type) {
                    return `<a class="badge badge-primary text text-white" href='/students/student-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/students/student-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteStudent('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'student_id' },
            { data: 'surname' },
            { data: 'other_names' },
            { data: 'sms_number' },
            { data: 'my_class' },
            { data: 'house' }
        ]
    });
}

const loadTeachersIntoTable = () => {
    // Load all teachers into the table
    $('#teacher_table')?.DataTable({
        ajax: {
            url: "/ajax/teachers",
            dataSrc: 'teachers'
        },
        columns: [
            {
                data: 'staff_id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/staff/staff-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/staff/staff-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteStaff('${data}')">
                                <i class="bi bi-trash"></i> 
                            </a> `
                }
            },
            {
                data: 'staff_id',
            },
            { data: 'surname' },
            { data: 'other_names' },
            { data: 'sms_number' },
            { data: 'gender' }
        ]
    });
}

const loadClassesIntoTable = () => {
    // Load all classes into the table
    $('#class_table')?.DataTable({
        ajax: {
            url: "/ajax/classes",
            dataSrc: 'classes'
        },
        columns: [
            {
                data: 'class_id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/students/class-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/students/class-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteClass('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'class_id' },
            { data: 'name' },
            { data: 'stream' },
            { data: 'form' },
            { data: 'course_name' },
            { data: 'class_teacher_name' }
        ]
    });
}

const loadSubjectsIntoTable = () => {
    // Load all subjects into the table
    $('#subject_table')?.DataTable({
        ajax: {
            url: "/ajax/subjects",
            dataSrc: 'subjects'
        },
        columns: [
            {
                data: 'subject_id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/students/subject-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/students/subject-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteSubject('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'subject_id' },
            { data: 'name' },
            { data: 'is_elective' },
            { data: 'student_count' },
        ]
    });
}


const loadCoursesIntoTable = () => {
    // Load all courses into the table
    $('#course_table')?.DataTable({
        ajax: {
            url: "/ajax/courses",
            dataSrc: 'courses'
        },
        columns: [
            {
                data: 'course_id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/students/course-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/students/course-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteCourse('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'course_id' },
            { data: 'name' },
            { data: 'subjects',
              render: (data, type) => {
                  let subjects = ""
                  for (let subject of data){
                    if (!subject.is_elective) continue
                    subjects += `<p class="text m-0">${subject.name} (${subject.subject_id})</p>`
                  }
                    return subjects
                }
            }
        ]
    });
}


const loadHouseMastersIntoTable = () => {
    // Load all courses into the table
    $('#house_master_table')?.DataTable({
        ajax: {
            url: "/ajax/house-masters",
            dataSrc: 'house_masters'
        },
        columns: [
            {
                data: 'house',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/students/house-master-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/students/house-master-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-danger text text-white" onClick="deleteHouseMaster('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'id' },
            { data: 'house' },
            { data: 'house_master'}
        ]
    });
}


const loadTeacherSubjectsIntoTable = () => {
    $('#teacher_subject_table')?.DataTable({
        ajax: {
            url: "/ajax/teachers-subjects",
            dataSrc: 'teachers_subjects'
        },
        columns: [
            {
                data: 'id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/staff/teachers-subjects-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <span class="badge badge-danger text text-white" onClick="deleteTeacherSubject('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'id' },
            { data: 'subject_name' },
            { data: 'class_name' },
            { data: 'teacher'}
        ]
    });
}


const loadGradingSystemsIntoTable = () => {
    $('#grading_system_table')?.DataTable({
        ajax: {
            url: "/ajax/grading-systems",
            dataSrc: 'grading_systems'
        },
        columns: [
            {
                data: 'id',
                render: (data, type) => {
                    return `<a class="badge badge-primary text text-white" href='/students/grading-system-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <span class="badge badge-danger text text-white" onClick="deleteGradingSytem('${data}')">
                                <i class="bi bi-trash"></i> 
                            </span> `
                }
            },
            { data: 'id' },
            { data: 'min_score' },
            { data: 'grade' },
            { data: 'remark'}
        ]
    });
}

// Load tables when page is done loading.
$(document).ready(() => {
    loadStudentsIntoTable()
    loadTeachersIntoTable()
    loadClassesIntoTable()
    loadSubjectsIntoTable()
    loadCoursesIntoTable()
    loadHouseMastersIntoTable()
    loadTeacherSubjectsIntoTable()

    $('#edit_record_table').DataTable();

    loadGradingSystemsIntoTable()
});

const deleteStudent = (student_id) => {
    document.querySelector('#input_student_id').value = student_id
    document.querySelector('#span_student_id').innerText = student_id
    $('#delete-student-modal').modal('show')
}

const deleteStaff = (staff_id) => {
    document.querySelector('#input_staff_id').value = staff_id
    document.querySelector('#span_staff_id').innerText = staff_id
    $('#delete-staff-modal').modal('show')
}

const deleteClass = (class_id) => {
    document.querySelector('#input_class_id').value = class_id
    document.querySelector('#span_class_id').innerText = class_id
    $('#delete-class-modal').modal('show')
}

const deleteSubject = (subject_id) => {
    document.querySelector('#input_subject_id').value = subject_id
    document.querySelector('#span_subject_id').innerText = subject_id
    $('#delete-subject-modal').modal('show')
}

const deleteCourse = (course_id) => {
    document.querySelector('#input_course_id').value = course_id
    document.querySelector('#span_course_id').innerText = course_id
    $('#delete-course-modal').modal('show')
}

const deleteHouseMaster = (house) => {
    document.querySelector('#input_house_master_id').value = house
    document.querySelector('#span_house_master_id').innerText = house
    $('#delete-house-master-modal').modal('show')
}

const deleteTeacherSubject = (id) => {
    document.querySelector('#input_id').value = id
    $('#delete-teacher-subject-modal').modal('show')
}

const deleteGradingSytem = (id) => {
    document.querySelector('#input_grading_system_id').value = id
    $('#delete-grading-system-modal').modal('show')
}
