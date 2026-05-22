# GoLocalChina — Deployment Guide (Vercel + Railway)

**Cost: $0/month** on free tiers. HTTPS included. Custom domain supported.

---

## Step 1: Deploy Backend to Railway (5 min)

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `Ilovecodinghhh/golocalchina`
4. Railway will auto-detect — set these:
   - **Root Directory:** `golocalchina-api`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Railway dashboard:
   ```
   JWT_SECRET_KEY=<generate a random 64-char string>
   CORS_ORIGINS=https://golocalchina.vercel.app
   ```
6. Click **Deploy** → Railway gives you a URL like `golocalchina-api-production.up.railway.app`
7. Test: visit `https://YOUR_RAILWAY_URL/health` — should show `{"status":"ok"}`

---

## Step 2: Deploy Frontend to Vercel (5 min)

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click **"Add New Project"** → Import `Ilovecodinghhh/golocalchina`
3. Configure:
   - **Root Directory:** `golocalchina-web`
   - **Framework:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Click **Deploy** → Vercel gives you `golocalchina.vercel.app`

---

## Step 3: Connect Frontend → Backend (2 min)

1. In your Vercel project, go to **Settings → Environment Variables**
2. (The API URL is already configured in `vercel.json` — just update it)
3. Edit `golocalchina-web/vercel.json` in GitHub:
   ```json
   "rewrites": [
     { "source": "/api/:path*", "destination": "https://YOUR_RAILWAY_URL.up.railway.app/api/:path*" }
   ]
   ```
4. Push the change → Vercel auto-redeploys

---

## Step 4: Custom Domain (optional, $10/year)

1. Buy a domain (e.g., `golocalchina.com`) from Namecheap or Cloudflare
2. In Vercel: **Settings → Domains → Add** `golocalchina.com`
3. Point your domain's DNS to Vercel (they give you the records)
4. HTTPS is automatic

---

## That's It!

Your live URLs:
- **Frontend:** `https://golocalchina.vercel.app` (or your custom domain)
- **Backend API:** `https://YOUR_RAILWAY_URL.up.railway.app/health`
- **API Docs:** `https://YOUR_RAILWAY_URL.up.railway.app/docs`

Both have HTTPS, auto-deploy on git push, and cost $0.
