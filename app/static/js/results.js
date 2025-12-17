const imageModal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImg');

/* 
window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
});

window.addEventListener('popstate', function () {
    const ok = confirm('Leave results and go back?');
    if (!ok) history.forward();
});
 */

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

// Rename functionality
let currentPersonName = '';
const renameModal = document.getElementById('renameModal');
const renameInput = document.getElementById('renameInput');
const renameBtns = document.querySelectorAll('.renameBtn');

renameBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        currentPersonName = btn.dataset.personName;
        renameInput.value = btn.dataset.personDisplay;
        renameModal.classList.remove('hidden');
    });
});

document.getElementById('renameCancel').addEventListener('click', () => {
    renameModal.classList.add('hidden');
});

document.getElementById('renameSave').addEventListener('click', async () => {
    const newName = renameInput.value.trim();
    if (!newName) {
        alert('Please enter a name');
        return;
    }

    try {
        const response = await fetch('/rename-person', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ old_name: currentPersonName, new_name: newName })
        });

        if (response.ok) {
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to rename');
        }
    } catch (err) {
        alert('Error: ' + err.message);
    }
});