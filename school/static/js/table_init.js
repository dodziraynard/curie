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
                    return `<a href='/students/student-edit/${data}'>${data}</a>`
                }
            },
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
                    return `<a href='/staff/staff-edit/${data}'>${data}</a>`
                }
            },
            { data: 'surname' },
            { data: 'other_names' },
            { data: 'sms_number' },
            { data: 'gender' }
        ]
    });
});