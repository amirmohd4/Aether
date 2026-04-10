# 🏛️ Aether GovOS - Government Integration Operating System

> One API for all government land services across India

## 🚀 Quick Start

```bash
docker-compose up
```

**That's it!** Open http://localhost:3000 in your browser.

---

## 📋 What You Get

### **5 Complete Land Services:**
1. 🏠 **Property Registration** - Full automated workflow (6 steps)
2. 🔄 **Mutation** - Ownership transfer and land record updates
3. 📜 **Encumbrance Certificate** - 30-year transaction history
4. 🏗️ **Land Use Conversion** - Agricultural to residential/commercial
5. 🛡️ **Title Verification** - Risk assessment with AI

### **Tech Stack:**
- **Backend:** FastAPI + PostgreSQL + Redis
- **Frontend:** React 19 + TypeScript + Tailwind CSS
- **AI/ML:** Scikit-learn (Fraud Detection)
- **Data:** 10,000 mock properties

---

## 🎯 Testing Guide

### **Access Points:**
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8001/api/docs
- **Health Check:** http://localhost:8001/health

### **Test Each Service:**

#### **1. Property Search & Registration**
1. Open http://localhost:3000
2. Click any property card
3. Click "Start Registration" button
4. Watch 6-step workflow complete

#### **2. AI Fraud Detection**
1. Click property card
2. Click "Check Fraud" button
3. View fraud score (0-100) with explanation

#### **3. Mutation (Ownership Transfer)**
1. Click "Apply Mutation" button
2. Enter new owner name
3. View mutation workflow results

#### **4. Encumbrance Certificate**
1. Click "Get EC" button
2. View 30-year transaction history
3. Check EC status (Clear/Encumbered)

#### **5. Land Use Conversion**
1. Click "Convert Land Use" button
2. Enter target use (commercial/residential)
3. View conversion workflow

#### **6. Title Verification**
1. Click "Verify Title" button
2. View risk score and recommendations
3. See ownership chain and disputes

---

## 🗄️ Database

**Pre-loaded Data:**
- 10,000 Properties (5,000 Karnataka + 5,000 J&K)
- 100 Citizens
- Realistic variations (clear/disputed/encumbered)
- Fraud patterns built-in

**Access PostgreSQL:**
```bash
docker exec -it aether-postgres psql -U postgres -d aether_govos
```

**Sample Queries:**
```sql
SELECT property_id, state, owner, title_status FROM properties LIMIT 10;
```

---

## 📊 API Documentation

**18 REST APIs Available:**

### **Property APIs:**
```bash
GET  /api/property/{property_id}
GET  /api/property/search/by-state/{state}
POST /api/property/verify-title/{property_id}
```

### **Workflow APIs:**
```bash
POST /api/workflow/start
POST /api/workflow/mutation/start
POST /api/workflow/ec/generate
POST /api/workflow/conversion/start
POST /api/workflow/title/verify
```

### **Fraud Detection:**
```bash
POST /api/fraud/detect/{property_id}
GET  /api/fraud/alerts/high-risk
```

**Full API Docs:** http://localhost:8001/api/docs

---

## 🌍 Cloud Deployment

### **Render (Free Tier - 5 min)**
1. Create account: https://render.com
2. Create PostgreSQL + Redis
3. Deploy backend (Python web service)
4. Deploy frontend (Static site)
5. **Live!**

### **Railway (Simplest - 3 min)**
1. Go to: https://railway.app
2. Deploy from GitHub repo
3. Railway auto-detects docker-compose
4. **Live!**

### **Docker Deployment Anywhere:**
```bash
docker-compose up -d
```

---

## 🔧 Development

### **Without Docker:**

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -c "from database import init_db; init_db()"
python ../scripts/generate_mock_data.py
python run.py
```

**Frontend:**
```bash
yarn install
yarn dev
```

### **Environment Variables:**

**Backend (.env):**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aether_govos
REDIS_URL=redis://localhost:6379/0
ACTIVE_STATE=karnataka
```

---

## 📞 Support

- **Demo:** http://localhost:3000
- **API Docs:** http://localhost:8001/api/docs
- **Issues:** GitHub Issues

---

## 🎬 Demo Video Script

**2-Minute Walkthrough:**
1. [0:00-0:30] Property search and registration
2. [0:30-1:00] AI fraud detection
3. [1:00-1:30] 4 new services (mutation, EC, conversion, title)
4. [1:30-2:00] Dashboards and API marketplace

---

## 📁 Project Structure

```
/app/
├── backend/                    # FastAPI Backend
│   ├── api/                   # API routes
│   ├── models/                # Database models
│   ├── services/              # Business logic
│   ├── connectors/            # Mock connectors
│   └── main.py
├── frontend/                   # React Frontend
│   └── src/
├── configs/                    # State configurations
├── docker-compose.yml
└── README.md
```

---

## 🚀 Features

- ✅ 5 Complete workflows
- ✅ 8 Mock government connectors
- ✅ AI fraud detection (10 rules + ML)
- ✅ Real-time dashboards
- ✅ API marketplace
- ✅ Multi-state support
- ✅ Production-ready

---

**Deploy Aether GovOS in under 5 minutes! 🎉**
