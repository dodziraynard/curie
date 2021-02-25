$(document).ready(function () {
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
                            <span class="badge badge-primary text text-white" onClick="deleteStudent(${data})">
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

    // Load all teachers into the table
    $('#teacher_table')?.DataTable({
        ajax: {
            url: "/ajax/teachers",
            dataSrc: 'teachers'
        },
        columns: [
            {
                data: 'staff_id',
                render: function (data, type) {
                    return `<a class="badge badge-primary text text-white" href='/staff/staff-edit/${data}'>
                                <i class="bi bi-pencil"></i> 
                            </a>
                            <a class="badge badge-primary text text-white" href='/staff/staff-detail/${data}'>
                                <i class="bi bi-eye"></i> 
                            </a> 
                            <span class="badge badge-primary text text-white" onClick="deleteStaff(${data})">
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