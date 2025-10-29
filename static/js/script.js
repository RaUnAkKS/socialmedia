document.addEventListener("DOMContentLoaded", () => {
    console.log("Frontend loaded ✅");
});
const searchInput = document.getElementById('search-user');
const chatItems = document.querySelectorAll('.chat-item');

searchInput?.addEventListener('input', () => {
  const filter = searchInput.value.toLowerCase();
  chatItems.forEach(item => {
    const username = item.querySelector('.chat-username').textContent.toLowerCase();
    item.style.display = username.includes(filter) ? 'flex' : 'none';
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const chatBody = document.querySelector('.chat-body');
  if (chatBody) {
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});

