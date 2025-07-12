// PIE CHART - CATEGORY DISTRIBUTION
const ctx1 = document.getElementById('categoryChart').getContext('2d');
new Chart(ctx1, {
    type: 'pie',
    data: {
        labels: Object.keys(categoryData),
        datasets: [{
            label: 'Category Count',
            data: Object.values(categoryData),
            backgroundColor: [
                '#1abc9c', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', '#e67e22'
            ],
            borderColor: '#2c2c2c',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#fff',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

// BAR CHART - PRIORITY DISTRIBUTION
const ctx2 = document.getElementById('priorityChart').getContext('2d');
new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: Object.keys(priorityData),
        datasets: [{
            label: 'Tasks',
            data: Object.values(priorityData),
            backgroundColor: ['#f39c12', '#e74c3c', '#2ecc71'],
            borderRadius: 6,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                ticks: { color: '#fff' },
                grid: { color: '#333' }
            },
            x: {
                ticks: { color: '#fff' },
                grid: { color: '#333' }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: '#222',
                titleColor: '#fff',
                bodyColor: '#1db954'
            }
        }
    }
});
