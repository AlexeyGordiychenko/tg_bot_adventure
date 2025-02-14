import json
import os
from db import (
    Base,
    Item,
    Location,
    NPC,
    Enemy,
    Dialog,
    PlayerResponse,
    Direction,
    Quest,
    engine,
    Session,
)


def get_json_data(filename):
    """A function that reads a JSON file and returns its data.

    :param str filename: The name of the JSON file without the extension.

    :returns:
        dict: The data from the JSON file.
    """
    try:
        with open(
            os.path.join(os.path.dirname(__file__), f"data/{filename}.json"), "r"
        ) as file:
            return json.load(file)
    except Exception as e:
        print(f"Couldn't read the json file '{filename}': {e}")
        return []


def load_npcs(session):
    """A function that loads the NPC data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    for npc_data in get_json_data("npcs"):
        session.add(NPC(**npc_data))
    session.commit()


def load_enemies(session):
    """A function that loads the enemy data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    for enemy_data in get_json_data("enemies"):
        session.add(Enemy(**enemy_data))
    session.commit()


def load_dialogs(session):
    """A function that loads the dialog data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    for dialog in get_json_data("dialogs"):
        session.add(
            Dialog(
                npc_id=dialog["npc_id"],
                stage_id=dialog["stage_id"],
                npc_text=dialog["npc_text"],
            )
        )

        for response in dialog["responses"]:
            session.add(
                PlayerResponse(
                    **response, npc_id=dialog["npc_id"], stage_id=dialog["stage_id"]
                )
            )

    session.commit()


def load_locations(session):
    """A function that loads the location data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    locations = get_json_data("locations")
    for location in locations:
        session.add(
            Location(
                id=location["id"],
                name=location["name"],
                description=location["description"],
            )
        )

    for location in locations:
        for direction in location["directions"]:
            session.add(
                Direction(location_from_id=location["id"], location_to_id=direction)
            )
    session.commit()


def load_items(session):
    """A function that loads the item data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    for item_data in get_json_data("items"):
        session.add(Item(**item_data))
    session.commit()


def load_quests(session):
    """A function that loads the quest data from the JSON file and adds them to the database.

    :param Session session: The database session object.
    """
    for quest_data in get_json_data("quests"):
        session.add(Quest(**quest_data))
    session.commit()


def load_all():
    tables_to_drop = [
        Location.__table__,
        NPC.__table__,
        Enemy.__table__,
        Dialog.__table__,
        PlayerResponse.__table__,
        Direction.__table__,
        Item.__table__,
        Quest.__table__,
    ]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

    Base.metadata.create_all(engine)

    session = Session()
    load_items(session)
    load_npcs(session)
    load_enemies(session)
    load_dialogs(session)
    load_quests(session)
    load_locations(session)


if __name__ == "__main__":
    load_all()
