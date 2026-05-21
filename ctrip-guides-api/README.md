# Ctrip-Guides API

> Information service platform connecting foreign tourists with independently licensed tour guides in China.
> **This platform is NOT a travel agency (非旅行社).**

## Quick Start

```bash
# 1. Start services
docker-compose up -d

# 2. Run migrations
alembic upgrade head

# 3. API is at http://localhost:8000
# Docs: http://localhost:8000/docs
```

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/auth/register` | Register tourist or guide | No |
| POST | `/api/v1/auth/login` | Login, get JWT tokens | No |
| GET | `/api/v1/guides` | Search guides (city, language, specialty) | No |
| GET | `/api/v1/guides/{id}` | Guide detail + published listings | No |
| POST | `/api/v1/service-requests` | Request to connect with a guide | JWT |
| GET | `/api/v1/service-requests/mine` | List my service requests | JWT |
| GET | `/health` | Health check | No |

## Environment Variables

See `.env.example` for all configuration options.

## Path B Legal Compliance

This codebase follows Path B (pure information platform) constraints:
- No "tour", "package", or "booking" terminology — uses "service request", "connection", "listing"
- Guides set their own prices — platform does NOT control pricing
- Platform fee is labeled "信息服务费" (Information Service Fee), not "commission"
- Guides are independent contractors — no employment relationship implied
- All guide-authored content is owned by the guide
