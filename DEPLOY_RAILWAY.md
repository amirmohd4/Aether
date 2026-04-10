# 🚂 Railway Deployment Guide

## Deploy Aether GovOS in 3 Clicks

---

## Why Railway?

- ✅ **Simplest deployment** - Auto-detects docker-compose.yml
- ✅ **One-click setup** - No configuration needed
- ✅ **Free $5 credit** - Enough for demo/testing
- ✅ **Auto SSL** - HTTPS automatically
- ✅ **Zero config** - Just connect GitHub

---

## 🚀 Quick Deploy (3 Minutes)

### **Step 1: Prepare Repository**

1. **Fork or clone** this repository to your GitHub account
2. **Ensure** docker-compose.yml is in the root directory

---

### **Step 2: Deploy on Railway**

#### **Option A: One-Click Deploy (Recommended)**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/aether-govos)

1. Click the button above
2. Sign in with GitHub
3. Click "Deploy Now"
4. Wait 3-5 minutes
5. **Done!** ✅

---

#### **Option B: Manual Deploy**

1. **Go to:** https://railway.app
2. **Sign in** with GitHub
3. **Click:** "New Project"
4. **Select:** "Deploy from GitHub repo"
5. **Choose:** Your Aether GovOS repository
6. **Railway detects** docker-compose.yml automatically
7. **Click:** "Deploy"
8. **Wait:** 3-5 minutes for deployment

---

### **Step 3: Access Your Application**

1. **Go to** Railway dashboard
2. **Click** on your project
3. **Click** "frontend" service
4. **Click** "Settings" tab
5. **Find:** "Public Networking" section
6. **Click:** "Generate Domain"
7. **Copy** the URL (e.g., `aether-govos-production.up.railway.app`)
8. **Open** URL in browser

---

## ⚙️ Configuration

### **Environment Variables (Auto-Set)**

Railway automatically sets:
```
DATABASE_URL - PostgreSQL connection
REDIS_URL - Redis connection
PORT - Service port
```

### **Custom Variables (Optional)**

Add these in Railway dashboard:

1. **Click** service (backend)
2. **Click** "Variables" tab
3. **Add:**
   ```
   ACTIVE_STATE=karnataka
   SECRET_KEY=your-secret-key
   API_RATE_LIMIT=100
   ```

---

## 📊 Monitoring

### **View Logs:**
```
1. Click service
2. Click "Deployments" tab
3. Click latest deployment
4. View real-time logs
```

### **Resource Usage:**
```
1. Click service
2. Click "Metrics" tab
3. View CPU, Memory, Network
```

---

## 💰 Pricing

### **Free Tier:**
```
$5 free credit on signup
Enough for ~500 hours
Perfect for demos
```

### **Hobby Plan:**
```
$5/month
Unlimited projects
Always-on services
Custom domains
```

### **Pro Plan:**
```
$20/month
Priority support
Advanced metrics
Team collaboration
```

---

## 🔄 Updates

### **Auto-Deploy:**

Push to GitHub = Auto-deploy on Railway

```bash
git add .
git commit -m "Update"
git push origin main
```

Railway deploys automatically! ✨

---

## 🌐 Custom Domain

1. **Go to** service settings
2. **Click** "Networking"
3. **Add** custom domain
4. **Update** DNS:
   ```
   CNAME: your-domain.com -> your-app.up.railway.app
   ```
5. **Wait** for propagation (5-60 min)

---

## ✅ Verification

### **Quick Test:**
```bash
curl https://your-app.up.railway.app/api/system/health
```

**Expected:**
```json
{"status":"healthy","service":"Aether GovOS"}
```

---

## 🔧 Troubleshooting

### **Service Not Starting:**
- Check deployment logs
- Verify docker-compose.yml syntax
- Ensure all environment variables set

### **Database Connection Error:**
- Railway auto-provisions PostgreSQL
- Check DATABASE_URL is set
- Restart service

### **Frontend Not Loading:**
- Check backend URL in frontend variables
- Verify CORS settings
- Clear browser cache

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app
- **Discord:** https://discord.gg/railway
- **Email:** team@railway.app

---

## 🎉 Success!

**Your Aether GovOS is live on Railway!**

Share: `https://your-app.up.railway.app`

---

**🚀 Fastest deployment ever!**
