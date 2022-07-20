import { Modal } from 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Cropper from 'cropperjs';

const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.overlay');
const closeSidebar = document.querySelector('.close-sidebar');
const openSidebar = document.querySelector('.open-sidebar');
const overlayToggles = document.querySelectorAll('.overlay-toggle');

// Activate the sidebar active element
const menuContainers = document.querySelectorAll('.menu-container');
menuContainers?.forEach(menuContainer => {
    document.getElementById(menuContainer.dataset.activeItem)?.classList.add("active")
})

overlay?.addEventListener('click', () => {
    overlayToggles?.forEach(toggle => {
        toggle.classList.remove('active');
    })
    overlay?.classList.remove('active');
})

closeSidebar?.addEventListener("click", () => {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
})

openSidebar?.addEventListener("click", () => {
    sidebar.classList.add('active');
    overlay.classList.add('active');
})

// Toggle alerts
const alertContainer = document.querySelector(".alert-container")
window.hideAlert = function () {
    alertContainer?.classList.add("hide")
}


// Form validation
window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})


// Deletion
const confirmationForms = document.querySelectorAll(".requires-confirmation")
const generalDeletionModal = document.querySelector("#generalDeletionModal")
const confirmButton = document.querySelector("#confirm-button")
confirmationForms?.forEach(form => {
    const message = form.dataset.message
    form.addEventListener("submit", event => {
        event.preventDefault()
        var myModal = new Modal(generalDeletionModal)
        if (message != null) {
            generalDeletionModal.querySelector("#message").innerHTML = message
        }
        myModal.show()

        confirmButton.onclick = () => {
            form.removeEventListener("submit", event)
            form.submit()
        }
    })
})

// Toggle session for subject mapping
window.toggleSession = function (element) {
    const sessionId = element.value
    const location = window.location
    const url = new URL(location)
    url.searchParams.set("session_id", sessionId)
    window.location.href = url.href
}

// Update report modal src
const reportIframe = document.querySelector("#report-iframe")
const reportPreviewButton = document.querySelector("#report-preview-button")
window.updateReportIframeSrc = function (url) {
    reportPreviewButton?.setAttribute("href", url)
    reportIframe?.setAttribute("src", url)
}


// Cropping
const croppableContainers = document.querySelectorAll(".croppable-container")
croppableContainers?.forEach(container => {
    const image = container.querySelector('img');
    const dataContainer = container.querySelector('.cropdata');
    if (image != null && dataContainer != null) {
        let aspectRatio = image.dataset.aspectRatio
        if (aspectRatio != null && aspectRatio != undefined && aspectRatio != "") {
            aspectRatio = aspectRatio.split(":").map(x => parseInt(x))
            aspectRatio = aspectRatio[0] / aspectRatio[1]
        } else {
            aspectRatio = null
        }
        new Cropper(image, {
            aspectRatio: aspectRatio,
            crop(event) {
                const data = `${event.detail.x},${event.detail.y},${event.detail.width},${event.detail.height},${event.detail.rotate},${event.detail.scaleX},${event.detail.scaleY}`
                dataContainer.setAttribute("value", data)
            },
        });
    }
})
