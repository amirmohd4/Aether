# 🚀 Render.com Deployment Guide

## Complete Aether GovOS Deployment in 5 Minutes

---

## ✅ Prerequisites

- Render.com account (free tier available)
- GitHub account
- This repository forked/cloned to your GitHub

---

## 📋 Step-by-Step Deployment

### **Step 1: Create PostgreSQL Database (2 minutes)**

1. **Go to Render Dashboard:** https://dashboard.render.com
2. **Click:** "New +" → "PostgreSQL"
3. **Fill in details:**
   ```
   Name: aether-postgres
   Database: aether_govos
   User: postgres
   Region: Choose nearest
   Plan: Free (sufficient for demo)
   ```
4. **Click:** "Create Database"
5. **Wait:** ~60 seconds for provisioning
6. **Copy:** Internal Database URL (format: `postgresql://user:pass@host/db`)
   - Find in database dashboard under "Connections"
   - Click "Internal Database URL" to copy

---

### **Step 2: Create Redis Instance (1 minute)**

1. **Click:** "New +" → "Redis"
2. **Fill in details:**
   ```
   Name: aether-redis
   Region: Same as PostgreSQL
   Plan: Free
   Max Memory: 25 MB (default)
   ```
3. **Click:** "Create Redis"
4. **Copy:** Internal Redis URL (format: `redis://host:port`)
   - Find in Redis dashboard under "Connections"

---

### **Step 3: Deploy Backend Service (3 minutes)**

1. **Click:** "New +" → "Web Service"
2. **Connect GitHub:**
   - If first time: Click "Connect Account"
   - Authorize Render to access your GitHub
3. **Select Repository:** Your Aether GovOS repo
4. **Fill in details:**
   ```
   Name: aether-backend
   Region: Same as database
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: sh -c "python -c 'from database import init_db; init_db()' && python /opt/render/project/src/../scripts/generate_mock_data.py && uvicorn main:app --host 0.0.0.0 --port $PORT"
   Plan: Free
   ```

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these variables:
   ```
   DATABASE_URL = <paste PostgreSQL internal URL>
   REDIS_URL = <paste Redis internal URL>
   ACTIVE_STATE = karnataka
   SECRET_KEY = aether-production-secret-key-change-this
   MOCK_FAILURE = false
   API_RATE_LIMIT = 100
   PYTHON_VERSION = 3.11
   ```

6. **Click:** "Create Web Service"
7. **Wait:** 3-5 minutes for build and deploy
8. **Copy Backend URL:** Will be like `https://aether-backend-xxxx.onrender.com`

---

### **Step 4: Deploy Frontend (2 minutes)**

1. **Click:** "New +" → "Static Site"
2. **Select Repository:** Same Aether GovOS repo
3. **Fill in details:**
   ```
   Name: aether-frontend
   Branch: main
   Root Directory: (leave empty or ".")
   Build Command: yarn install && yarn build
   Publish Directory: dist
   ```

4. **Add Environment Variable:**
   ```
   VITE_API_URL = <paste backend URL from Step 3>
   ```

5. **Click:** "Create Static Site"
6. **Wait:** 2-3 minutes for build
7. **Copy Frontend URL:** Will be like `https://aether-frontend-xxxx.onrender.com`

---

## ✅ Verification

### **Test Your Deployment:**

1. **Open Frontend URL** in browser
2. **Expected:** Aether GovOS homepage loads
3. **Click:** Property Search tab
4. **Expected:** See 10 property cards
5. **Click:** Any property
6. **Expected:** Property details display

### **API Health Check:**
```bash
curl https://aether-backend-xxxx.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Aether GovOS"
}
```

---

## 🔧 Troubleshooting

### **Backend Not Starting:**

1. **Check Logs:**
   - Go to backend service dashboard
   - Click "Logs" tab
   - Look for errors

2. **Common Issues:**
   - **Database connection failed:** Verify DATABASE_URL is correct (use internal URL)
   - **Redis connection failed:** Verify REDIS_URL is correct
   - **Module not found:** Check build command completed successfully

### **Frontend Not Loading:**

1. **Check Build Logs:**
   - Go to frontend service dashboard
   - Click "Events" tab
   - Verify build succeeded

2. **Common Issues:**
   - **API calls failing:** Check VITE_API_URL points to backend
   - **Blank page:** Check browser console for errors
   - **Build failed:** Verify package.json exists in root

### **Slow Performance:**

**Free Tier Limitations:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Solution: Upgrade to paid tier ($7/month) for always-on service

---

## 💰 Cost Breakdown

### **Free Tier (Perfect for Demo):**
```
PostgreSQL: Free (1 GB storage)
Redis: Free (25 MB)
Backend: Free (750 hours/month)
Frontend: Free (100 GB bandwidth)

Total: $0/month
```

### **Production Tier:**
```
PostgreSQL: $7/month (256 MB RAM, 1 GB disk)
Redis: $10/month (100 MB)
Backend: $7/month (always-on)
Frontend: Free (100 GB bandwidth)

Total: $24/month
```

---

## 🔄 Update Deployment

### **Auto-Deploy on Git Push:**

Render auto-deploys when you push to connected branch.

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will:
1. Detect push
2. Rebuild services
3. Deploy automatically
4. Zero downtime

### **Manual Deploy:**

1. Go to service dashboard
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

---

## 📊 Monitoring

### **Built-in Monitoring:**

1. **Metrics Dashboard:**
   - CPU usage
   - Memory usage
   - Request count
   - Response times

2. **Logs:**
   - Real-time log streaming
   - Last 7 days retained
   - Search and filter

3. **Alerts:**
   - Set up email alerts for:
     - Service down
     - High error rate
     - Resource limits

---

## 🌐 Custom Domain (Optional)

### **Add Custom Domain:**

1. **Go to Frontend Service**
2. **Click:** "Settings" → "Custom Domains"
3. **Click:** "Add Custom Domain"
4. **Enter:** Your domain (e.g., `demo.aether-govos.com`)
5. **Add DNS Records:**
   ```
   Type: CNAME
   Name: demo
   Value: aether-frontend-xxxx.onrender.com
   ```
6. **Wait:** DNS propagation (5-60 minutes)
7. **Verify:** Visit your custom domain

### **SSL Certificate:**
- Render provides free SSL automatically
- No configuration needed
- Auto-renews

---

## 🎯 Post-Deployment Checklist

- [ ] All 3 services showing "Live"
- [ ] Frontend loads in browser
- [ ] Backend API health check passes
- [ ] Property search returns data
- [ ] All 5 workflows functional
- [ ] Fraud detection working
- [ ] Dashboards showing statistics
- [ ] API marketplace accessible

---

## 📞 Support

### **Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Email: support@render.com

### **Aether GovOS Support:**
- GitHub Issues: https://github.com/aether-govos/platform/issues
- Email: support@aether-govos.com

---

## 🎉 Success!

**Your Aether GovOS is now live!**

Share your demo URL:
- Frontend: `https://aether-frontend-xxxx.onrender.com`
- API Docs: `https://aether-backend-xxxx.onrender.com/api/docs`

**Next Steps:**
- Share with stakeholders
- Gather feedback
- Customize for your needs
- Deploy to production

---

**🚀 Happy Deploying!**
