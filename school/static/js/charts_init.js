var ctx = document.getElementById('myChart')?.getContext('2d');

// Setting up student teacher charts.
url = "/ajax/student-teacher-count"
fetch(url)
    .then(response => response.json())
    .then(res => {
        showStudentTeacherChart(res.students, res.teachers)
    }).catch(err => {
        showStudentTeacherChart(1, 1)
    })

const showStudentTeacherChart = (students, teachers) => {
    data = {
        labels: ['Students', 'Teachers'],
        datasets: [{
            data: [students, teachers],
            backgroundColor: [
                'indigo',
                'orange',
            ],
        }],
    };
    if (ctx)
        new Chart(ctx, {
            type: 'doughnut',
            data: data,
        });
}

