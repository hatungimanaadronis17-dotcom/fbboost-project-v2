function loadTasks() {
  fetch("/users/tasks/")
    .then(res => res.json())
    .then(tasks => {
      const tbody = document.getElementById("tasks-body");
      tbody.innerHTML = "";

      tasks.forEach(task => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><img src="${task.icon}" width="30"> ${task.network}</td>
          <td>${task.task}</td>
          <td class="reward">${task.reward} coins</td>
          <td>${task.time}</td>
          <td>
            <button class="action-btn" onclick="doTask(${task.id}, this)">
              Faire la tâche
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    });
}

function doTask(taskId, btn) {
  btn.disabled = true;
  btn.textContent = "Ouverture...";

  fetch(`/users/task/complete/${taskId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
    .then(res => res.json())
    .then(data => {
      btn.textContent = "Terminé ✔";
      alert("Tâche terminée ! Coins ajoutés.");
    });
}

// Récupère le CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

loadTasks();
setInterval(loadTasks, 15000);
