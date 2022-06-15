# Python imports
from typing import List

# Pip imports
from pydantic_mongo import AbstractRepository, ObjectIdField

# Internal imports
from libras_the_game.database import Database
from libras_the_game.words.models import Word


class WordsRepository(AbstractRepository[Word]):
    def __init__(self):
        super().__init__(Database.get_db_client())

    class Meta:
        collection_name = "words"

    def get_random_word(self) -> Word:
        random_word = next(self.get_collection().aggregate([{"$sample": {"size": 1}}]))
        return self.to_model(random_word)

    def get_random_excluded_words(
        self,
        exclude_hand_configs_ids: List[ObjectIdField],
        count: int,
        exclude_word_id: ObjectIdField,
    ) -> List[Word]:
        random_words = self.get_collection().aggregate(
            [
                {
                    "$match": {
                        "_id": {"$nin": [exclude_word_id]},
                        "hand_configs": {"$nin": exclude_hand_configs_ids},
                    }
                },
                {"$sample": {"size": count}},
            ]
        )
        return [self.to_model(rw) for rw in random_words]
