# E-commerce AI Recommendation System

## Overview
This project is a Django-based e-commerce web application enhanced with a hybrid AI-powered product recommendation system. It demonstrates end-to-end backend development, user interaction tracking, recommendation modeling, and performance optimization using Cython.

The system is designed to simulate how modern e-commerce platforms recommend products based on user behavior such as views, likes, and dislikes, combining rule-based scoring with intelligent fallback mechanisms for new users.

---

## Key Features

### Core E-commerce Functionality
- Product listing and product detail pages
- User authentication (login/logout)
- Cart management (add to cart, view cart)
- Session-based user handling
- User-specific product interactions

### User Interaction Tracking
- **Views**: Counted only when a user opens a product detail page (captures genuine interest)
- **Likes / Dislikes**: One per user per product, implemented as a toggle to avoid noisy data
- Persistent storage of interactions for recommendation modeling
- View counts are updated using atomic database operations to prevent race conditions

### Hybrid Recommendation System
- Rule-based, behavior-driven recommendation engine
- Scores products using:
  - View frequency (recurring interest)
  - Likes (positive signal)
  - Dislikes (negative signal)
- The system also builds a user–item interaction matrix and computes user–user similarity using cosine similarity.
- This introduces a basic collaborative filtering recommendation system.
- **Cold-start handling**: New users receive recommendations based on globally popular products
- Score normalization to prevent bias toward extreme values

### Caching Layer

To improve performance and scalability:

- Recommendations are cached per user for 5 minutes
- Implemented using Django’s caching framework
- Reduces repeated computation and database queries
- Improves response time for frequently active users

### Performance Optimization with Cython
- Identified recommendation scoring as a compute-heavy hot path
- Reimplemented scoring logic using **Cython**
- Compiled into a native extension (.pyd) callable directly from Django
- Benchmarked against pure Python implementation and achieved a measurable speedup over pure Python implementation
- Benchmark Result 

| Implementation | Time   |
| -------------- | ------ |
| Python         | ~0.78s |
| Cython         | ~0.14s |
| Speedup        | ~3–5×  |

---
## Data Engineering Pipeline

Interaction data is transformed before training:

1. Extract user interactions from database
2. Convert actions into numerical scores using ORM annotations
3. Build user–item matrix
4. Train similarity model
5. Store similarity matrix for recommendation use


---

## Tech Stack
| Component                | Technology           |
| ------------------------ | -------------------- |
| Backend                  | Django (Python)      |
| Database                 | SQLite (Development) |
| Recommendation System    | Python               |
| Collaborative Filtering  | Scikit-learn         |
| Performance Optimization | Cython               |
| Caching                  | Django Cache         |
| Environment              | Python 3.11          |

---

## Project Structure

```
ecommerce_ai/
├── ecommerce_ai/        # Django project settings
├── store/               # Main application
│   ├── models.py        # Product, CartItem, UserInteraction models
│   ├── views.py         # Product, cart, and interaction views
│   ├── recommendations.py
│   ├── ml/              # ML / recommender preparation logic
│   ├── cython_utils/    # Cython-optimized scoring
│   ├── benchmarks/      # Performance benchmark scripts
│   └── utils/           # Pure Python utilities
├── db.sqlite3
└── manage.py
```

---

## Recommendation Scoring Logic

Each product is assigned a score per user based on interaction signals:

- Views contribute a small positive weight (recurring interest)
- Likes contribute a strong positive weight
- Dislikes contribute a negative weight

Scores are normalized using min–max normalization before ranking.

For users with no interaction history, the system falls back to recommending globally popular products based on aggregate view counts.

---

## Cython Optimization

The recommendation scoring function was identified as a frequently executed, compute-heavy operation. To optimize this:

- The scoring logic was rewritten using Cython
- Compiled into a native `.pyd` extension
- Exposed to Python using `cpdef` for seamless Django integration

### Result
Benchmarking showed a **3–5× performance improvement** compared to the pure Python implementation.

---

## Benchmarking

A simple micro-benchmark compares Python vs Cython scoring:

```bash
python -m store.benchmarks.benchmark_scoring
```

Example output:
```
Python time : 0.78s
Cython time : 0.14s
Speedup     : 5.5x
```

---

## How to Run

### 1. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Install dependencies
```bash
cd store/cython_utils
python setup.py build_ext --inplace
```
### 3. Run migrations
```bash
python manage.py migrate
```
### 4. Start the development server
```bash
python manage.py runserver
```

---

## Design Decisions

- Views are counted only on product detail pages to avoid inflated signals
- Likes/dislikes are restricted to one per user–product to preserve data quality
- Cython is used selectively on hot paths rather than prematurely optimizing the entire system

---

## Future Improvements

- Periodic offline training with larger datasets
- Deployment with PostgreSQL for production 
- Redis caching instead of local memory cache
- Matrix Factorization (SVD / ALS)
- Deploy on AWS/GCP

---

## Summary

This project demonstrates:
- Backend development using Django
- User behavior tracking and data modeling
- Hybrid recommendation system (rule-based + collaborative filtering)
- Feature engineering and ML pipeline integration
- Caching for performance improvement
- Low-level performance optimization using Cython
- Benchmarking and performance analysis