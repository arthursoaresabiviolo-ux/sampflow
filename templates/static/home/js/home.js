function switchTab(event, tabId) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));

            // Deactivate all tab buttons
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Activate selected tab and button
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

// Back to Top Button Functionality
document.addEventListener('DOMContentLoaded', () => {
    const backToTopBtn = document.getElementById('back-to-top');

    if (!backToTopBtn) return;

    const checkScroll = (scrollTop) => {
        if (scrollTop > 50) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    };

    window.addEventListener('scroll', () => {
        checkScroll(window.scrollY || document.documentElement.scrollTop);
    });

    document.addEventListener('scroll', (e) => {
        if (e.target.scrollTop !== undefined) {
            checkScroll(e.target.scrollTop);
        }
    }, true);

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

        const activeTab = document.querySelector('.tab-content.active');
        if (activeTab) {
            activeTab.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});

function openEditModal(button) {
// 1. Get the data from the pencil button's data-* attributes
const id = button.dataset.id;
const name = button.dataset.name;
const address = button.dataset.address;
const country = button.dataset.country;
const email = button.dataset.email;
const phone = button.dataset.phone;

// 2. Fills in the form fields
document.getElementById('client-id').value = id;
document.getElementById('name').value = name;
document.getElementById('address').value = (address === 'None' || !address) ? '' : address;
document.getElementById('country').value = country;
document.getElementById('email').value = (email === 'None' || !email) ? '' : email;
document.getElementById('phone').value = (phone === 'None' || !phone) ? '' : phone;

// 3. Switches the form interface to Edit mode
document.getElementById('form-title').innerText = 'Editar Cliente';
document.getElementById('btn-submit').innerText = 'SALVAR ALTERAÇÕES';
document.getElementById('btn-cancel').style.display = 'block';

// 4. Redirects the form action to the update route
document.getElementById('client-form').action = `/client/edit/${id}/`;
}

function resetForm() {
// Clears the form and returns to "New Customer" mode
document.getElementById('client-id').value = '';
document.getElementById('client-form').reset();

document.getElementById('form-title').innerText = 'Novo Cliente';
document.getElementById('btn-submit').innerText = 'REGISTRAR CLIENTE';
document.getElementById('btn-cancel').style.display = 'none';

document.getElementById('client-form').action = "{% url 'create_client' %}";
}
