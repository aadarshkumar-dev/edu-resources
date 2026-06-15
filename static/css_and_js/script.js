const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('active');
});


let notify = document.getElementById("notify");

notify.classList.remove("notify_go");
notify.classList.add("notify_come");

setTimeout(() => {
    notify.classList.remove("notify_come");
    notify.classList.add("notify_go");
}, 6000);
