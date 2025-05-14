// Archivo JavaScript principal
document.addEventListener("DOMContentLoaded", function () {
  // Escuchar eventos de notificación globales
  document.addEventListener("showNotification", function (e) {
    const { message, type } = e.detail;
    showNotification(message, type);
  });

  // Sistema de notificaciones
  function showNotification(message, type = "info") {
    const notifications = document.getElementById("notifications");
    if (!notifications) return;

    const notification = document.createElement("div");
    let icon = "";

    switch (type) {
      case "success":
        icon = '<i class="bi bi-check-circle-fill me-2 text-success"></i>';
        break;
      case "error":
        icon = '<i class="bi bi-exclamation-circle-fill me-2 text-danger"></i>';
        break;
      case "warning":
        icon =
          '<i class="bi bi-exclamation-triangle-fill me-2 text-warning"></i>';
        break;
      default:
        icon = '<i class="bi bi-info-circle-fill me-2 text-info"></i>';
    }

    notification.className = "notification";
    notification.innerHTML = `
            <div class="d-flex align-items-center">
                ${icon}
                <div>${message}</div>
                <button type="button" class="btn-close btn-close-white ms-auto" aria-label="Close"></button>
            </div>
        `;

    notifications.appendChild(notification);

    // Mostrar la notificación
    setTimeout(() => {
      notification.classList.add("show");
    }, 10);

    // Configurar el cierre
    const closeBtn = notification.querySelector(".btn-close");
    closeBtn.addEventListener("click", () => {
      notification.classList.remove("show");
      setTimeout(() => {
        notification.remove();
      }, 300);
    });

    // Auto cerrar después de 5 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.classList.remove("show");
        setTimeout(() => {
          if (notification.parentNode) {
            notification.remove();
          }
        }, 300);
      }
    }, 5000);
  }

  // Efectos de animación para elementos interactivos
  const interactiveElements = document.querySelectorAll(
    ".card, .btn-danger, .gallery-item"
  );
  interactiveElements.forEach((element) => {
    element.addEventListener("mouseenter", function () {
      this.classList.add("hovering");
    });

    element.addEventListener("mouseleave", function () {
      this.classList.remove("hovering");
    });
  });
});
