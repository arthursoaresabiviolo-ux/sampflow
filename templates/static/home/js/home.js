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
    const form = document.getElementById('sample-form');
    form.reset();
    form.action = '/sample/create/';
    document.getElementById('sample-modal-title').innerText = 'Cadastrar Nova Amostra';
    document.getElementById('sample-submit-btn').innerText = 'Salvar Amostra';
    document.getElementById('sampleModal').style.display = 'flex';
}

function closeSampleModal() {
    document.getElementById('sampleModal').style.display = 'none';
}

function toggleSampleDetails(sampleId, button) {
    const details = document.getElementById(`sample-details-${sampleId}`);
    if (!details) return;

    const expanded = details.hasAttribute('hidden');
    details.toggleAttribute('hidden', !expanded);
    button.title = expanded ? 'Ocultar detalhes' : 'Ver detalhes e editar amostra';
    button.setAttribute('aria-expanded', String(expanded));
    button.querySelector('.sample-details-label').textContent = expanded ? 'Ocultar' : 'Detalhes';
    button.classList.toggle('is-expanded', expanded);
}

function openSampleEditModal(button) {
    const data = button.dataset;
    const form = document.getElementById('sample-form');
    const value = (name) => data[name] || '';

    form.reset();
    form.action = `/sample/edit/${data.id}/`;
    document.getElementById('client').value = value('client');
    document.getElementById('contract').value = value('contract');
    document.getElementById('reference-month').value = value('referenceMonth');
    document.getElementById('sample-type').value = value('sampleType');
    document.getElementById('status').value = value('status');
    document.getElementById('weight').value = value('weight');
    document.getElementById('shipment-cost').value = value('shipmentCost');
    document.getElementById('fiscal-number').value = value('fiscalNumber');
    document.getElementById('shipping-date').value = value('shippingDate');
    document.getElementById('delivery-date').value = value('deliveryDate');
    document.getElementById('tracking-number').value = value('trackingNumber');
    document.getElementById('courier').value = value('courier');
    document.getElementById('screen-size').value = value('screenSize');
    document.getElementById('cupping').value = value('cupping');
    document.getElementById('comments').value = value('comments');
    document.getElementById('sample-modal-title').innerText = 'Editar Amostra';
    document.getElementById('sample-submit-btn').innerText = 'Salvar alterações';
    document.getElementById('sampleModal').style.display = 'flex';
}

// Closes the modal when clicking outside the area
window.addEventListener('click', function(event) {
    const modal = document.getElementById('sampleModal');
    if (event.target === modal) {
        closeSampleModal();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-sample-details').forEach(function(button) {
        button.addEventListener('click', function() {
            toggleSampleDetails(button.dataset.sampleId, button);
        });
    });
});
