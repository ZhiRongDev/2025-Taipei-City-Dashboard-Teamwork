# Deployment Guide

## Quick Start

### Development Mode

```bash
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
```

The built files will be in the `dist/` folder.

## Deployment Options

### 1. GitHub Pages

#### Step 1: Update vite.config.js

```javascript
export default defineConfig({
  plugins: [vue()],
  base: "/2025-Taipei-City-Dashboard-Teamwork/", // Your repo name
  build: {
    outDir: "dist",
  },
});
```

#### Step 2: Build and Deploy

```bash
npm run build
git add dist -f
git commit -m "Deploy to GitHub Pages"
git subtree push --prefix dist origin gh-pages
```

#### Step 3: Enable GitHub Pages

- Go to repository Settings > Pages
- Select `gh-pages` branch
- Save

### 2. Netlify

#### Option A: Drag and Drop

1. Run `npm run build`
2. Drag the `dist/` folder to [Netlify Drop](https://app.netlify.com/drop)

#### Option B: Git Integration

1. Connect your GitHub repository
2. Build command: `npm run build`
3. Publish directory: `dist`

### 3. Vercel

```bash
npm i -g vercel
vercel
```

Or use the [Vercel Dashboard](https://vercel.com/):

- Import your GitHub repository
- Framework Preset: Vite
- Build Command: `npm run build`
- Output Directory: `dist`

### 4. AWS S3 + CloudFront

#### Step 1: Build

```bash
npm run build
```

#### Step 2: Upload to S3

```bash
aws s3 sync dist/ s3://your-bucket-name --delete
```

#### Step 3: Configure S3

- Enable Static Website Hosting
- Set Index document: `index.html`
- Set Error document: `index.html` (for SPA routing)

#### Step 4: CloudFront (Optional)

- Create CloudFront distribution
- Point to S3 bucket
- Set Default Root Object: `index.html`
- Custom Error Response: 404 -> /index.html (200)

### 5. Docker

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Build and run:

```bash
docker build -t taipei-dashboard .
docker run -p 8080:80 taipei-dashboard
```

## Environment Configuration

### MapBox Token

Create a `.env` file in the root directory and add your MapBox token:

```bash
VITE_MAPBOX_TOKEN=your_token_here
```

The application is configured to read this token automatically.

### Data Files

Ensure the `source/` directory is included in your deployment. The application loads data from:

- `/source/component_ready/*.csv`
- `/source/topic/taipei/*.csv`
- `/source/topic/newtaipeis/*.csv`
- `/source/clean/合併/*.geojson`

## Performance Optimization

### Code Splitting

To reduce initial bundle size, consider lazy-loading routes:

```javascript
// src/main.js
const routes = [
  { path: "/", component: () => import("./views/Overview.vue") },
  { path: "/aed", component: () => import("./views/AEDAnalysis.vue") },
  // ... other routes
];
```

### MapBox Optimization

- Use `mapbox-gl-js-cdn` for smaller bundle
- Load MapBox only when needed with dynamic import

### Data Optimization

- Pre-process large CSV files into JSON
- Use data compression (gzip)
- Implement data pagination for large tables

## Troubleshooting

### 404 on Refresh (SPA Routing)

Configure your server to always serve `index.html`:

**Netlify**: Create `public/_redirects`:

```
/*    /index.html   200
```

**Apache**: Create `.htaccess`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### MapBox Not Loading

- Check token validity
- Verify CORS settings
- Check browser console for errors

### Data Files Not Found

- Ensure `source/` folder is deployed
- Check file paths are correct
- Verify public directory configuration

## Monitoring

### Performance

- Use Lighthouse for performance audits
- Monitor Core Web Vitals
- Check bundle size with `npm run build`

### Analytics

Consider adding:

- Google Analytics
- Plausible Analytics
- Fathom Analytics

## Security

### CSP Headers

Add Content Security Policy headers:

```
default-src 'self';
script-src 'self' 'unsafe-eval';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
connect-src 'self' https://api.mapbox.com;
```

### Dependencies

Regularly update dependencies:

```bash
npm audit
npm update
```

## Support

For deployment issues:

1. Check browser console for errors
2. Verify all data files are accessible
3. Test MapBox token validity
4. Review server/CDN configuration
