# file-sharing-drf

A small file-sharing REST API built with Django REST Framework, backed by Postgres and S3-compatible object storage ([Garage](https://garagehq.deuxfleurs.fr/)), running behind Traefik in Docker Compose.

Built as a learning/portfolio project to get hands-on with DRF, JWT auth, object storage, and containerized local dev — not a production service.

## Stack

- **Django / Django REST Framework** — API layer
- **PostgreSQL** — relational data (users, file metadata)
- **Garage** — self-hosted, S3-compatible object storage for the actual file bytes, via `django-storages`
- **djangorestframework-simplejwt** — JWT authentication
- **Traefik** — reverse proxy / routing for local multi-container setup
- **pytest** — test suite

## Features

- JWT-based authentication (`/api/token/`, `/api/token/refresh`)
- Upload, list, retrieve, and delete files, with metadata (title, extension, size) tracked in Postgres and file bytes stored in Garage
- Ownership-scoped write access — a user can only delete their own files (enforced via a custom `IsOwnerOrReadOnly` permission, and covered by tests)
- Server-side file size limit, enforced before the file is accepted
- Paginated list endpoints

## API

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/token/` | — | Obtain JWT access/refresh token pair |
| POST | `/api/token/refresh` | — | Refresh an access token |
| GET | `/api/v1/files` | — | List files (public — see *Design notes*) |
| POST | `/api/v1/files` | Required | Upload a file |
| GET | `/api/v1/files/<id>` | — | Retrieve file metadata + download URL |
| DELETE | `/api/v1/files/<id>` | Owner only | Delete a file (removed from both Postgres and object storage) |
| GET | `/api/v1/users` | — | List users |
| GET | `/api/v1/users/<id>` | — | Retrieve a user and their files |
| POST | `/api/v1/logout` | — | Logout with Blacklisting |
| GET/POST | `/auth` | — | DRF browsable-API session login |

## Running locally

Requires Docker, and a local hosts entry for the Traefik routing to work (`site.test`, `garage.site.test` → `127.0.0.1`).

1. Copy the env template and fill in Postgres credentials + Garage tokens:
   ```bash
   cp .env_example .env
   ```
2. Bring up the stack:
   ```bash
   docker compose up -d
   ```
3. Bootstrap Garage (first run only — see `garage.toml` for the running config):
   ```bash
   docker compose exec garage /garage status        # copy the node ID
   docker compose exec garage /garage layout assign -z <zone> -c <capacity> <node_id>
   docker compose exec garage /garage layout apply --version 1
   docker compose exec garage /garage bucket create <bucket_name>
   docker compose exec garage /garage key create <key_name>   # copy key_id / secret into .env
   docker compose exec garage /garage bucket allow --read --write --owner <bucket_name> --key <key_name>
   ```
4. Run migrations and create an account (there's no self-service signup — see *Design notes*):
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
5. API is now served at `http://site.test/`.

### Tests

```bash
pytest
```

## Design notes / known limitations

Documented deliberately, since some of these look like bugs out of context but are scoping decisions:

- **File and user listings are public by design.** `GET /api/v1/files` and `GET /api/v1/users` aren't scoped to the requesting user — only *writes* (create/delete) are ownership-restricted. This makes the app behave like a public file-sharing board rather than a private drive. If it were headed toward private-by-default storage, the read side would need the same ownership scoping the write side already has.
- **No self-service registration.** Accounts are created via `createsuperuser`/Django admin only. Fine for a small personal deployment; a real signup flow would be a prerequisite for opening this up further.
- **No orphan-storage reconciliation.** If a delete fails to remove the object from Garage (network blip, bad credentials) after the Postgres row is already gone, the app logs it and moves on rather than blocking the user's delete or retrying. That trades a slow, rare storage leak for a delete path that never gets stuck — a deliberate call, not an oversight, but a real gap if this ever needed to run unattended for a long time.
- **No rate limiting yet.** Nothing currently throttles repeated requests (login included). Acceptable for a local/personal deployment; would need `DEFAULT_THROTTLE_CLASSES` (and a tighter scope specifically on `/api/token/`) before any public exposure.
- **No token revocation.** Refresh tokens can't currently be invalidated early (no logout, no blacklist). A stolen refresh token stays valid until it naturally expires.

## What I'd do next

- Decide on and implement a storage-reconciliation job for the delete-failure edge case
- Add a real signup flow if this ever needs multi-tenant use beyond me
