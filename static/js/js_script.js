
//OBSŁUGA KALENDARZY 
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var classSelect = document.getElementById('class-select');
    var replacementForm = document.getElementById('replacementForm');
    var classSelectReplacement = document.getElementById('class-select-replacement');
    

    function renderCalendar(id_class) {
        if (window.currentCalendar) {
            window.currentCalendar.destroy();
        }
    
        fetch('/get_lessons', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ classId: id_class })
        })
            .then(response => response.json())
            .then(events => {
                window.currentCalendar = new FullCalendar.Calendar(calendarEl, {
                    firstDay: 1,
                    height: 650,
                    initialView: 'dayGridMonth',
                    slotMinTime: '08:00:00',
                    slotMaxTime: '17:00:00',
                    events: events,
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
                    eventClick: function (info) {
                        const dialog = document.getElementById('eventDialog');
                        const dialogTitle = dialog.querySelector('.dialog-title');
                        const dialogDescription = dialog.querySelector('.dialog-description');
                        const dialogDetails = dialog.querySelector('.dialog-details');
    
                        const startDate = new Date(info.event.start);
                        const endDate = new Date(info.event.end);
    
                        const date = startDate.toLocaleDateString('pl-PL', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            weekday: 'long'
                        });
    
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
    
                window.currentCalendar.render();
            })
            .catch(error => console.error('Błąd pobierania lekcji:', error));
    }
    

    // Obsługa formularza zastępstw
    replacementForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const selectedClass = classSelectReplacement.value;
        const subject = document.getElementById('subject').value;
        const teacher = document.getElementById('teacher').value;
        const date = document.getElementById('date').value;
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;
        const room = document.getElementById('room').value;

        if (!calendars[selectedClass]) {
            calendars[selectedClass] = [];
        }

        calendars[selectedClass].push({
            title: `${subject} (Zastępstwo)`,
            start: `${date}T${startTime}`,
            end: `${date}T${endTime}`,
            backgroundColor: '#FF0000',
            borderColor: '#FF0000',
            description: `Zastępstwo w sali ${room}.`,
            teacher: teacher,
            room: room
        });

        if (classSelect && classSelect.value === selectedClass) {
            renderCalendar(selectedClass); // Odśwież widok kalendarza, jeśli wybrana klasa jest aktywna
        }

        replacementForm.reset(); // Wyczyść formularz
        alert('Zastępstwo zostało dodane!');
    });
});






/////////// wyswietlanie ocen


// Elementy DOM
document.addEventListener('DOMContentLoaded', function () {
    const classSelect = document.getElementById("classSelect");
    const gradesContainer = document.getElementById("gradesContainer");
    const studentsTableBody = document.getElementById("studentsTableBody");

    let activeTooltip = null; // Zmienna przechowująca aktywny tooltip

    // Funkcja do renderowania uczniów i ocen
    function renderTable(classKey) {
        const students = classData[classKey];
        studentsTableBody.innerHTML = ""; // Wyczyszczenie tabeli

        students.forEach(student => {
            const row = document.createElement("tr");

            // Imię i nazwisko
            const nameCell = document.createElement("td");
            nameCell.textContent = student.name;
            row.appendChild(nameCell);

            // Kategorie ocen
            ["sprawdzian", "kartkowka", "pracaKlasowa", "zadanieDomowe", "inne"].forEach(category => {
                const categoryCell = document.createElement("td");

                // Wyświetlanie ocen w kategorii
                student.grades[category].forEach(grade => {
                    const gradeBox = document.createElement("div");
                    gradeBox.classList.add("grade-box");
                    gradeBox.textContent = grade;

                    // Tworzenie tooltipa
                    const tooltip = document.createElement("div");
                    tooltip.classList.add("tooltip");
                    tooltip.textContent = `Informacje o ocenie: ${grade}`;

                    gradeBox.appendChild(tooltip);

                    // Obsługa kliknięcia na ocenę
                    gradeBox.addEventListener("click", (e) => {
                        e.stopPropagation(); // Zatrzymanie propagacji, aby kliknięcie poza tooltipem działało poprawnie
                        
                        // Ukryj poprzedni tooltip, jeśli istnieje
                        if (activeTooltip && activeTooltip !== tooltip) {
                            activeTooltip.classList.remove("show");
                        }

                        // Przełącz wyświetlanie obecnego tooltipa
                        tooltip.classList.toggle("show");

                        // Zaktualizuj aktywny tooltip
                        activeTooltip = tooltip.classList.contains("show") ? tooltip : null;
                    });

                    categoryCell.appendChild(gradeBox);
                });

                row.appendChild(categoryCell);
            });

            studentsTableBody.appendChild(row);
        });

        gradesContainer.style.display = "block";
    }

    // Ukrywanie tooltipa po kliknięciu gdzieś indziej
    document.addEventListener("click", () => {
        if (activeTooltip) {
            activeTooltip.classList.remove("show");
            activeTooltip = null;
        }
    });

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

window.addEventListener('DOMContentLoaded', () => {
    const editModeBtn = document.getElementById('edit-mode-btn');
    const statusButtons = document.querySelectorAll('.status-btn');
    const table = document.querySelector('table');
    let isEditMode = false;
    let selectedStatus = '';
    const attendanceData = {};

    // Toggle edit mode
    editModeBtn.addEventListener('click', () => {
        isEditMode = !isEditMode;
        editModeBtn.textContent = isEditMode ? 'Zakończ edycję' : 'Edycja';
        document.querySelectorAll('.editable').forEach(cell => {
            if (isEditMode) {
                cell.setAttribute('contenteditable', 'true');
                cell.style.pointerEvents = 'auto'; // Włączenie kliknięcia
                cell.style.backgroundColor = ''; // Przywrócenie tła komórek
            } else {
                cell.removeAttribute('contenteditable');
                cell.style.pointerEvents = 'none'; // Zablokowanie kliknięcia
                cell.style.backgroundColor = '#f4f4f4'; // Tło dla komórek tylko do odczytu
            }
        });
    });

    // Handle status selection and visual feedback in legend
    statusButtons.forEach(button => {
        button.addEventListener('click', () => {
            statusButtons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            selectedStatus = button.dataset.status;
        });
    });

    // Handle cell click for changing status
    table.addEventListener('click', (event) => {
        const cell = event.target;
        if (cell.classList.contains('editable') && isEditMode) {
            if (selectedStatus) {
                cell.textContent = selectedStatus;
                switch (selectedStatus) {
                    case 'O':
                        cell.style.backgroundColor = 'green';
                        break;
                    case '-':
                        cell.style.backgroundColor = 'yellow';
                        break;
                    case 'U':
                        cell.style.backgroundColor = 'red';
                        break;
                    case 'S':
                        cell.style.backgroundColor = 'blue';
                        break;
                    default:
                        cell.style.backgroundColor = '';
                }
            }
        }
    });

    // Handle cell selection for mass editing
    table.addEventListener('click', (event) => {
        const cell = event.target;
        if (cell.classList.contains('editable') && isEditMode) {
            cell.classList.toggle('selected');
        }
    });
});
//JULIA-FREKFENCJA

let editMode = false;
let selectedStatus = "O";

// Tryb edycji
document.getElementById("edit-mode-btn").addEventListener("click", () => {
    editMode = !editMode;
    const cells = document.querySelectorAll("tbody td");
    cells.forEach(cell => {
        cell.classList.toggle("disabled", !editMode);
    });

    // Zmieniamy kolor przycisku "Edycja"
    const editButton = document.getElementById("edit-mode-btn");
    editButton.classList.toggle("active", editMode);
});

// Zaznaczanie statusu z legendy
const statusButtons = document.querySelectorAll(".status-btn");
statusButtons.forEach(button => {
    button.addEventListener("click", () => {
        statusButtons.forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");
        selectedStatus = button.getAttribute("data-status");
    });
});

// Wypełnianie komórek tabeli
document.querySelectorAll("tbody td").forEach(cell => {
    cell.addEventListener("click", () => {
        if (editMode && cell.classList.contains("editable")) {
            cell.textContent = selectedStatus;
        }
    });
});

//KONIEC FREKFENCJI