from store.models import UserInteraction
from django.db.models import F, Case, When, Value, IntegerField

def export_interaction_dataset():
    qs = UserInteraction.objects.annotate(
        like_score=Case(
            When(action="like", then=Value(5)),
            default=Value(0),
            output_field=IntegerField()
        ),
        dislike_score=Case(
            When(action="dislike", then=Value(-5)),
            default=Value(0),
            output_field=IntegerField()
        ),
        total_score=F("view_count") + F("like_score") + F("dislike_score")
    ).values(
        "user_id", "product_id", "total_score"
    )


    return list(qs)