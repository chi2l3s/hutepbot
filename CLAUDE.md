# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Telegram bot (`hutepbot`) that sells VPN subscriptions. Users pick a plan, pay via Telegram Stars or CryptoBot, and the bot provisions a client on a self-hosted 3x-ui-style VPN panel. Russian-language UI.

## Stack

- Python + [aiogram](https://docs.aiogram.dev) v3 (async Telegram framework, FSM via `states.py`)
- SQLAlchemy 2.x async + asyncpg, Postgres 17 (via docker-compose)
- Alembic for migrations
- `aiocryptopay` for CryptoBot invoices (currently `Networks.TEST_NET` in [services/crypto.py](services/crypto.py))
- `hutep_vpn/` is a generated OpenAPI client for the 3x-ui VPN panel — **do not hand-edit**, regenerate if the panel API changes
- `loguru` for logging (configured in [logger.py](logger.py))

## Commands

All commands run from repo root. Use the venv at `.venv/`.

```bash
# Start Postgres (reads POSTGRES_* from .env)
docker-compose up -d

# Run the bot
python bot.py

# Migrations
alembic upgrade head
alembic revision --autogenerate -m "message"
alembic downgrade -1
```

No test suite, linter, or formatter is configured.

## Required env vars (.env)

`BOT_TOKEN`, `DATABASE_URL` (asyncpg DSN), `POSTGRES_DB/USER/PASSWORD`, `VPN_BASE_URL`, `VPN_API_TOKEN`, `VPN_BASE_SUB`, `CRYPTO_BOT_TOKEN`.

## Architecture

Entry point [bot.py](bot.py) wires aiogram up: creates `Bot` + `Dispatcher`, registers `DbSessionMiddleware` (opens an `AsyncSession` per update and injects it as `session=` kwarg into every handler), and includes the routers from `handlers/`. Each handler module owns one `Router` named after its concern (`start`, `terms`, `support`, `profile`, `purchase`).

**Important:** [bot.py](bot.py) currently forces all Telegram traffic through a hardcoded local HTTP proxy `http://127.0.0.1:12334` via `AiohttpSession`. The bot will not connect without that proxy running (or the line removed).

### Purchase flow (the core path)

Driven by `PaymentState` FSM in [states.py](states.py) and `PLANS` dict in [constants.py](constants.py) (the canonical source of plan keys, prices in ₽, Stars amounts, durations).

1. User clicks `purchase` → [handlers/purchase.py](handlers/purchase.py) shows `plans_keyboard` (state: `choosing_plan`).
2. User picks a plan key from `PLANS` → state becomes `choosing_method`, plan_key stored in FSM data.
3. Two payment branches:
   - **Stars**: `answer_invoice` with `currency='XTR'`. Telegram fires `successful_payment` → handler calls `create_payment` directly (note: this branch does NOT go through `activate_subscription` and does NOT provision the VPN client — see Known issues).
   - **Crypto**: `services.crypto.create_invoice` returns a CryptoBot mini-app URL. User clicks "Я оплатил" → `check_payment` polls CryptoBot for paid invoices matching the `{plan_key}:{user_id}` payload → `services.subscription.activate_subscription` runs.

### `activate_subscription` ([services/subscription.py](services/subscription.py))

The single place that should provision/extend a VPN client and record a payment. It calls `vpn_service.get_client(user_id)` first; if absent, calls `create_client` on the panel (inbound id `4`, hardcoded) and stores a `Subscription` row keyed by the panel's `subId`. The user's Telegram ID is used verbatim as the panel `email` field.

### Database

Three models in [db/models.py](db/models.py): `User` (PK = telegram id), `Subscription` (one row per provisioned VPN client, keyed by `sub_id` from the panel), `Payment` (audit row per transaction, `provider` = `'stars'` or `'cryptobot'`). All access goes through helpers in [db/repository.py](db/repository.py) — handlers receive a session from the middleware and pass it in.

## Known issues / gotchas

- **Stars payment doesn't activate VPN.** [handlers/purchase.py](handlers/purchase.py:88) uses `F.successfull_payment` (typo, should be `F.successful_payment`) and only calls `create_payment` — it never calls `activate_subscription`, so no VPN client is provisioned for Stars purchases.
- **`profile` handler is broken.** [handlers/profile.py](handlers/profile.py:15) casts `user_id` to `str` before passing to `get_active_subscription`, but the column is `BigInteger`. Also `format_time` expects ms but receives a `datetime`.
- **Duplicate `back_main` handler.** Both [handlers/profile.py](handlers/profile.py) and [handlers/support.py](handlers/support.py) register `F.data == 'back_main'` callbacks. aiogram dispatches to the first match (profile, registered earlier in [bot.py](bot.py:29)).
- **CryptoBot is on testnet.** [services/crypto.py](services/crypto.py:13) uses `Networks.TEST_NET` — switch to `Networks.MAIN_NET` before production.
- **Subscription month math is approximate** — `months * 30` days, not calendar months ([db/repository.py](db/repository.py:15), [services/vpn.py](services/vpn.py:43)).
- **Multiple `_fix_datetime` migrations** exist in [alembic/versions/](alembic/versions/); review history before adding new schema changes.
