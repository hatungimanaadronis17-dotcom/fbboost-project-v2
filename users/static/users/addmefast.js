// Liste FAKE (tu remplaceras plus tard par des tâches Django)
const fakeTasks = [
  { network: "YouTube", icon: "https://img.icons8.com/fluency/48/youtube-play.png", task: "Abonnez-vous à cette chaîne", reward: 8, time: "2 min 34s" },
  { network: "Instagram", icon: "https://img.icons8.com/fluency/48/instagram-new.png", task: "Liker cette photo", reward: 5, time: "58s" },
  { network: "TikTok", icon: "https://img.icons8.com/fluency/48/tiktok.png", task: "Suivre ce compte", reward: 6, time: "1 min 12s" },
  { network: "Facebook", icon: "https://img.icons8.com/fluency/48/facebook-new.png", task: "Liker cette page", reward: 4, time: "3 min 01s" },
  { network: "Twitter", icon: "https://img.icons8.com/fluency/48/twitter.png", task: "Retweeter ce post", reward: 7, time: "42s" },
];

function loadTasks() {
  const tbody = document.getElementById("tasks-body");
  tbody.innerHTML = "";

  fakeTasks.forEach(task => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="network">
        <img src="${task.icon}" width="30"> ${task.network}
      </td>
      <td>${task.task}</td>
      <td class="reward">${task.reward} coins</td>
      <td class="timer">${task.time}</td>
      <td>
         <button class="action-btn" onclick="doTask(this)">
           Faire la tâche
         </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function doTask(btn) {
  btn.disabled = true;
  btn.textContent = "Ouverture...";

  setTimeout(() => {
    const coins = btn.closest("tr").querySelector(".reward").textContent;
    alert("Tâche accomplie ! +" + coins);

    btn.textContent = "Terminé";
  }, 1500);
}

loadTasks();
setInterval(loadTasks, 15000);
