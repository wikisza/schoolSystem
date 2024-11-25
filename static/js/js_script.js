
//OBSŁUGA KALENDARZY 

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        firstDay: 1,
        height: 650,
        initialView: 'dayGridMonth',
        slotMinTime: '08:00:00', // Minimalna godzina zajec
        slotMaxTime: '17:00:00', // Maksymalna godzina zajec
        events: [
            {
                title: 'Język polski',
                start: '2024-11-20T08:00:00',
                end: '2024-11-20T10:00:00',
                backgroundColor: '#800000',
                borderColor: '#800000',
                description: 'Zajęcia w sali 7A.',
                teacher: 'Jan Kowalski',
                room: '7A'
            },
            {
                title: 'Static Event 2',
                start: '2024-11-25T10:00:00',
                end: '2024-11-25T13:00:00',
                backgroundColor: '#800000',
                borderColor: '#800000',
                description: 'Zajęcia w sali 102.',
                teacher: 'Anna Nowak',
                room: '102'
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
        },
        // Zawartosc wyskakujacego okienka po kliknieciu na zajęcie w planie zajęć
        eventClick: function (info) {
            const dialog = document.getElementById('eventDialog');
            const dialogTitle = dialog.querySelector('.dialog-title');
            const dialogDescription = dialog.querySelector('.dialog-description');
            const dialogDetails = dialog.querySelector('.dialog-details');
            
            // Pobieranie daty i godziny z wydarzenia
            const startDate = new Date(info.event.start);
            const endDate = new Date(info.event.end);

            // Formatowanie daty
            const date = startDate.toLocaleDateString('pl-PL', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                weekday: 'long'
            });

            // Formatowanie godzin
            const startTime = startDate.toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' });
            const endTime = endDate.toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' });

            dialogTitle.textContent = info.event.title;
            dialogDescription.textContent = info.event.extendedProps.description;

            dialogDetails.innerHTML = `
            <p><strong>Dzień:</strong> ${date}</p>
            <p><strong>Godzina:</strong> ${startTime} - ${endTime}</p>
            <p><strong>Nauczyciel:</strong> ${info.event.extendedProps.teacher}</p>
            <p><strong>Sala:</strong> ${info.event.extendedProps.room}</p>
            `;

            dialog.showModal();
        }
    });
    calendar.render();
});


/////////// wyswietlanie ocen

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

///////////////// dodawanie oceny

// Elementy DOM
document.addEventListener('DOMContentLoaded', function () {
    const classSelect = document.getElementById("classSelect");
    const tableAddGrade = document.getElementById("tableAddGrade");
    const bodyAddGrade = document.getElementById("bodyAddGrade");
    const headAddGrade = document.getElementById("headAddGrade");
    const openDialog = document.getElementById("openDialog");

    function renderTable2(classKey) {
        const students = classData[classKey];
        bodyAddGrade.innerHTML = ""; // Wyczyszczenie tabeli

        students.forEach((student, index) => {
            const row = document.createElement("tr");

            // Imię i nazwisko
            const nameCell = document.createElement("td");
            nameCell.textContent = student.name;
            row.appendChild(nameCell);

            bodyAddGrade.appendChild(row);
        });

        tableAddGrade.style.display = "block";
        openDialog.style.display = "block";
    }

    // Obsługa wyboru klasy
    classSelect.addEventListener("change", (e) => {
        const selectedClass = e.target.value;
        renderTable2(selectedClass);
    });


    ///////////////////////// OBSŁUGA DIALOGU
    const openDialogButton = document.getElementById('openDialog');
    const gradeDialog = document.getElementById('gradeDialog');
    const confirmGrades = document.getElementById("confirmGrades");

    // Otwieranie dialogu
    openDialogButton.addEventListener('click', () => {
        gradeDialog.showModal();
    });

    // Obsługa przycisków w dialogu
    const cancelButton = gradeDialog.querySelector('.cancel');
    const confirmButton = gradeDialog.querySelector('.confirm');

    cancelButton.addEventListener('click', () => {
        gradeDialog.close();
    });

    gradeDialog.addEventListener('close', () => {
        const selectedType = gradeDialog.returnValue; // Zwraca 'confirm' jeśli kliknięto potwierdź
        console.log("Dialog zamknięty:", selectedType);
    });

    gradeDialog.addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedType = gradeDialog.querySelector('input[name="gradeType"]:checked').value;
        console.log("Wybrano typ oceny:", selectedType);

        gradeDialog.close(selectedType);
    });

    confirmButton.addEventListener('click', (e) => {
        e.preventDefault(); // Zapobiegamy wysyłaniu formularza

        // Pobranie danych z dialogu
        const selectedCategory = gradeDialog.querySelector('#gradesTypes').value;
        const gradeDescription = gradeDialog.querySelector('input[type="text"]').value;

        // Dodanie nowej kolumny do tabeli
        const category = document.createElement("th");
        category.textContent = `${selectedCategory}`;
        headAddGrade.querySelector("tr").appendChild(category);

        // Dodanie pustych komórek dla każdego ucznia
        bodyAddGrade.querySelectorAll("tr").forEach(row => {
            const newCell = document.createElement("td");

            const input = document.createElement("input");
            input.type = "text";
            newCell.appendChild(input);
            row.appendChild(newCell);
            gradeDialog.close();

            confirmGrades.style.display = "block";
        });

    });
    

});


