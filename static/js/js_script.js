
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        firstDay: 1,
        height: 650,
        initialView: 'dayGridMonth',
        events: [
            {
                title: 'Static Event',
                start: '2024-11-20',
                end: '2024-11-22',
                backgroundColor: '#800000',
                borderColor: '#800000'
            },
            {
                title: 'Static Event 2',
                start: '2024-11-25',
                end: '2024-11-30',
                backgroundColor: '#800000',
                borderColor: '#800000'
            }
        ],
        locale: 'pl',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },

    });
    calendar.render();
});
