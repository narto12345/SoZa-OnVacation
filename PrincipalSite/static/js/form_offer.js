document.addEventListener('DOMContentLoaded', function () {
    const dropZonePrincipal = document.getElementById('drop-zone-principal');
    const fileInputPrincipal = document.getElementById('imagenPrincipal');
    const previewContainerPrincipal = document.getElementById('preview-container-principal');

    const dropZoneCarrusel = document.getElementById('drop-zone-carrusel');
    const fileInputCarrusel = document.getElementById('imagenesCarrusel');
    const previewContainerCarrusel = document.getElementById('preview-container-carrusel');

    function showImagePreviewPrincipal(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewContainerPrincipal.innerHTML = ''; 

            const imgContainer = document.createElement('div');
            imgContainer.classList.add('image-container');
            imgContainer.style.position = 'relative';

            const imgElement = document.createElement('img');
            imgElement.classList.add('img-fluid');
            imgElement.src = e.target.result;

            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.classList.add('remove-button');
            removeButton.style.position = 'absolute';
            removeButton.style.top = '5px';
            removeButton.style.right = '5px';
            removeButton.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
            removeButton.style.color = 'white';
            removeButton.style.border = 'none';
            removeButton.style.borderRadius = '50%';
            removeButton.style.fontSize = '14px';
            removeButton.style.cursor = 'pointer';

            removeButton.addEventListener('click', function () {
                previewContainerPrincipal.innerHTML = ''; 
                fileInputPrincipal.value = ""; 
            });

            imgContainer.appendChild(imgElement);
            imgContainer.appendChild(removeButton);

            previewContainerPrincipal.appendChild(imgContainer);
        };
        reader.readAsDataURL(file); 
    }

    function showImagePreviewCarrusel(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imgElement = document.createElement('img');
            imgElement.classList.add('img-fluid');
            imgElement.style.width = '100px'; 
            imgElement.style.height = '100px'; 
            imgElement.style.marginRight = '10px'; 
            imgElement.style.marginBottom = '10px'; 
            imgElement.src = e.target.result;

            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.classList.add('remove-button');
            removeButton.style.position = 'absolute';
            removeButton.style.top = '0';
            removeButton.style.right = '0';
            removeButton.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
            removeButton.style.color = 'white';
            removeButton.style.border = 'none';
            removeButton.style.borderRadius = '50%';
            removeButton.style.fontSize = '14px';
            removeButton.style.cursor = 'pointer';

            removeButton.addEventListener('click', function () {
                previewContainerCarrusel.removeChild(imgContainer); 
            });

            const imgContainer = document.createElement('div');
            imgContainer.style.position = 'relative';
            imgContainer.style.display = 'inline-block';

            imgContainer.appendChild(imgElement);
            imgContainer.appendChild(removeButton);

            previewContainerCarrusel.appendChild(imgContainer);
        };
        reader.readAsDataURL(file); 
    }

    fileInputPrincipal.addEventListener('change', function () {
        const files = fileInputPrincipal.files;
        if (files.length > 0) {
            showImagePreviewPrincipal(files[0]); 
        }
    });

    dropZonePrincipal.addEventListener('dragover', function (event) {
        event.preventDefault(); 
        dropZonePrincipal.style.backgroundColor = '#e9e9e9'; 
    });

    dropZonePrincipal.addEventListener('dragleave', function () {
        dropZonePrincipal.style.backgroundColor = '#f9f9f9'; 
    });

    dropZonePrincipal.addEventListener('drop', function (event) {
        event.preventDefault();
        dropZonePrincipal.style.backgroundColor = '#f9f9f9';

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            showImagePreviewPrincipal(files[0]); 
        }
    });

    dropZonePrincipal.addEventListener('click', function () {
        fileInputPrincipal.click();
    });

    fileInputCarrusel.addEventListener('change', function () {
        const files = fileInputCarrusel.files;
        if (files.length > 0) {
            Array.from(files).forEach(file => {
                showImagePreviewCarrusel(file); 
            });
        }
    });

    dropZoneCarrusel.addEventListener('dragover', function (event) {
        event.preventDefault();
        dropZoneCarrusel.style.backgroundColor = '#e9e9e9'; 
    });

    dropZoneCarrusel.addEventListener('dragleave', function () {
        dropZoneCarrusel.style.backgroundColor = '#f9f9f9'; 
    });

    dropZoneCarrusel.addEventListener('drop', function (event) {
        event.preventDefault();
        dropZoneCarrusel.style.backgroundColor = '#f9f9f9';

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            Array.from(files).forEach(file => {
                showImagePreviewCarrusel(file);
            });
        }
    });
    dropZoneCarrusel.addEventListener('click', function () {
        fileInputCarrusel.click();
    });
});
