def calculate_match(pref, profile):
    score = 0

    if pref.min_age <= profile.age <= pref.max_age:
        score += 25

    if pref.religion == profile.religion:
        score += 25

    if pref.education == profile.education:
        score += 25

    if pref.location == profile.location:
        score += 25

    return score
