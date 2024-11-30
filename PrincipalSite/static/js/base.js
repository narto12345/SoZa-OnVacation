// Nicolas Code
const dropdownButton = document.getElementById("dropdown-button");
const dropdownContent = document.getElementById("dropdown-content");
const navbarCollapse = document.getElementById("navbarCollapse");

dropdownButton.addEventListener("click", () => {
  const isOpen = dropdownContent.style.opacity === "1";

  if (isOpen) {
    dropdownContent.style.opacity = "0";
    dropdownContent.style.transform = "scaleY(0)";
  } else {
    dropdownContent.style.opacity = "1";
    dropdownContent.style.transform = "scaleY(1)";
  }
});

// Opcional: Cerrar el dropdown si haces clic fuera
document.addEventListener("click", (event) => {
  if (!event.target.closest("#dropdown-button")) {
    dropdownContent.style.opacity = "0";
    dropdownContent.style.transform = "scaleY(0)";
  }
});
