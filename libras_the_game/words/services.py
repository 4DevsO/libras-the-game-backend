# Python imports
from typing import List

# Pip imports
from pydantic_mongo import ObjectIdField

# Internal imports
from libras_the_game.common.errors import DuplicatedResourceError, ResourceNotFoundError
from libras_the_game.common.models.boolean_response import BooleanResponse
from libras_the_game.hand_configs.services import (
    get_hand_configs_by_ids,
    get_hand_configs_by_names,
)
from libras_the_game.words.models import CreateWord, DeleteWord, Word
from libras_the_game.words.repository import WordsRepository


def get_words() -> List[Word]:
    repository = WordsRepository()
    return list(repository.find_by({}))


def get_random_word() -> Word:
    repository = WordsRepository()
    return populate_hand_configs_obj(repository.get_random_word())


def get_random_excluded_words(
    exclude_hand_configs_ids: List[ObjectIdField],
    count: int,
    exclude_word_id: ObjectIdField,
) -> List[Word]:
    repository = WordsRepository()
    return repository.get_random_excluded_words(
        exclude_hand_configs_ids, count, exclude_word_id
    )


def create_word(word: CreateWord) -> Word:
    repository = WordsRepository()

    if repository.find_one_by({"word": word.word}):
        raise DuplicatedResourceError({"word": word.word})

    hand_config_source = word.hand_configs_names
    get_hand_configs = get_hand_configs_by_names
    hand_config_attr = "name"
    if word.hand_configs:
        hand_config_source = word.hand_configs
        get_hand_configs = get_hand_configs_by_ids
        hand_config_attr = "id"

    found_hcs = list(get_hand_configs(hand_config_source))
    found_hcs_attr = [getattr(hc, hand_config_attr) for hc in found_hcs]
    errors = {
        "hand_configs": str(hc) for hc in hand_config_source if hc not in found_hcs_attr
    }

    if len(errors):
        raise ResourceNotFoundError(errors)

    found_hcs_ids = [hc.id for hc in found_hcs]
    word = Word(word=word.word, hand_configs=found_hcs_ids)
    repository.save(word)
    return word


def delete_word(word: DeleteWord) -> BooleanResponse:
    repository = WordsRepository()
    if word.id:
        word = repository.find_one_by_id(word.id)
    else:
        word = repository.find_one_by({"word": word.word})

    if word:
        repository.delete(word)
        return BooleanResponse(result=True)
    return BooleanResponse(result=False)


def populate_hand_configs_obj(word: Word) -> Word:
    word.hand_configs_obj = list(get_hand_configs_by_ids(word.hand_configs))
    return word
