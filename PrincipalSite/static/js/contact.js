document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("contactForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Prevenir el comportamiento por defecto del formulario

        const formData = new FormData(form);  // Recoger los datos del formulario

        fetch("/contact/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())  // Tomamos la respuesta del server
        .then(data => {
            // Limpiar los errores anteriores
            clearErrors();

            if (data.success) {
                // Mostrar el modal de éxito si la respuesta es exitosa y el form guardó todo ok
                $('#successModal').modal('show');
                form.reset();  // Limpiar el formulario después de enviarlo
            } else {
                // Si hay errores, mostrar los mensajes específicos (salen en inglés temporalmente)
                showErrors(data.errors);
            }
        })
        .catch(error => {
            console.error("Error al enviar el formulario:", error);
            alert("Hubo un error en el envío del formulario.");
        });
    });

    // Función para mostrar los errores (si son campos inválidos o si son obligatorios :)
    function showErrors(errors) {
        // Sirve para mostrar cada error en su lugar específico
        for (const field in errors) {
            const fieldElement = document.querySelector(`[name="${field}"]`);
            if (fieldElement) {
                const errorMessage = errors[field].join(", ");  // Unir errores si hay más de uno
                const errorElement = fieldElement.closest('.control-group').querySelector('.help-block');
                if (errorElement) {
                    errorElement.textContent = errorMessage;
                    errorElement.style.display = 'block';  // Asegurarse de que el mensaje de error sea visible
                }
            }
        }
    }

    // Función para limpiar los errores cuando el usuario los corrija!
    function clearErrors() {
        const errorElements = document.querySelectorAll('.help-block');
        errorElements.forEach((errorElement) => {
            errorElement.textContent = '';
            errorElement.style.display = 'none';  // Ocultar los mensajes cuando los estén corrigiendo
        });
    }
});
