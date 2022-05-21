"""This module will define custom signals and catches it"""

# pylint: disable=unused-argument
from django.dispatch import Signal, receiver

game_clicked_signal = Signal()


@receiver(game_clicked_signal)
def increment_number_of_clicks_of_game(game_object, *args, **kwargs):
    """
    Everytime a Buyer chooses a Game or clicks on it, a signal will be
    generated and recieve by this method and in reponse, it will increment
    total clicks the game has revieved it yet.
    """
    game_object.clicks += 1
    game_object.save()
