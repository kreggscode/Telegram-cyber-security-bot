
def decide_post_type() -> str:
    """
    For the Language Learning Bot, we always want to post a language pair 
    whenever the script is run (scheduled by GitHub Actions).
    """
    return "cyber_post"
