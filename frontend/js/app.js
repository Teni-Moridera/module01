const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const statusEl = document.getElementById("status");
const statsEl = document.getElementById("stats");
const ratingTableBody = document.querySelector("#ratingTable tbody");

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#b91c1c" : "#166534";
}

function renderStats(stats) {
  statsEl.innerHTML = "";
  const entries = [
    ["Студентов", stats.student_count],
    ["Оценок", stats.grade_count],
    ["Средний балл", stats.average_score.toFixed(2)],
    ["Мин. оценка", stats.min_score],
    ["Макс. оценка", stats.max_score],
    ["Процент успеваемости", `${stats.pass_rate.toFixed(1)}%`],
  ];

  entries.forEach(([label, value]) => {
    const card = document.createElement("div");
    card.className = "stat-card";
    card.innerHTML = `<strong>${label}</strong><div>${value}</div>`;
    statsEl.appendChild(card);
  });
}

function renderRating(rating) {
  ratingTableBody.innerHTML = "";
  rating.forEach((student, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${student.name}</td>
      <td>${student.group}</td>
      <td>${student.average_score.toFixed(2)}</td>
    `;
    ratingTableBody.appendChild(row);
  });
}

function buildChartsFromStudents(students) {
  const scores = [];
  const groupCounts = {};
  const subjectTotals = {};
  const subjectCounts = {};

  students.forEach((student) => {
    groupCounts[student.group] = (groupCounts[student.group] || 0) + 1;
    student.grades.forEach((grade) => {
      scores.push(grade.score);
      subjectTotals[grade.subject] =
        (subjectTotals[grade.subject] || 0) + grade.score;
      subjectCounts[grade.subject] =
        (subjectCounts[grade.subject] || 0) + 1;
    });
  });

  const subjectAverages = {};
  Object.keys(subjectTotals).forEach((subject) => {
    subjectAverages[subject] = subjectTotals[subject] / subjectCounts[subject];
  });

  window.renderDistributionChart(scores);
  window.renderGroupChart(groupCounts);
  window.renderSubjectChart(subjectAverages);
}

async function fetchStats() {
  const response = await fetch("http://localhost:8000/api/statistics");
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Ошибка получения статистики");
  }
  return response.json();
}

async function fetchStudents() {
  const response = await fetch("http://localhost:8000/api/students");
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Ошибка получения студентов");
  }
  return response.json();
}

uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    setStatus("Выберите файл JSON или CSV.", true);
    return;
  }

  uploadBtn.disabled = true;
  setStatus("Загрузка...");

  try {
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://localhost:8000/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Ошибка загрузки");
    }

    const [stats, students] = await Promise.all([
      fetchStats(),
      fetchStudents(),
    ]);

    renderStats(stats);
    renderRating(stats.rating);
    buildChartsFromStudents(students);
    setStatus("Данные успешно загружены.");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    uploadBtn.disabled = false;
  }
});
