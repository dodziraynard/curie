var ctx = document.getElementById('myChart').getContext('2d');

data = {
    labels: ['Students', 'Teachers'],
    datasets: [{
        data: [100, 20],
        backgroundColor: [
            'indigo',
            'orange',
        ],
    }],
};

var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
});
