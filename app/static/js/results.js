const imageModal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImg');

window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
});

window.addEventListener('popstate', function () {
    const ok = confirm('Leave results and go back?');
    if (!ok) history.forward();
});

document.querySelectorAll('section img').forEach(img => {
    img.addEventListener('click', () => {
        modalImg.src = img.src; // set modal image source
        imageModal.classList.remove('hidden'); // show modal
    });
});

// close modal when clicking outside image
imageModal.addEventListener('click', (e) => {
    if (e.target === imageModal) {
        imageModal.classList.add('hidden'); // hide modal
    }
});