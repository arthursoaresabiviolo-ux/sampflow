// Tab Switching
function switchTab(event, tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Edit Modal / Form Handler
function openEditModal(button) {
    const ds = button.dataset;
    const getValue = (val) => (!val || val === 'None') ? '' : val;

    document.getElementById('client-id').value = ds.id;
    document.getElementById('name').value = ds.name;
    document.getElementById('address').value = getValue(ds.address);
    document.getElementById('country').value = ds.country;
    document.getElementById('email').value = getValue(ds.email);
    document.getElementById('phone').value = getValue(ds.phone);

    document.getElementById('form-title').innerText = 'Editar Cliente';
    document.getElementById('btn-submit').innerText = 'SALVAR ALTERAÇÕES';
    document.getElementById('btn-cancel').style.display = 'block';
    document.getElementById('client-form').action = `/client/edit/${ds.id}/`;
}

function resetForm() {
    const form = document.getElementById('client-form');
    form.reset();
    document.getElementById('client-id').value = '';
    document.getElementById('form-title').innerText = 'Novo Cliente';
    document.getElementById('btn-submit').innerText = 'REGISTRAR CLIENTE';
    document.getElementById('btn-cancel').style.display = 'none';
    form.action = "{% url 'create_client' %}";
}

// Back to Top functionality
document.addEventListener('DOMContentLoaded', () => {
    const backBtn = document.getElementById('back-to-top');
    if (!backBtn) return;

    window.addEventListener('scroll', () => {
        backBtn.classList.toggle('show', window.scrollY > 50);
    });

    backBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

function openSampleModal() {
    document.getElementById('sampleModal').style.display = 'flex';
}

function closeSampleModal() {
    document.getElementById('sampleModal').style.display = 'none';
}

// Closes the modal when clicking outside the area
window.addEventListener('click', function(event) {
    const modal = document.getElementById('sampleModal');
    if (event.target === modal) {
        closeSampleModal();
    }
});