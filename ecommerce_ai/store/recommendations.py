from datetime import timedelta
from django.utils.timezone import now
from django.db.models import (
    F, Case, When, Value, FloatField, ExpressionWrapper
)
from django.db.models.functions import Log
from store.models import UserInteraction, Product
import math
from django.db.models import Sum

from django.core.cache import cache

def min_max_normalize(scores):
    if not scores:
        return scores

    values = [s for _, s in scores]
    min_s, max_s = min(values), max(values)

    if min_s == max_s:
        return [(pid, 1.0) for pid, _ in scores]

    return [
        (pid, (s - min_s) / (max_s - min_s)) for pid, s in scores
    ]

def get_fallback_products(limit=5):
    return (
        UserInteraction.objects
        .values("product")
        .annotate(score=Sum("view_count"))
        .order_by("-score")[:limit]
    )


CACHE_TTL = 60 * 5  # 5 minutes


def get_recommended_products_for_user(user, limit=5):
    cache_key = f"reco_user_{user.id}"

    cached = cache.get(cache_key)
    if cached:
        return Product.objects.filter(id__in=cached)

    interactions = UserInteraction.objects.filter(user=user)

    #  Cold start
    if not interactions.exists():
        ids = [x["product"] for x in get_fallback_products(limit)]
        cache.set(cache_key, ids, CACHE_TTL)
        return Product.objects.filter(id__in=ids)

    scores = {}

    for i in interactions:
        scores.setdefault(i.product_id, 0)

        if i.action == "like":
            scores[i.product_id] += 3
        elif i.action == "dislike":
            scores[i.product_id] -= 2

        scores[i.product_id] += i.view_count * 0.2

    scored = [(pid, score) for pid, score in scores.items()]
    scored = min_max_normalize(scored)
    scored.sort(key=lambda x: x[1], reverse=True)

    product_ids = [pid for pid, _ in scored][:limit]

    cache.set(cache_key, product_ids, CACHE_TTL)
    return Product.objects.filter(id__in=product_ids)
