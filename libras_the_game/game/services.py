# Python imports
import random
from typing import List

# Internal imports
from libras_the_game.common.errors.internal_server_error import InternalServerError
from libras_the_game.game.models import Game
from libras_the_game.hand_configs.models import HandConfig
from libras_the_game.words.models import Word
from libras_the_game.words.services import get_random_excluded_words, get_random_word


def get_game() -> Game:
    words_options_count = 3
    word_options: List[Word] = None

    max_attempts = 10
    current_attempt = 0

    answer: Word = None
    hand_config: HandConfig

    while current_attempt < max_attempts and word_options is None:
        try:
            answer = get_random_word()
            hand_config = random.choice(answer.hand_configs_obj)
            word_options = get_random_excluded_words(
                [hand_config.id], words_options_count, answer.id
            )
        except Exception:
            current_attempt += 1
            word_options = None
    if word_options is None:
        raise InternalServerError("could not create game", "game")

    word_options = [w.word for w in [*word_options, answer]]
    random.shuffle(word_options)
    return Game(
        words=word_options,
        hand_config=hand_config,
        answer=answer.word,
    )
