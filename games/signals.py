from django.dispatch import Signal, receiver

game_clicked_signal = Signal()

@receiver(game_clicked_signal)
def increment_number_of_clicks_of_game(game_object, *args, **kwargs):
    game_object.clicks += 1
    game_object.save()


