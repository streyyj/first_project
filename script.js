// === Firebase Конфиг (вставь свой!) ===
const firebaseConfig = {
    apiKey: "AIzaSyDPpt3LIyOgUJBJfy9kM1uLe3vot53AKck",
    authDomain: "streyj-77632.firebaseapp.com",
    projectId: "streyj-77632",
    storageBucket: "streyj-77632.firebasestorage.app",
    messagingSenderId: "377000252929",
    appId: "1:377000252929:web:6b05402714faa47cb01200",
    databaseURL: "https://your-project.firebaseio.com",
    storageBucket: "your-project.appspot.com",
  };
  
  firebase.initializeApp(firebaseConfig);
  const database = firebase.database();
  const storage = firebase.storage();
  
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
  
  for (let i = 0; i < 80; i++) particles.push(createParticle());
  animateParticles();
  
  // === Логика заданий ===
  const tasks = Array.from({ length: 24 }, (_, i) => i + 3);
  const taskList = document.getElementById("taskList");
  
  function loadTasksFromFirebase() {
    database.ref("egeTasks").on("value", snapshot => {
      const savedTasks = snapshot.val() || {};
      taskList.innerHTML = "";
      tasks.forEach(num => {
        const taskId = "task" + num;
        const commentId = "comment" + num;
        const linkId = "link" + num;
        const fileId = "file" + num;
  
        const status = savedTasks[taskId]?.status || "not-done";
        const comment = savedTasks[taskId]?.comment || "";
        const link = savedTasks[taskId]?.link || "";
        const fileName = savedTasks[taskId]?.fileName || "";
  
        const li = document.createElement("li");
        li.id = `item-${taskId}`;
        li.innerHTML = `
          <div class="task-row">
            <button class="status-btn ${status}" data-task="${taskId}">${status === "done" ? "Выполнено" : "Не выполнено"}</button>
            <div style="flex:1;">
              <span class="label-text">Задание ${num}</span><br/>
              <textarea id="${commentId}" placeholder="Напиши заметку о задании..." oninput="saveProgress(${num})">${comment}</textarea>
              <input type="text" id="${linkId}" placeholder="Ссылка или файл..." value="${link}" oninput="saveProgress(${num})">
              <br/><br/>
              <div class="file-upload-area" ondragover="dragOverHandler(event)" ondrop="dropHandler(event, ${num})" onclick="document.getElementById('file${num}').click()">
                📁 Нажми или перетащи файл сюда
                <input type="file" id="file${num}" onchange="uploadFile(${num})" style="display:none;">
              </div>
              <span id="fileName${num}">${fileName}</span>
              <button onclick="downloadFile(${num})" id="downloadBtn${num}" style="margin-left: 10px; display: ${fileName ? 'inline-block' : 'none'};">📥 Скачать</button>
              <button onclick="deleteFile(${num})" id="deleteBtn${num}" style="margin-left: 10px; display: ${fileName ? 'inline-block' : 'none'};">🗑️ Удалить</button>
            </div>
          </div>
        `;
        taskList.appendChild(li);
      });
    });
  }
  
  // === Обновление прогресса ===
  function saveProgress(taskNum) {
    const taskId = "task" + taskNum;
    const comment = document.getElementById("comment" + taskNum).value;
    const link = document.getElementById("link" + taskNum).value;
    const saved = JSON.parse(localStorage.getItem("egeTasks")) || {};
  
    saved[taskId] = {
      status: saved[taskId]?.status || "not-done",
      comment,
      link,
      fileName: saved[taskId]?.fileName || "",
    };
  
    localStorage.setItem("egeTasks", JSON.stringify(saved));
    database.ref("egeTasks/" + taskId).update({
      comment,
      link,
      fileName: saved[taskId]?.fileName || ""
    });
  }
  
  // === Кнопка статуса ===
  document.addEventListener("click", e => {
    if (e.target.classList.contains("status-btn")) {
      const btn = e.target;
      const taskId = btn.dataset.task;
      const currentStatus = btn.classList.contains("done") ? "done" : "not-done";
      const newStatus = currentStatus === "done" ? "not-done" : "done";
  
      btn.className = "status-btn " + newStatus;
      btn.textContent = newStatus === "done" ? "Выполнено" : "Не выполнено";
  
      const saved = JSON.parse(localStorage.getItem("egeTasks")) || {};
      saved[taskId] = { ...saved[taskId], status: newStatus };
      localStorage.setItem("egeTasks", JSON.stringify(saved));
  
      database.ref("egeTasks/" + taskId).update({ status: newStatus });
    }
  });
  
  // === Drag & Drop файлов ===
  function dragOverHandler(e) {
    e.preventDefault();
    e.target.classList.add("hover");
  }
  
  function dropHandler(e, taskNum) {
    e.preventDefault();
    e.target.classList.remove("hover");
    const file = e.dataTransfer.files[0];
    handleFile(file, taskNum);
  }
  
  function uploadFile(taskNum) {
    const file = document.getElementById("file" + taskNum).files[0];
    handleFile(file, taskNum);
  }
  
  function handleFile(file, taskNum) {
    if (!file) return;
  
    const reader = new FileReader();
    reader.onload = function(e) {
      const taskId = "task" + taskNum;
      const fileNameSpan = document.getElementById("fileName" + taskNum);
      const downloadBtn = document.getElementById("downloadBtn" + taskNum);
      const deleteBtn = document.getElementById("deleteBtn" + taskNum);
  
      // Сохраняем имя файла локально
      const saved = JSON.parse(localStorage.getItem("egeTasks")) || {};
      saved[taskId] = { ...saved[taskId], fileName: file.name };
      localStorage.setItem("egeTasks", JSON.stringify(saved));
  
      // Загружаем файл в Firebase Storage
      const storageRef = storage.ref(`uploads/${taskId}-${file.name}`);
      const metadata = { contentType: file.type };
  
      storageRef.put(file, metadata).then(snapshot => {
        console.log("Файл загружен:", snapshot.totalBytes, "bytes");
        return snapshot.ref.getDownloadURL();
      }).then(downloadURL => {
        fileNameSpan.textContent = file.name;
        downloadBtn.onclick = () => {
          window.open(downloadURL);
        };
        downloadBtn.style.display = "inline-block";
        deleteBtn.onclick = () => deleteFile(taskNum);
        deleteBtn.style.display = "inline-block";
  
        database.ref("egeTasks/" + taskId).update({ fileName: file.name });
      });
    };
    reader.readAsDataURL(file);
  }
  
  // === Скачивание и удаление файлов ===
  function downloadFile(taskNum) {
    const ref = storage.ref(`uploads/task${taskNum}-somefile.pdf`);
    ref.getDownloadURL().then(url => {
      const a = document.createElement("a");
      a.href = url;
      a.download = `задание_${taskNum}.pdf`;
      a.click();
    });
  }
  
  function deleteFile(taskNum) {
    const taskId = "task" + taskNum;
    storage.ref(`uploads/${taskId}-somefile.pdf`).delete().then(() => {
      document.getElementById("fileName" + taskNum).textContent = "";
      document.getElementById("downloadBtn" + taskNum).style.display = "none";
      document.getElementById("deleteBtn" + taskNum).style.display = "none";
      document.getElementById("file" + taskNum).value = "";
  
      const saved = JSON.parse(localStorage.getItem("egeTasks")) || {};
      delete saved[taskId].fileName;
      localStorage.setItem("egeTasks", JSON.stringify(saved));
      database.ref("egeTasks/" + taskId).update({ fileName: null });
    });
  }
  
  // === Реальное время ===
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
  
  // === Прогресс ===
  function updateProgress() {
    const total = tasks.length;
    const done = [...document.querySelectorAll(".status-btn.done")].length;
    const percent = Math.round((done / total) * 100);
    document.getElementById("progressText").innerText = `Выполнено: ${done} из ${total} заданий`;
    document.getElementById("progressFill").style.width = `${percent}%`;
  }
  
  // === Тема ===
  function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
  }
  document.getElementById("toggleTheme").onclick = toggleDarkMode;
  
  // === Первый запуск ===
  loadTasksFromFirebase();
  updateProgress();
