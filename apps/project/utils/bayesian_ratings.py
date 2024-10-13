from django.db.models import Avg

def calculate_bayesian_average(project, m=5):
    """
    Calculate the Bayesian average for the given project.

    Parameters:
    - project: The project instance for which to calculate the average.
    - m: Minimum votes required to be considered for the average (default is 5).

    Returns:
    - Weighted average rating of the project.
    """
    # Calculate the mean rating across all projects
    C = project.__class__.objects.aggregate(mean_rating=Avg('average_rating'))['mean_rating'] or 0

    # Get the number of ratings and average rating for this project
    v = project.ratings.count()
    R = project.average_rating

    # Calculate Bayesian average
    if v < m:
        weighted_average = (0 * C + R * v) / (v + 1)  # Adjusted to avoid division by zero
    else:
        weighted_average = ((m * C) + (R * v)) / (m + v)

    return weighted_average
