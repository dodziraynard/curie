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
                            <span class="badge badge-primary text text-white" onClick="deleteStudent('${data}')">
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
                            <span class="badge badge-primary text text-white" onClick="deleteStaff('${data}')">
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
                            <span class="badge badge-primary text text-white" onClick="deleteClass('${data}')">
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
                            <span class="badge badge-primary text text-white" onClick="deleteSubject('${data}')">
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

// Load tables when page is done loading.
$(document).ready(() => {
    loadStudentsIntoTable()
    loadTeachersIntoTable()
    loadClassesIntoTable()
    loadSubjectsIntoTable()
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