# scorer.pyx

cpdef float fast_score(int views, int likes, int dislikes):
    return views * 0.2 + likes * 3 - dislikes * 2
