# Python imports
from typing import List

# Pip imports
from bson import ObjectId

# Internal imports
from libras_the_game.common.clients.imgur_client import ImgurClient
from libras_the_game.common.errors import DuplicatedResourceError
from libras_the_game.common.models.boolean_response import BooleanResponse
from libras_the_game.hand_configs.models import (
    CreateHandConfig,
    DeleteHandConfig,
    HandConfig,
)
from libras_the_game.hand_configs.repository import HandConfigsRepository


def get_hand_configs() -> List[HandConfig]:
    repository = HandConfigsRepository()
    return list(repository.find_by({}))


def get_hand_configs_by_ids(ids: List[ObjectId]) -> List[HandConfig]:
    repository = HandConfigsRepository()
    return repository.find_by({"id": {"$in": ids}})


def get_hand_configs_by_names(names: List[str]) -> List[HandConfig]:
    repository = HandConfigsRepository()
    return repository.find_by({"name": {"$in": names}})


def create_hand_config(config: CreateHandConfig) -> HandConfig:
    repository = HandConfigsRepository()

    if repository.find_one_by({"name": config.name}):
        raise DuplicatedResourceError({"name": config.name})

    imgur_client: ImgurClient = ImgurClient.get_imgur_client()
    image = imgur_client.upload_image(config.image)

    hand_config = HandConfig(name=config.name, image=image)
    repository.save(hand_config)
    return hand_config


def delete_hand_config(config: DeleteHandConfig) -> BooleanResponse:
    repository = HandConfigsRepository()
    if config.id:
        hand_config = repository.find_one_by_id(config.id)
    else:
        hand_config = repository.find_one_by({"name": config.name})

    if hand_config:
        repository.delete(hand_config)
        return BooleanResponse(result=True)
    return BooleanResponse(result=False)
