
//OBSŁUGA KALENDARZY 

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        firstDay: 1,
        height: 650,
        initialView: 'dayGridMonth',
        events: [
            {
                title: 'Język polski',
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
        buttonText: {
            today: 'Dziś',
            month: 'Miesiąc',
            week: 'Tydzień',
            day: 'Dzień'
        }

    });
    calendar.render();
});


// OBSŁUGA OCEN

// Przykładowe dane uczniów dla poszczególnych klas
const classData = {
    class1: [
        { name: "Stanisław Gustaw", grades: { sprawdzian: [5], kartkowka: [4], pracaKlasowa: [3], zadanieDomowe: [4], inne: [] } },
        { name: "Anna Nowak", grades: { sprawdzian: [4], kartkowka: [5], pracaKlasowa: [4], zadanieDomowe: [3], inne: [] } },
    ],
    class2: [
        { name: "Piotr Wiśniewski", grades: { sprawdzian: [3], kartkowka: [4], pracaKlasowa: [5], zadanieDomowe: [4], inne: [] } },
        { name: "Ewa Zielińska", grades: { sprawdzian: [5], kartkowka: [5], pracaKlasowa: [4], zadanieDomowe: [3], inne: [] } },
    ]
};

// Elementy DOM
document.addEventListener('DOMContentLoaded', function () {
const classSelect = document.getElementById("classSelect");
const gradesContainer = document.getElementById("gradesContainer");
const studentsTableBody = document.getElementById("studentsTableBody");

// Funkcja do renderowania uczniów i ocen
function renderTable(classKey) {
    const students = classData[classKey];
    studentsTableBody.innerHTML = ""; // Wyczyszczenie tabeli

    students.forEach((student, index) => {
        const row = document.createElement("tr");
        
        // Imię i nazwisko
        const nameCell = document.createElement("td");
        nameCell.textContent = student.name;
        row.appendChild(nameCell);

        // Kategorie ocen
        ["sprawdzian", "kartkowka", "pracaKlasowa", "zadanieDomowe", "inne"].forEach(category => {
            const categoryCell = document.createElement("td");

            // Wyświetlanie ocen w kategorii
            categoryCell.textContent = student.grades[category].join(", ");
            row.appendChild(categoryCell);
        });

        studentsTableBody.appendChild(row);
    });

    gradesContainer.style.display = "block";
}

// Obsługa wyboru klasy
classSelect.addEventListener("change", (e) => {
    const selectedClass = e.target.value;
    renderTable(selectedClass);
});

});


