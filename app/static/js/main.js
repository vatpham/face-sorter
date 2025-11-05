const fileInput = document.getElementById('fileinput');
const preview = document.getElementById('preview');
const uploadForm = document.getElementById('uploadForm');
const loadingOverlay = document.getElementById('loadingOverlay');
const dropZone = document.getElementById('drop-zone');
const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');

preview.innerHTML = '';

function handleFiles(files) {
    if (!files || files.length === 0) {
        clearBtn.classList.add('hidden');
        submitBtn.classList.add('hidden');
        preview.innerHTML = '';
        fileInput.value = '';
        return;
    }

    // filter image files
    const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
    if (imageFiles.length === 0) return;

    const dataTransfer = new DataTransfer();
    imageFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;

    // update preview
    preview.innerHTML = '';
    Array.from(fileInput.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'h-24 w-auto rounded-md border border-gray-300 object-contain bg-white';
            preview.appendChild(img);
        };
        reader.readAsDataURL(file);
    });

    clearBtn.classList.remove('hidden');
    submitBtn.classList.remove('hidden');
}

fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function dropHandler(e) {
    e.preventDefault();
    dropZone.classList.remove('border-4', 'border-blue-600');
    handleFiles(e.dataTransfer.files);
}
dropZone.addEventListener('drop', dropHandler);

// cursor effect
dropZone.addEventListener('dragover', (e) => {
    const fileItems = [...e.dataTransfer.items].filter(item => item.kind === 'file');
    if (fileItems.length > 0) {
        e.preventDefault(); // allow drop
        e.dataTransfer.dropEffect = fileItems.some(item => item.type.startsWith('image/')) ? 'copy' : 'none';
    }
});

// border on dragenter and dragleave
dropZone.addEventListener('dragenter', () => {
    dropZone.classList.add('border-4', 'border-blue-600');
});
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-4', 'border-blue-600');
});
dropZone.addEventListener('drop', () => {
    dropZone.classList.remove('border-4', 'border-blue-600');
});

// prevent default drop/open behavior on window
window.addEventListener('dragover', (e) => {
    const fileItems = [...e.dataTransfer.items].filter(item => item.kind === 'file');
    if (fileItems.length > 0) e.preventDefault();
});
window.addEventListener('drop', (e) => {
    const fileItems = [...e.dataTransfer.items].filter(item => item.kind === 'file');
    if (fileItems.length > 0) e.preventDefault();
});

// show loading overlay on form submit
uploadForm.addEventListener('submit', () => {
    const files = Array.from(fileInput.files || []);
    if (files.length === 0) return;
    loadingOverlay.classList.remove('hidden');
});

clearBtn.addEventListener('click', () => {
    fileInput.value = '';   // clear file input
    preview.innerHTML = ''; // clear preview
    dropZone.classList.remove('border-4', 'border-blue-600'); // reset drag highlight
    clearBtn.classList.add('hidden'); // hide clear button if no files
    submitBtn.classList.add('hidden'); // hide submit button if no files
});