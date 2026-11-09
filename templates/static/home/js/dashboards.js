// Dashboard tab: monthly shipment-cost summary.
(function () {
    const dataElement = document.getElementById('dashboard-cost-data');
    const monthInput = document.getElementById('dashboard-month');
    if (!dataElement || !monthInput) return;

    let costs = [];
    try { costs = JSON.parse(dataElement.textContent); } catch (error) { return; }

    const formatter = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    const dateFormatter = new Intl.DateTimeFormat('pt-BR', { timeZone: 'UTC' });
    const monthFormatter = new Intl.DateTimeFormat('pt-BR', { month: 'long', year: 'numeric', timeZone: 'UTC' });
    const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[character]);

    const latestMonth = costs.reduce((latest, item) => item.date.slice(0, 7) > latest ? item.date.slice(0, 7) : latest, '');
    monthInput.value = latestMonth || new Date().toISOString().slice(0, 7);

    function render() {
        const selectedMonth = monthInput.value;
        const monthlyCosts = costs.filter((item) => item.date.startsWith(selectedMonth));
        const total = monthlyCosts.reduce((sum, item) => sum + Number(item.cost), 0);
        const average = monthlyCosts.length ? total / monthlyCosts.length : 0;
        const selectedDate = selectedMonth ? new Date(`${selectedMonth}-01T00:00:00Z`) : null;
        document.getElementById('dashboard-total-cost').textContent = formatter.format(total);
        document.getElementById('dashboard-sample-count').textContent = monthlyCosts.length;
        document.getElementById('dashboard-average-cost').textContent = formatter.format(average);
        document.getElementById('dashboard-period-label').textContent = selectedDate ? monthFormatter.format(selectedDate) : 'Selecione um mês';

        const costsByClient = monthlyCosts.reduce((accumulator, item) => {
            accumulator[item.client] = (accumulator[item.client] || 0) + Number(item.cost);
            return accumulator;
        }, {});
        const clientBreakdown = Object.entries(costsByClient).sort(([, a], [, b]) => b - a);
        document.getElementById('dashboard-client-breakdown').innerHTML = clientBreakdown.length
            ? clientBreakdown.map(([client, cost]) => `<div class="client-cost-row"><div class="client-cost-info"><span>${escapeHtml(client)}</span><span>${formatter.format(cost)}</span></div><div class="cost-progress"><span style="width: ${total ? (cost / total) * 100 : 0}%"></span></div></div>`).join('')
            : '<p class="dashboard-empty">Não há custos de envio registrados neste mês.</p>';

        document.getElementById('dashboard-cost-table').innerHTML = monthlyCosts.length
            ? monthlyCosts.map((item) => `<tr><td>${dateFormatter.format(new Date(`${item.date}T00:00:00Z`))}</td><td>${escapeHtml(item.contract)}</td><td>${escapeHtml(item.client)}</td><td>${escapeHtml(item.sample_type)}</td><td>${escapeHtml(item.courier)}</td><td>${formatter.format(item.cost)}</td></tr>`).join('')
            : '<tr><td colspan="6" class="dashboard-empty">Nenhuma amostra com custo e data de envio foi encontrada para este mês.</td></tr>';
    }

    monthInput.addEventListener('change', render);
    render();
}());
