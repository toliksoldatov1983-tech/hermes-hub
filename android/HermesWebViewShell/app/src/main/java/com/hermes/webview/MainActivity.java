package com.hermes.webview;

import android.annotation.SuppressLint;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

/**
 * Hermes-Clean Android WebView Shell.
 *
 * Safe-local mode. Opens Mobile Web UI.
 * Default URL: http://127.0.0.1:8514
 * LAN/external mode: DISABLED.
 */
public class MainActivity extends AppCompatActivity {

    private static final String PREF_NAME = "hermes_prefs";
    private static final String KEY_API_URL = "api_url";
    private static final String DEFAULT_API_URL = "http://127.0.0.1:8514";

    private WebView webView;
    private EditText urlInput;
    private TextView statusText;
    private TextView warningText;
    private SharedPreferences prefs;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prefs = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        String apiUrl = prefs.getString(KEY_API_URL, DEFAULT_API_URL);

        // Views
        webView = findViewById(R.id.webview);
        urlInput = findViewById(R.id.url_input);
        statusText = findViewById(R.id.status_text);
        warningText = findViewById(R.id.warning_text);
        Button openBtn = findViewById(R.id.btn_open);
        Button checkBtn = findViewById(R.id.btn_check_api);
        Button saveBtn = findViewById(R.id.btn_save_url);

        urlInput.setText(apiUrl);
        updateWarning(apiUrl);

        // ── WebView security settings ──
        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);       // Required for Mobile Web UI
        ws.setDomStorageEnabled(true);       // Required for localStorage (API URL cache)
        ws.setAllowFileAccess(false);        // BLOCKED: no file access
        ws.setAllowContentAccess(false);     // BLOCKED: no content access
        ws.setAllowFileAccessFromFileURLs(false);
        ws.setAllowUniversalAccessFromFileURLs(false);
        ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        ws.setSavePassword(false);           // BLOCKED: no password saving
        ws.setSaveFormData(false);           // BLOCKED: no form data saving

        // No Android JS bridge (BLOCKED)
        // webView.addJavascriptInterface(...); // NOT added

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                statusText.setText("Загружено: " + url);
            }

            @Override
            public void onReceivedError(WebView view, int errorCode,
                                        String description, String failingUrl) {
                statusText.setText("Ошибка: " + description);
                webView.setVisibility(View.GONE);
                findViewById(R.id.error_screen).setVisibility(View.VISIBLE);
            }
        });

        // ── Buttons ──
        openBtn.setOnClickListener(v -> {
            String url = urlInput.getText().toString().trim();
            if (!url.isEmpty()) {
                statusText.setText("Загрузка...");
                webView.setVisibility(View.VISIBLE);
                findViewById(R.id.error_screen).setVisibility(View.GONE);
                webView.loadUrl(url);
            }
        });

        checkBtn.setOnClickListener(v -> {
            String url = urlInput.getText().toString().trim();
            String checkUrl = url.replaceAll("/$", "") + "/api/status";
            Toast.makeText(this, "Проверка API: " + checkUrl, Toast.LENGTH_SHORT).show();
            webView.loadUrl(checkUrl);
        });

        saveBtn.setOnClickListener(v -> {
            String url = urlInput.getText().toString().trim();
            prefs.edit().putString(KEY_API_URL, url).apply();
            updateWarning(url);
            Toast.makeText(this, "Сохранено: " + url, Toast.LENGTH_SHORT).show();
        });

        // Auto-load on start
        webView.loadUrl(apiUrl);
    }

    private void updateWarning(String url) {
        if (url.contains("127.0.0.1") || url.contains("localhost")) {
            warningText.setText(
                "⚠️ Safe-local shell. 127.0.0.1 на телефоне = сам телефон, а не ПК.\n" +
                "Для доступа к Hermes-Clean на ПК нужен будущий LAN/Tailscale/VPN режим."
            );
            warningText.setVisibility(View.VISIBLE);
        } else {
            warningText.setText(
                "⚠️ LAN/external mode DISABLED.\n" +
                "Требуется APPROVE_LAN_MODE для доступа к Hermes-Clean на ПК."
            );
            warningText.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
