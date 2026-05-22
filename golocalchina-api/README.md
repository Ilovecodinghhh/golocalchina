# GoLocalChina API

> Information service platform connecting foreign tourists with independently licensed tour guides in China.
> **This platform is NOT a travel agency (非旅行社). We do not process payments.**

## Quick Start

```bash
docker-compose up -d
# API at http://localhost:8000/docs
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

## Business Model

- **Free for tourists and guides** — no platform fees, no commissions
- **Tourist pays guide directly** at time of service (cash, Alipay, WeChat Pay)
- **Revenue via advertising** — travel affiliates, sponsored listings, display ads

## Path B Legal Compliance

- Pure information platform — we facilitate connections, not transactions
- Guide sets own prices — platform does NOT control pricing
- No payment processing — zero fund custody, zero PBOC license risk
- PIPL + GDPR dual compliance structure
