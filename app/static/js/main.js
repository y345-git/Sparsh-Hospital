// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Handle toggle fields
    const toggleSelects = document.querySelectorAll('.toggle-days');
    toggleSelects.forEach(select => {
        // Set initial state
        const targetId = select.dataset.target;
        const targetField = document.getElementById(targetId);
        if (targetField) {
            targetField.disabled = select.value === '0';
        }

        // Add change listener
        select.addEventListener('change', function() {
            const targetId = this.dataset.target;
            const targetField = document.getElementById(targetId);
            if (targetField) {
                targetField.disabled = this.value === '0';
                if (this.value === '0') {
                    targetField.value = '';
                }
            }
        });
    });
});

// Flash message auto-hide
window.setTimeout(function() {
    // Only select alerts inside the container, not the permanent notification at the top
    const alerts = document.querySelectorAll('.container-fluid .alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease-in-out';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 3000);

// Form validation for patient forms
function validatePatientForm(event) {
    const form = event.target;
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        
        // Find all invalid required fields
        const invalidFields = form.querySelectorAll(':invalid');
        let errorMessage = 'Please fill in the following required fields:\n';
        invalidFields.forEach(field => {
            const label = field.closest('.col-md-6, .col-md-4, .col-md-3, .col-12')
                              .querySelector('.form-label')
                              ?.textContent || field.name;
            errorMessage += `\n- ${label.trim()}`;
        });
        
        // Show alert
        alert(errorMessage);
    }
    form.classList.add('was-validated');
}

// Add event listeners when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Find all patient forms (both add and edit)
    const patientForms = document.querySelectorAll('#patientForm');
    patientForms.forEach(form => {
        form.addEventListener('submit', validatePatientForm);
    });
}); 