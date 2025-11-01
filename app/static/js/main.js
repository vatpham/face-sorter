const fileInput = document.getElementById('fileinput');
const preview = document.getElementById('preview');
const uploadForm = document.getElementById('uploadForm');
const loadingOverlay = document.getElementById('loadingOverlay');

preview.innerHTML = '';

fileInput.addEventListener('change', () => {
    preview.innerHTML = ''; // clear previous thumbnails
    Array.from(fileInput.files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = e => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'h-24 w-auto rounded-md border border-gray-300 object-contain bg-white';
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
});

window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        window.location.reload();
    }
});

uploadForm.addEventListener('submit', (e) => {
    const files = Array.from(fileInput.files || []);
    if (files.length === 0) return;
    loadingOverlay.classList.remove('hidden');
});
window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        loadingOverlay.classList.add('hidden');
    }
});

