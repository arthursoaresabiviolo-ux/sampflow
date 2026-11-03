// Tab Switching & Persistence
function activateTab(tabId, updateUrl = true) {
    const targetContent = document.getElementById(tabId);
    if (!targetContent) return;

    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

    targetContent.classList.add('active');

    const matchingBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    if (matchingBtn) {
        matchingBtn.classList.add('active');
    }

    try {
        localStorage.setItem('sampflow_active_tab', tabId);
    } catch (e) {}

    if (updateUrl) {
        if (window.history && window.history.replaceState) {
            window.history.replaceState(null, '', `#${tabId}`);
        } else {
            window.location.hash = tabId;
        }
    }

    const preloadStyle = document.getElementById('tab-preload-style');
    if (preloadStyle) {
        preloadStyle.remove();
    }

    const backBtn = document.getElementById('back-to-top');
    if (backBtn) {
        backBtn.classList.toggle('show', window.scrollY > 50);
    }
}

function switchTab(event, tabId) {
    if (event && event.preventDefault) {
        event.preventDefault();
    }
    activateTab(tabId, true);
}

function restoreActiveTab() {
    const validTabs = ['samples-tab', 'dashboards-tab', 'clients-tab'];
    const hash = window.location.hash ? window.location.hash.replace('#', '') : null;
    let targetTab = null;

    if (hash && validTabs.includes(hash)) {
        targetTab = hash;
    } else {
        try {
            const storedTab = localStorage.getItem('sampflow_active_tab');
            if (storedTab && validTabs.includes(storedTab)) {
                targetTab = storedTab;
            }
        } catch (e) {}
    }

    if (targetTab) {
        activateTab(targetTab, false);
    }
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
    const normalize = (text) => String(text).trim().toLocaleLowerCase('pt-BR');
    const setSelectValue = (id, rawValue) => {
        const select = document.getElementById(id);
        const matchingOption = Array.from(select.options).find(
            (option) => normalize(option.value) === normalize(rawValue)
        );
        select.value = matchingOption ? matchingOption.value : rawValue;
    };

    form.reset();
    form.action = `/sample/edit/${data.id}/`;
    setSelectValue('client', value('client'));
    document.getElementById('contract').value = value('contract');
    document.getElementById('reference-month').value = value('referenceMonth');
    setSelectValue('sample-type', value('sampleType'));
    setSelectValue('status', value('status'));
    document.getElementById('weight').value = value('weight');
    document.getElementById('gross-weight').value = value('grossWeight');
    setSelectValue('package-type', value('packageType'));
    document.getElementById('shipment-cost').value = value('shipmentCost');
    document.getElementById('fiscal-number').value = value('fiscalNumber');
    document.getElementById('shipping-date').value = value('shippingDate');
    document.getElementById('delivery-date').value = value('deliveryDate');
    document.getElementById('tracking-number').value = value('trackingNumber');
    setSelectValue('courier', value('courier'));
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

// Sample Search / Filter Functionality
function initSampleSearch() {
    const searchInput = document.getElementById('sample-search-input');
    const clearBtn = document.getElementById('clear-sample-search');
    const noResults = document.getElementById('no-search-results');
    if (!searchInput) return;

    const normalize = (text) => (text || '')
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .trim();

    const performFilter = () => {
        const query = normalize(searchInput.value);
        const cards = document.querySelectorAll('.samples-grid .sample-card');
        let visibleCount = 0;

        if (clearBtn) {
            clearBtn.style.display = query.length > 0 ? 'block' : 'none';
        }

        cards.forEach((card) => {
            const cardText = normalize(card.textContent);
            const matches = !query || cardText.includes(query);
            card.style.display = matches ? '' : 'none';
            if (matches) visibleCount++;
        });

        if (noResults) {
            noResults.style.display = (cards.length > 0 && visibleCount === 0) ? 'block' : 'none';
        }
    };

    searchInput.addEventListener('input', performFilter);

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            performFilter();
            searchInput.focus();
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    restoreActiveTab();
    initSampleSearch();
    const sampleForm = document.getElementById('sample-form');
    const sampleImageInput = document.getElementById('sample-image');
    const allowedImageTypes = new Set(['image/jpeg', 'image/png']);

    sampleForm?.addEventListener('submit', function(event) {
        const image = sampleImageInput?.files[0];
        if (image && !allowedImageTypes.has(image.type)) {
            event.preventDefault();
            alert('Envie a foto da amostra nos formatos PNG ou JPEG.');
            sampleImageInput.value = '';
        }
    });

    document.querySelectorAll('.btn-sample-details').forEach(function(button) {
        button.addEventListener('click', function() {
            toggleSampleDetails(button.dataset.sampleId, button);
        });
    });
});
