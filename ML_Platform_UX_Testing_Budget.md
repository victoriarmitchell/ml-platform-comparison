# **ML Platform UX Testing Budget Proposal**

## **📌 Overview**
**Goal:** Conduct UX testing across **Google Vertex AI, AWS SageMaker, and Azure ML** for model **training, registry, and deployment** while keeping costs minimal by shutting down instances when not in use.

---

## **1️⃣ Estimated Cost Breakdown by Phase**  

| **Phase**  | **Task**  | **Estimated Usage**  | **Estimated Cost**  |
|------------|-----------|----------------|----------------|
| **Phase 0** | Local model training and evaluation  | Notebook instance (local)  | **$0**  |
| **Phase 0.5** | Model upload to GCS & Registry | Cloud Storage (~5GB) | **$0.25** |
| **Phase 1** | Train and register model in **Vertex AI, SageMaker, Azure ML** | On-demand training | **$30 - $50** |
| **Phase 2** | Deploy model to an endpoint in all platforms | Endpoint (shut down when not in use) | **$30 - $60** |
| **Phase 3** | Multi-platform comparison | Monitoring & inference testing | **$20 - $40** |
| **Total Estimated Cost** | | | **$90 - $150** |

---

## **2️⃣ Cost Breakdown by Cloud Platform**  

| **Platform**  | **Service Used**  | **Estimated Cost**  |
|--------------|------------------|------------------|
| **Google Vertex AI**  | Model training, registry, deployment | **$30 - $50** |
| **AWS SageMaker**  | Model training, registry, deployment  | **$30 - $50** |
| **Azure ML**  | Model training, registry, deployment  | **$30 - $50** |

🔹 **Total Estimated Cost Across Platforms:** **$90 - $150**  

---

## **3️⃣ Detailed Cost Breakdown**

### **A. Compute Costs (Training & Inference)**
| **Resource** | **Usage Estimate** | **Cost per Hour** | **Estimated Cost** |
|-------------|-------------------|------------------|------------------|
| Vertex AI training | 1 hour per run | $0.10 - $0.20 | **$1 per run** |
| Vertex AI endpoint | 1 vCPU, 2GB RAM (shut down when not in use) | $0.05/hour | **$5 - $10 total** |
| SageMaker training | 1 hour per run | $0.15/hour | **$1.50 per run** |
| SageMaker endpoint | ml.m5.large (shut down when not in use) | $0.10/hour | **$10 total** |
| Azure ML training | 1 hour per run | $0.10 - $0.15 | **$1.50 per run** |
| Azure ML endpoint | Standard_DS3_v2 (shut down when not in use) | $0.08/hour | **$10 total** |

---

### **B. Data Storage Costs**
| **Storage Service**  | **Estimated Usage**  | **Cost**  |
|----------------------|------------------|----------------|
| **Google Cloud Storage**  | 5GB | **$0.25/month** |
| **AWS S3**  | 5GB | **$0.15/month** |
| **Azure Blob Storage**  | 5GB | **$0.12/month** |

---

### **C. Model Registry & Monitoring Costs**
| **Service**  | **Usage**  | **Estimated Cost**  |
|-------------|---------|----------------|
| **Vertex AI Model Registry**  | Model registration & versioning | **$0.10 per model** |
| **SageMaker Model Registry**  | Model registration & versioning | **$0.15 per model** |
| **Azure ML Model Registry**  | Model registration & versioning | **$0.12 per model** |
| **Vertex AI Model Monitoring**  | 10K predictions (optional) | **$10 - $15** |

---

## **4️⃣ Revised Budget Summary**
| **Category**  | **Estimated Cost Range**  |
|-------------|------------------|
| **Cloud Compute (Training & Inference)** | **$75 - $150** |
| **Storage (5GB per platform)** | **$0.50 - $1** |
| **Model Registry & Monitoring** | **$10 - $20** |
| **Total Estimated Budget** | **$90 - $150** |

---

## **5️⃣ Cost Optimization Strategies**
- **Train locally** where possible and only run cloud training **on demand**.  
- **Shut down endpoints** after testing (this saves **$50+ per month**).  
- **Use preemptible instances** for training to save ~60%.  
- **Use free-tier resources** for storage.  

---

## **6️⃣ Next Steps**
1️⃣ **Confirm scope** and finalize the budget.  
2️⃣ **Test cost assumptions** with a small-scale run.  
3️⃣ **Track actual costs** using Google Cloud Billing reports.  

---

### **📌 Final Estimate**
💰 **$90 - $150 total** (with minimal idle cloud usage)  

🚀 This estimate ensures all three platforms include **model training, registry, and deployment while keeping costs lean**.  
