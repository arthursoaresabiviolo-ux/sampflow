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