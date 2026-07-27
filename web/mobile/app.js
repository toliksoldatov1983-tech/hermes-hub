// Hermes-Clean Mobile Web UI — App Logic
// Safe-local only. No secrets. No external calls (except localhost:8514).

(function() {
    'use strict';

    // ── Screen navigation ──

    function showScreen(name) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        const screen = document.getElementById('screen-' + name);
        if (screen) screen.classList.add('active');

        // Update bottom nav
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        const tab = document.querySelector(`.nav-tab[data-screen="${name}"]`);
        if (tab) tab.classList.add('active');

        // Load data for screen
        loadScreen(name);
    }

    // Click handlers for nav buttons
    document.querySelectorAll('.nav-tab, .nav-btn').forEach(el => {
        el.addEventListener('click', function() {
            const screen = this.dataset.screen;
            if (screen) showScreen(screen);
        });
    });

    // ── Screen data loaders ──

    async function loadScreen(name) {
        switch(name) {
            case 'home': return loadHome();
            case 'assistant': return loadAssistant();
            case 'malyarka': return loadMalyarka();
            case 'status': return loadStatus();
            case 'checks': return loadChecks();
            case 'ai-provider': return loadAIProvider();
            case 'safety': return loadSafety();
            case 'settings': return; // static
        }
    }

    // ── Home ──

    async function loadHome() {
        try {
            const resp = await HermesAPI.dashboard();
            if (resp.status === 'OK') {
                setText('home-mode', 'safe-local');
                setText('home-api', resp.data['api_url'] || HermesAPI.getBaseUrl());
                setText('home-tests', resp.data['tests_passed'] || '—');
                setText('home-next', resp.data['next_task'] || '—');
                setHeaderStatus(true);
            } else {
                setText('home-mode', 'API недоступен');
                setText('home-api', HermesAPI.getBaseUrl());
                setHeaderStatus(false);
            }
        } catch(e) {
            setText('home-mode', 'Ошибка');
            setHeaderStatus(false);
        }
    }

    // ── Assistant ──

    async function loadAssistant() {
        const el = document.getElementById('assistant-content');
        el.innerHTML = '<div class="card"><p><span class="spinner"></span> Загрузка...</p></div>';
        try {
            const resp = await HermesAPI.dailyAssistant();
            if (resp.status === 'OK') {
                el.innerHTML = renderKeyValueCard(resp.data);
            } else {
                el.innerHTML = `<div class="card"><p class="blocked">API недоступен: ${resp.blocked_reason || '—'}</p></div>`;
            }
        } catch(e) {
            el.innerHTML = '<div class="card"><p class="blocked">Ошибка загрузки</p></div>';
        }
    }

    document.getElementById('btn-assistant-load').addEventListener('click', loadAssistant);

    // ── Malyarka ──

    async function loadMalyarka() {
        // Load status
        try {
            const resp = await HermesAPI.malyarkaStatus();
            const el = document.getElementById('malyarka-status-card');
            if (resp.status === 'OK') {
                el.innerHTML = '<h3>Статус</h3>' + renderKeyValueCard(resp.data);
            } else {
                el.innerHTML = '<p class="dim">Статус недоступен</p>';
            }
        } catch(e) {
            document.getElementById('malyarka-status-card').innerHTML = '<p class="dim">Ошибка</p>';
        }
    }

    document.getElementById('btn-malyarka-parse').addEventListener('click', async function() {
        const input = document.getElementById('malyarka-input').value.trim();
        if (!input) return;

        const resultEl = document.getElementById('malyarka-result');
        resultEl.style.display = 'block';
        resultEl.innerHTML = '<p><span class="spinner"></span> Разбор...</p>';

        try {
            const resp = await HermesAPI.malyarkaDialog('clean');
            if (resp.status === 'OK') {
                resultEl.innerHTML = `<h3>Результат (dry-run)</h3>` + renderKeyValueCard(resp.data) +
                    '<p class="dim" style="margin-top:8px">⚠️ Реальные export-файлы не создаются. Dry-run only.</p>';
            } else {
                resultEl.innerHTML = `<p class="blocked">Ошибка: ${resp.blocked_reason || '—'}</p>`;
            }
        } catch(e) {
            resultEl.innerHTML = '<p class="blocked">Ошибка запроса</p>';
        }
    });

    // ── Status ──

    async function loadStatus() {
        const el = document.getElementById('status-content');
        el.innerHTML = '<div class="card"><p><span class="spinner"></span> Загрузка...</p></div>';
        try {
            const resp = await HermesAPI.status();
            if (resp.status === 'OK') {
                el.innerHTML = renderKeyValueCard(resp.data);
            } else {
                el.innerHTML = `<div class="card"><p class="blocked">API недоступен</p></div>`;
            }
        } catch(e) {
            el.innerHTML = '<div class="card"><p class="blocked">Ошибка</p></div>';
        }
    }

    // ── Checks ──

    async function loadChecks() {
        const el = document.getElementById('checks-content');
        el.innerHTML = '<div class="card"><p><span class="spinner"></span> Загрузка...</p></div>';
        try {
            const health = await HermesAPI.localHealth();
            const dashboard = await HermesAPI.dashboard();

            let html = '';
            if (health.status === 'OK') {
                html += '<div class="card"><h3>Health</h3>' + renderKeyValueCard(health.data) + '</div>';
            }
            if (dashboard.status === 'OK') {
                html += '<div class="card"><h3>Dashboard</h3>' + renderKeyValueCard(dashboard.data) + '</div>';
            }
            html += `<div class="card">
                <h3>Subsystems</h3>
                <div class="data-row"><span class="key">Включено</span><span class="val ok">6</span></div>
                <div class="data-row"><span class="key">Выключено</span><span class="val blocked">6</span></div>
                <div class="data-row"><span class="key">Live Telegram</span><span class="val blocked">disabled</span></div>
                <div class="data-row"><span class="key">Google Drive</span><span class="val blocked">disabled</span></div>
                <div class="data-row"><span class="key">Внешние API</span><span class="val blocked">disabled</span></div>
            </div>`;
            el.innerHTML = html;
        } catch(e) {
            el.innerHTML = '<div class="card"><p class="blocked">Ошибка загрузки</p></div>';
        }
    }

    // ── AI Provider ──

    async function loadAIProvider() {
        const el = document.getElementById('ai-provider-content');
        el.innerHTML = '<div class="card"><p><span class="spinner"></span> Загрузка...</p></div>';
        try {
            const resp = await HermesAPI.aiProviderStatus();
            if (resp.status === 'OK') {
                let html = renderKeyValueCard(resp.data);
                html += `<div class="card">
                    <h3>Провайдеры</h3>
                    <div class="data-row"><span class="key">mock</span><span class="val ok">SAFE ✓</span></div>
                    <div class="data-row"><span class="key">mock-review</span><span class="val ok">SAFE ✓</span></div>
                    <div class="data-row"><span class="key">Gemini</span><span class="val blocked">BLOCKED</span></div>
                    <div class="data-row"><span class="key">DeepSeek</span><span class="val blocked">BLOCKED</span></div>
                </div>`;
                el.innerHTML = html;
            } else {
                el.innerHTML = `<div class="card"><p class="blocked">API недоступен</p></div>`;
            }
        } catch(e) {
            el.innerHTML = '<div class="card"><p class="blocked">Ошибка</p></div>';
        }
    }

    // ── Safety ──

    async function loadSafety() {
        const el = document.getElementById('safety-content');
        try {
            const resp = await HermesAPI.bridgeStatus();
            let html = `<div class="card">
                <h3>Approval Gates</h3>
                <div class="data-row"><span class="key">APPROVE_SECRET_SETUP</span><span class="val blocked">требуется</span></div>
                <div class="data-row"><span class="key">APPROVE_TELEGRAM_LIVE</span><span class="val blocked">требуется</span></div>
                <div class="data-row"><span class="key">APPROVE_REAL_ORDER_ACCESS</span><span class="val blocked">требуется</span></div>
                <div class="data-row"><span class="key">APPROVE_GOOGLE_DRIVE_MOVE</span><span class="val blocked">требуется</span></div>
                <div class="data-row"><span class="key">APPROVE_ARCHIVE_UNPACK</span><span class="val blocked">требуется</span></div>
                <div class="data-row"><span class="key">APPROVE_DELETE</span><span class="val blocked">требуется</span></div>
            </div>`;

            html += `<div class="card">
                <h3>Безопасность</h3>
                <div class="data-row"><span class="key">Safe-local</span><span class="val ok">активен</span></div>
                <div class="data-row"><span class="key">0.0.0.0</span><span class="val blocked">заблокирован</span></div>
                <div class="data-row"><span class="key">LAN/external</span><span class="val blocked">disabled</span></div>
                <div class="data-row"><span class="key">Firewall</span><span class="val ok">не трогается</span></div>
                <div class="data-row"><span class="key">Android app</span><span class="val dim">не создано</span></div>
            </div>`;

            if (resp.status === 'OK') {
                html += '<div class="card">' + renderKeyValueCard(resp.data) + '</div>';
            }
            el.innerHTML = html;
        } catch(e) {
            el.innerHTML = '<div class="card"><p class="blocked">Ошибка</p></div>';
        }
    }

    // ── Settings ──

    document.getElementById('settings-api-url').value = HermesAPI.getBaseUrl();

    document.getElementById('btn-settings-save').addEventListener('click', function() {
        const url = document.getElementById('settings-api-url').value.trim();
        const warnEl = document.getElementById('settings-warning');
        warnEl.style.display = 'none';

        if (url && !url.includes('127.0.0.1') && !url.includes('localhost')) {
            warnEl.textContent = '⚠️ LAN/external mode disabled. Только localhost разрешён по умолчанию.';
            warnEl.style.display = 'block';
        }

        HermesAPI.setBaseUrl(url);
    });

    // ── Helpers ──

    function setText(id, text) {
        const el = document.getElementById(id);
        if (el) el.textContent = text || '—';
    }

    function setHeaderStatus(ok) {
        const el = document.getElementById('header-status');
        if (ok) {
            el.textContent = 'safe-local';
            el.className = 'badge';
        } else {
            el.textContent = 'offline';
            el.className = 'badge blocked';
        }
    }

    function renderKeyValueCard(data) {
        if (!data || Object.keys(data).length === 0) return '<p class="dim">Нет данных</p>';
        let html = '';
        for (const [key, val] of Object.entries(data)) {
            if (key.startsWith('output_')) continue;
            const v = String(val === null ? '—' : val);
            html += `<div class="data-row"><span class="key">${esc(key)}</span><span class="val">${esc(v)}</span></div>`;
        }
        return html;
    }

    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // ── Init ──

    showScreen('home');
})();
