$(document).ready(function () {
    $('#student_table')?.DataTable({
        ajax: {
            url: "/ajax/students",
            dataSrc: 'students'
        },
        columns: [
            {
                data: 'student_id',
                render: function (data, type) {
                    return `<a href='/students/${data}'>${data}</a>`
                }
            },
            { data: 'surname' },
            { data: 'other_names' },
            { data: 'sms_number' },
            { data: 'my_class' },
            { data: 'house' }
        ]
    });
});