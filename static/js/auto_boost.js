document.addEventListener('DOMContentLoaded', () => {
    const badge = document.querySelector('.auto-boost-badge');
    if (!badge) return;

    const delay = 30000; // 30 secondes
    let index = 0;

    const autoLike = () => {
        const buttons = document.querySelectorAll('.like-btn');
        if (buttons.length === 0) return;

        const btn = buttons[index % buttons.length];
        if (!btn.classList.contains('liked')) {
            btn.classList.add('liked');
            btn.innerHTML = `Liked !`;
            const postId = btn.dataset.postId;
            fetch(`/like/${postId}/`, { method: 'GET' });
        }
        index++;
    };

    setInterval(autoLike, delay);
    console.log('FB Boost Auto activé – like toutes les 30s');
});
