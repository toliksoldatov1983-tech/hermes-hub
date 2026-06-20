# Local Demo Runbook

Date: 2026-06-17 | No server, no live

## 1. Fake Telegram Clean Order

```bash
python agents/local_simulation/full_chain_sales_malyarka_corel/run_full_chain_simulation.py
```
→ Full chain to Corel contract, production_ready=false

## 2. Fake Telegram Disputed Order

```bash
python agents/telegram_safe_adapter_agent/src/fake_full_chain_simulation.py
```
→ Blocked at Sales, review_required=true

## 3. Adapter Blocked Production Action

```python
process_telegram_event({"text": "production order"})
```
→ blocked, forbidden_action

## 4. Token-Like Blocked Input

```python
process_telegram_event({"text": "BOT_TOKEN"})
```
→ blocked, unsafe_secret_like_input

## 5. Safe Copy Chain Pass

Gate 2: ORDER_SAFE_COPY_001 → full chain pass

## 6. Disputed Safe Copy Blocked

Gate 3: ORDER_SAFE_COPY_002 → correctly blocked

## All Demos

- No server, no live, no secrets
- All results: not_final, production_ready=false
