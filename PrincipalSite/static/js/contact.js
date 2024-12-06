//Se activará cuando el formulario esté ok
document.addEventListener("DOMContentLoaded", function() {
    // Aquí se setea el formulario al cual hará referencia y al botón que lo activará
    const form = document.getElementById("contactForm");
    const sendMessageButton = document.getElementById("sendMessageButton");

    // Aquí se referencia el evento de escucha
    form.addEventListener("submit", function(event) {
        event.preventDefault(); 

        // Vamos a crear el formulario con los datos del formulario, los que se reciben
        const formData = new FormData(form);

        // Se usa ajax para enviarlos
        fetch(contactUrl, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //Si todo sale ok, se muestra el modal
                $('#successModal').modal('show');
                form.reset(); 
            } else {
                // Si hubo un error se mostrará una alerta tradicional, sin modal.
                alert("Hubo un error al enviar el formulario. Intenta nuevamente.");
            }
        })
        .catch(error => {
            console.error("Error al enviar el formulario:", error);
            alert("Hubo un error al enviar el formulario. Intenta nuevamente.");
        });
    });

    // Función para cerrar el modal
    const closeModalButton = document.querySelector('.btn-secondary');
    if (closeModalButton) {
        closeModalButton.addEventListener('click', function() {
            $('#successModal').modal('hide');
        });
    }
});
