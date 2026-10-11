# Free-tier Django hosting: Render + Neon + Cloudinary

This setup is for demos and development. Free services are not guaranteed to
stay free, always-on, or production-grade. Never use a free preview as a
client SLA without a separate reliability and security review.

## 1. PostgreSQL: Neon

1. Open https://console.neon.tech/ and create a **Free** PostgreSQL project.
2. In **Connect**, copy the connection string. Keep it private.
3. Prefer a region geographically close to your Render web service if
   available. Use a direct Neon connection string for migrations.
4. Keep a separate backup of any valuable data. A brand-new database will
   have no users or products until migrations and data import complete.

## 2. Product images: Cloudinary

1. Create a free account at https://cloudinary.com/.
2. Obtain the private `CLOUDINARY_URL` value from account settings.
3. Do not expose the Cloudinary API secret to the React Native app.
4. This is required by the Render settings so uploaded product images do
   not disappear after a free instance restart.

## 3. Django web service: Render

1. Open https://dashboard.render.com/ and link your GitHub account.
2. Create a Blueprint using this repository's
   `feature/client-ready-marketplace` branch and `render.yaml`.
   Alternatively, select **New -> Web Service**, choose the same branch,
   **Python**, **Free** instance and **Singapore** region, then set:
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
   - Start: `gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`
3. Configure **environment variables** in the Render dashboard:
   - `DJANGO_SECRET_KEY`: generate a fresh, random secret (Blueprint generates it).
   - `DATABASE_URL`: the Neon PostgreSQL URL (private).
   - `CLOUDINARY_URL`: the Cloudinary media URL (private).
   - `DEBUG`: `False`.
4. If you use a custom domain, set `ALLOWED_HOSTS` to the hostname (without
   https://) and, if you use a web browser client, add the browser origin
   to `CORS_ALLOWED_ORIGINS`. Render's generated .onrender.com host is
   discovered automatically by Django.
5. After deployment, open `https://YOUR-SERVICE.onrender.com/` to verify the
   backend success message and `https://YOUR-SERVICE.onrender.com/api/products/`
   to verify the API (a new database may return an empty array).

## 4. Mobile app configuration

In the **Frontend-repo** root, create a local file called `.env`:

```dotenv
EXPO_PUBLIC_API_URL=https://YOUR-SERVICE.onrender.com
```

Use your actual Render URL **without** the trailing slash or `/api`.
The value is a public API host, *not* a secret. The mobile repo ignores
`.env` in git. Run `git pull` on the frontend feature branch and restart:

```powershell
npx.cmd expo start --go --clear
```

Scan the QR code in Expo Go. Initial requests can be delayed while
the Render service wakes from idle.

## 5. Data, safety, and costs

- This is a NEW empty PostgreSQL database. Railway data does not transfer
  automatically; you need a backup/export of the old database to import it.
- Rotate any secrets from older commits or old deployments. Removing
  `myproject/.env` from the latest tree does not remove it from Git history.
- Do not put any `DATABASE_URL`, `DJANGO_SECRET_KEY`, or `CLOUDINARY_URL`
  in React Native's `EXPO_PUBLIC_*` variables.
- Render free instances sleep and have shared usage limits; Neon and
  Cloudinary also have usage limits. Account eligibility and plans may change.
- Validate privacy, authorization, error handling, backup recovery, and
  Android releases before handing this project to a paying client.
