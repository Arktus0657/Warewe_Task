# E-commerce AI Recommendation System

## Overview
This project is a Django-based e-commerce web application enhanced with an AI-powered product recommendation system. It demonstrates end-to-end backend development, user interaction tracking, basic recommendation logic, and performance optimization using Cython. The system is designed to be simple, extensible, and suitable for demonstrating applied machine learning concepts in a real-world web application.

---

## Key Features

### Core E-commerce Functionality
- Product listing and product detail pages
- User authentication (login/logout)
- Cart management (add to cart, view cart)
- Session-based user handling

### User Interaction Tracking
- **Views**: Counted only when a user opens a product detail page (captures genuine interest)
- **Likes / Dislikes**: One per user per product, implemented as a toggle to avoid noisy data
- Persistent storage of interactions for recommendation modeling

### Recommendation System
- Rule-based, behavior-driven recommendation engine
- Scores products using:
  - View frequency (recurring interest)
  - Likes (positive signal)
  - Dislikes (negative signal)
- **Cold-start handling**: New users receive recommendations based on globally popular products
- Score normalization to prevent bias toward extreme values

### Performance Optimization with Cython
- Identified recommendation scoring as a compute-heavy hot path
- Reimplemented scoring logic using **Cython**
- Compiled into a native extension callable directly from Django
- Achieved a measurable speedup over pure Python implementation

---

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (for development)
- **Recommendation Logic**: Python + Cython
- **Performance Optimization**: Cython (native extension)
- **Environment**: Python 3.11, Windows

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

1. Create and activate a virtual environment
2. Install dependencies
3. Run migrations
4. Start the development server

```bash
python manage.py migrate
python manage.py runserver
```

---

## Design Decisions

- Views are counted only on product detail pages to avoid inflated signals
- Likes/dislikes are restricted to one per user–product to preserve data quality
- Cython is used selectively on hot paths rather than prematurely optimizing the entire system

---

## Future Improvements

- Replace rule-based recommender with collaborative filtering or matrix factorization
- Periodic offline training with larger datasets
- Caching recommended results per user
- Deployment with PostgreSQL and Redis

---

## Summary

This project demonstrates practical backend engineering, thoughtful data modeling for recommendations, and real performance optimization using Cython. It balances correctness, simplicity, and efficiency, making it suitable both as an academic assignment and a foundation for real-world extension.

