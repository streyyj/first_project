// === Генерация частиц ===
const canvas = document.getElementById("particlesCanvas");
const ctx = canvas.getContext("2d");
let particles = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

function createParticle() {
  return {
    x: Math.random() * canvas.width,
    y: -Math.random() * 50,
    radius: Math.random() * 4 + 4,
    speedX: (Math.random() - 0.5) * 0.5,
    speedY: Math.random() * 1 + 0.5,
    opacity: Math.random() * 0.5 + 0.5
  };
}

function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(122, 90, 245, ${p.opacity})`;
    ctx.fill();
  });
}

function updateParticles() {
  particles.forEach(p => {
    p.x += p.speedX;
    p.y += p.speedY;
    if (p.y > canvas.height) Object.assign(p, createParticle());
  });
}

function animateParticles() {
  drawParticles();
  updateParticles();
  requestAnimationFrame(animateParticles);
}

for (let i = 0; i < 80; i++) {
  particles.push(createParticle());
}
animateParticles();

// === Логика заданий ===
const tasks = Array.from({ length: 24 }, (_, i) => i + 3); // Задания с 3 по 26
const taskList = document.getElementById("taskList");

const savedTasks = JSON.parse(localStorage.getItem("egeTasks")) || {};

tasks.forEach(num => {
  const taskId = "task" + num;
  const commentId = "comment" + num;

  const status = savedTasks[taskId]?.status || "not-done";
  const comment = savedTasks[taskId]?.comment || "";

  const li = document.createElement("li");
  li.id = `item-${taskId}`;
  li.innerHTML = `
    <div class="task-row">
      <button class="status-btn ${status}" data-task="${taskId}">${status === "done" ? "Выполнено" : "Не выполнено"}</button>
      <div style="flex:1;">
        <span class="label-text">Задание ${num}</span><br/>
        <textarea id="${commentId}" placeholder="Напиши заметку о задании..." oninput="saveProgress()">${comment}</textarea>
      </div>
    </div>
  `;
  taskList.appendChild(li);
});

// Переключение кнопок
taskList.addEventListener("click", e => {
  if (e.target.classList.contains("status-btn")) {
    const btn = e.target;
    const taskId = btn.dataset.task;
    const currentStatus = btn.classList.contains("done") ? "done" : "not-done";
    const newStatus = currentStatus === "done" ? "not-done" : "done";

    btn.className = "status-btn " + newStatus;
    btn.textContent = newStatus === "done" ? "Выполнено" : "Не выполнено";
    saveProgress();
  }
});

// Сохранение прогресса
function saveProgress() {
  const buttons = document.querySelectorAll(".status-btn");
  const progress = {};
  buttons.forEach(btn => {
    const taskId = btn.dataset.task;
    const commentId = "comment" + taskId.replace("task", "");
    progress[taskId] = {
      status: btn.classList.contains("done") ? "done" : "not-done",
      comment: document.getElementById(commentId).value
    };
  });
  localStorage.setItem("egeTasks", JSON.stringify(progress));
  updateProgress();
}

// Навигация
function scrollToTask(num) {
  const target = document.getElementById(`item-task${num}`);
  if (target) target.scrollIntoView({ behavior: "smooth", block: "center" });
  else alert("Задание не найдено!");
}

function highlightTask(num) {
  document.querySelectorAll("[id^='item-task']").forEach(el => el.style.backgroundColor = '');
  const target = document.getElementById(`item-task${num}`);
  if (target) target.style.backgroundColor = "#f0eaff";
}

// Прогресс
function updateProgress() {
  const total = tasks.length;
  const done = [...document.querySelectorAll(".status-btn.done")].length;
  const percent = Math.round((done / total) * 100);
  document.getElementById("progressText").innerText = `Выполнено: ${done} из ${total} заданий`;
  document.getElementById("progressFill").style.width = `${percent}%`;
}

// Реальное время
function updateRealTime() {
  const now = new Date();
  const options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  };
  const formattedTime = now.toLocaleDateString('ru-RU', options);
  document.getElementById("realTime").textContent = "📅 Сегодня: " + formattedTime;
}
setInterval(updateRealTime, 1000);
updateRealTime();

// Темная тема
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
}
document.getElementById("toggleTheme").onclick = toggleDarkMode;

// Инициализация
updateProgress();
