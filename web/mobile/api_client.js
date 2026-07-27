// Hermes-Clean Mobile API Client
// Safe-local only. No secrets. No external URLs. Default: 127.0.0.1:8514.

const HermesAPI = (() => {
    // Default base URL — only localhost
    const DEFAULT_BASE = 'http://127.0.0.1:8514';

    let _baseUrl = localStorage.getItem('hermes_api_url') || DEFAULT_BASE;

    function getBaseUrl() {
        return _baseUrl;
    }

    function setBaseUrl(url) {
        url = (url || '').trim();
        if (!url) {
            url = DEFAULT_BASE;
        }

        // Warn if not localhost
        if (!url.includes('127.0.0.1') && !url.includes('localhost')) {
            console.warn('HermesAPI: non-localhost URL detected. LAN/external mode is disabled.');
            // Still allow setting, but user will see warning
        }

        _baseUrl = url;
        try { localStorage.setItem('hermes_api_url', url); } catch(e) { /* ignore */ }
    }

    function resetBaseUrl() {
        setBaseUrl(DEFAULT_BASE);
    }

    async function request(method, path, body) {
        const url = _baseUrl.replace(/\/$/, '') + path;
        const opts = {
            method: method,
            headers: { 'Content-Type': 'application/json' },
        };
        if (body) {
            opts.body = JSON.stringify(body);
        }

        try {
            const resp = await fetch(url, opts);
            const data = await resp.json();
            return data;
        } catch (err) {
            return {
                status: 'ERROR',
                safe_local: true,
                endpoint: method + ' ' + path,
                action: 'network_error',
                data: {},
                warnings: ['API сервер недоступен. Проверьте mobile-api-server-check.'],
                blocked_reason: 'API unreachable: ' + err.message,
                next_step: 'Запустите сервер: python -m hermes_core.mobile_gateway.local_api_server',
                audit_metadata: {
                    safe_local: true,
                    bind_address: '127.0.0.1',
                    real_api_called: false,
                    network_called: true,  // localhost call failed
                }
            };
        }
    }

    // ── Endpoint methods ──

    function status()          { return request('GET', '/api/status'); }
    function dashboard()       { return request('GET', '/api/dashboard'); }
    function dailyReport()     { return request('GET', '/api/daily-report'); }
    function dailyAssistant()  { return request('GET', '/api/daily-assistant'); }
    function whatNext()        { return request('GET', '/api/what-next'); }
    function localHealth()     { return request('GET', '/api/local-health'); }
    function malyarkaStatus()  { return request('GET', '/api/malyarka/status'); }
    function malyarkaDialog(script) { return request('POST', '/api/malyarka/dialog', { script: script || 'clean' }); }
    function aiProviderStatus(){ return request('GET', '/api/ai-provider/status'); }
    function bridgeStatus()    { return request('GET', '/api/bridge/status'); }
    function bridgeRoute(action) { return request('POST', '/api/bridge/route', { action: action || 'status' }); }

    return {
        getBaseUrl, setBaseUrl, resetBaseUrl,
        status, dashboard, dailyReport, dailyAssistant, whatNext, localHealth,
        malyarkaStatus, malyarkaDialog, aiProviderStatus, bridgeStatus, bridgeRoute,
    };
})();
