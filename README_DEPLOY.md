# 🏛️ Aether GovOS - Government Integration Operating System

> One API for all government land services across India

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)

## 🚀 Quick Start (One Command)

```bash
docker-compose up
```

**That's it!** Open http://localhost:3000 in your browser.

---

## 📋 What You Get

### **5 Complete Land Services:**
1. 🏠 **Property Registration** - End-to-end property registration workflow
2. 🔄 **Mutation** - Ownership transfer and land record updates
3. 📜 **Encumbrance Certificate (EC)** - 30-year transaction history
4. 🏗️ **Land Use Conversion** - Agricultural to residential/commercial conversion
5. 🛡️ **Title Verification** - Comprehensive title check with risk score

### **8 Mock Government Connectors:**
- Karnataka: Kaveri, eAasthi, Bhoomi
- J&K: LRIS
- Generic: Aadhaar, DigiLocker
- Municipal: Zoning & Land Use
- Court: Legal Records & Disputes

### **Tech Stack:**
- **Backend:** FastAPI + PostgreSQL + Redis
- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS
- **AI/ML:** Scikit-learn Isolation Forest (Fraud Detection)
- **Data:** 10,000 mock properties with realistic variations

---

## 🎯 Demo Walkthrough

### **Access the Application:**
- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8001/api/docs
- **API Marketplace:** http://localhost:3000 (click "API Marketplace" tab)

### **Test Each Service:**

#### **1. Property Search & Registration**
```
1. Open http://localhost:3000
2. Select "Karnataka" from state dropdown
3. Browse property cards (10 properties displayed)
4. Click any property to view details
5. Click "Start Registration" button
6. Watch workflow progress (6 steps: title verification → encumbrance → stamp duty → payment → registration → mutation)
7. See real-time progress percentage
```

#### **2. AI Fraud Detection**
```
1. Click any property card
2. Click "Check Fraud" button
3. View fraud score (0-100) with color coding:
   - Green (0-25): Low risk
   - Yellow (25-50): Medium risk
   - Orange (50-75): High risk
   - Red (75-100): Critical risk
4. Read AI-generated explanation
5. See evidence of 10 fraud rules checked
```

#### **3. Apply Mutation (Ownership Transfer)**
```
1. Click property card
2. Click "Apply Mutation" button
3. Enter new owner name (e.g., "John Doe")
4. View mutation workflow progress
5. See mutation ID and status
6. Check updated land records
```

#### **4. Generate Encumbrance Certificate**
```
1. Click property card
2. Click "Get EC" button
3. View generated EC with:
   - EC ID
   - Certificate status (Clear/Encumbered)
   - 30-year transaction history
   - Total encumbrance amount
   - DigiLocker storage confirmation
4. See EC added to "EC History" section
```

#### **5. Land Use Conversion**
```
1. Click property card
2. Click "Convert Land Use" button
3. Enter target use (e.g., "commercial", "residential")
4. View conversion workflow:
   - Zoning eligibility check
   - Conversion fee calculation
   - Payment processing
   - Land use update
5. See conversion confirmation
```

#### **6. Title Verification**
```
1. Click property card
2. Click "Verify Title" button
3. View comprehensive title report:
   - Risk score (0-100)
   - Risk level (Very Low/Low/Medium/High/Critical)
   - AI recommendation
   - Risk factors list
   - 30-year ownership chain
   - Court dispute check
   - Identity verification
```

---

## 🌍 Cloud Deployment

### **Render (Recommended - Free Tier)**

**One-Click Deploy:**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Manual Steps:**
1. Create Render account: https://render.com
2. Create PostgreSQL + Redis instances
3. Deploy backend web service (Python)
4. Deploy frontend static site
5. **Live in 5 minutes!**

---

### **Railway (Simplest)**

**One-Click Deploy:**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

Railway auto-detects docker-compose.yml

---

## 📊 API Documentation

**Interactive Docs:** http://localhost:8001/api/docs

**18 Endpoints Available** - View in API Marketplace tab

---

## 🎬 Demo Video Script (2 Minutes)

**[0:00-0:30]** Property Search & Registration
**[0:30-1:00]** AI Fraud Detection + New Services
**[1:00-1:30]** Mutation, EC, Conversion, Title Verification
**[1:30-2:00]** Dashboards & API Marketplace

---

## 📞 Contact

- **Website:** https://aether-govos.com
- **Email:** support@aether-govos.com
- **Demo:** http://demo.aether-govos.com

---

**🚀 Deploy Aether GovOS in under 5 minutes!**
