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