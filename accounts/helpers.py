"""Helper functions for User model"""

from django.utils import timezone


def get_age_from_date_of_birth(date_of_birth):
    """
    When User sets his date of birth, his age will be automatically calculated
    and returned.

    Returns:
        (int): Age of User as of today
    """
    age_as_of_today = timezone.now() - date_of_birth
    age_in_years = (age_as_of_today.days/30)/12
    return age_in_years
