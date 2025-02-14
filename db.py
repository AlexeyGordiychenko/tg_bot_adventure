import os
from sqlalchemy import (
    Boolean,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    select,
    and_,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    foreign,
    selectinload,
    aliased,
)
from random import randint

Base = declarative_base()
db_path = os.path.join(os.path.dirname(__file__), "game.db")
engine = create_engine("sqlite:///" + db_path)
Session = sessionmaker(bind=engine)

directions_association = Table(
    "directions",
    Base.metadata,
    Column("location_from_id", Integer, ForeignKey("locations.id"), primary_key=True),
    Column("location_to_id", Integer, ForeignKey("locations.id"), primary_key=True),
)


class Direction(Base):
    """A class that represents a direction between two locations."""

    __tablename__ = "directions"


class NPC(Base):
    """A class that represents a non-player character (NPC) in the game."""

    __tablename__ = "npcs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", back_populates="npcs")
    dialogs = relationship("Dialog", back_populates="npc", order_by="Dialog.stage_id")
    quest = relationship("Quest", back_populates="npc")


class Enemy(Base):
    """A class that represents an enemy in the game."""

    __tablename__ = "enemies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"))
    level = Column(Integer)
    loot_id = Column(Integer, ForeignKey("items.id"), nullable=True)

    location = relationship("Location", back_populates="enemies")
    loot = relationship("Item")


class Location(Base):
    """A class that represents a location in the game."""

    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    directions = relationship(
        "Location",
        secondary=directions_association,
        primaryjoin=id == directions_association.c.location_from_id,
        secondaryjoin=id == directions_association.c.location_to_id,
    )
    npcs = relationship("NPC", back_populates="location")
    enemies = relationship("Enemy", back_populates="location")
    characters = relationship("Protagonist", back_populates="location")

    async def get_directions(self):
        """A method that returns the directions from this location."""
        with Session() as session:
            session.add(self)
            return self.directions

    async def get_npcs(self):
        """A method that returns the NPCs in this location."""
        with Session() as session:
            session.add(self)
            return self.npcs

    async def get_enemies(self):
        """A method that returns the enemies in this location."""
        with Session() as session:
            session.add(self)
            return self.enemies


class Dialog(Base):
    """A class that represents a dialog between an NPC and the player."""

    __tablename__ = "dialogs"
    npc_id = Column(Integer, ForeignKey("npcs.id"), primary_key=True)
    stage_id = Column(Integer, nullable=False, index=True, primary_key=True)
    npc_text = Column(String, nullable=False)

    responses = relationship(
        "PlayerResponse",
        primaryjoin="and_(Dialog.npc_id==PlayerResponse.npc_id, Dialog.stage_id==foreign(PlayerResponse.stage_id))",
    )
    npc = relationship("NPC", back_populates="dialogs")


class PlayerResponse(Base):
    """A class that represents a player's response to a dialog."""

    __tablename__ = "player_responses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    npc_id = Column(Integer, ForeignKey("npcs.id"))
    stage_id = Column(Integer)
    text = Column(String, nullable=False)
    next_stage_id = Column(Integer, nullable=True)

    dialog = relationship(
        "Dialog",
        primaryjoin="and_(foreign(PlayerResponse.npc_id) == remote(Dialog.npc_id), "
        "foreign(PlayerResponse.stage_id) == remote(Dialog.stage_id))",
        back_populates="responses",
    )


class Inventory(Base):
    """A class that represents an inventory of items for a character."""

    __tablename__ = "inventories"
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    count = Column(Integer)

    character = relationship("Protagonist", back_populates="inventory")
    item = relationship("Item", lazy="selectin")


class Item(Base):
    """A class that represents an item in the game."""

    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    usable = Column(Boolean)


class Quest(Base):
    """A class that represents a quest given by an NPC."""

    __tablename__ = "quests"
    npc_id = Column(Integer, ForeignKey("npcs.id"), primary_key=True)
    task = Column(String)
    required_level = Column(Integer)
    required_item_id = Column(Integer, ForeignKey("items.id"))
    required_count = Column(Integer)
    reward_item_id = Column(Integer, ForeignKey("items.id"))
    reward_count = Column(Integer)

    npc = relationship("NPC", back_populates="quest")
    required_item = relationship("Item", foreign_keys=[required_item_id])
    reward_item = relationship("Item", foreign_keys=[reward_item_id])


class Journal(Base):
    """A class that represents a journal entry for a character's quest."""

    __tablename__ = "journals"
    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    npc_id = Column(Integer, ForeignKey("npcs.id"), primary_key=True)
    completed = Column(Boolean)

    character = relationship("Protagonist", back_populates="journal")
    quest = relationship(
        "Quest",
        primaryjoin=npc_id == foreign(Quest.npc_id),
        viewonly=True,
        uselist=False,
    )


class Protagonist(Base):
    """A class that represents the main character of the game."""

    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hp = Column(Integer)
    level = Column(Integer)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", back_populates="characters")
    inventory = relationship(
        "Inventory", back_populates="character", cascade="all, delete-orphan"
    )
    inventory_usable = relationship(
        "Inventory",
        secondary="join(Inventory, Item, and_(Inventory.item_id == Item.id, Item.usable == True))",
        viewonly=True,
    )

    journal = relationship(
        "Journal", back_populates="character", cascade="all, delete-orphan"
    )
    journal_completed = relationship(
        "Journal",
        primaryjoin="and_(Protagonist.id == foreign(Journal.character_id), Journal.completed == True)",
        viewonly=True,
    )

    active_quests = relationship(
        "Quest",
        secondary="join(Quest, Journal, and_(Journal.npc_id == foreign(Quest.npc_id), Journal.completed == False))",
        primaryjoin="Journal.character_id==Protagonist.id",
        secondaryjoin="Journal.npc_id==foreign(Quest.npc_id)",
        viewonly=True,
    )

    def __init__(self, id: int, name: str):
        """A method that initializes a new protagonist object.

        :param int id: The id of the character.
        :param str name: The name of the character.
        """
        self.id = id
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.location_id = 1
        self.inventory = [Inventory(item_id=1, count=1), Inventory(item_id=2, count=5)]

    def talk_to(self, npc: NPC):
        """A method that initiates a dialog with an NPC.

        :param NPC npc: The NPC to talk to.

        :returns:
            Dialog: The dialog object for each stage of the conversation.
        """
        stage = 1
        with Session() as session:
            dialogs = (
                session.execute(
                    select(Dialog)
                    .options(selectinload(Dialog.responses))
                    .where(Dialog.npc_id == npc.id)
                )
                .scalars()
                .all()
            )

        while True:
            dialog = dialogs[stage - 1]
            if not dialog:
                break
            stage = yield dialog

    async def attack(self, enemy: Enemy):
        """A method that performs an attack on an enemy.

        :param Enemy enemy: The enemy to attack.

        :returns:
            tuple: A tuple of (win, loot), where win is a boolean indicating if the attack was successful, and loot is an Item object or None if the enemy had no loot.
        """
        character_total = randint(1, 6) + int(self.level)
        enemy_total = randint(1, 6) + int(enemy.level)
        win = character_total >= enemy_total
        loot = None
        with Session() as session:
            session.expire_on_commit = False
            session.add(self)
            if win:
                await self.advance_level()
                if enemy.loot_id:
                    existing_item = next(
                        (
                            item
                            for item in self.inventory
                            if item.item_id == enemy.loot_id
                        ),
                        None,
                    )
                    if existing_item:
                        existing_item.count += 1
                    else:
                        self.inventory.append(Inventory(item_id=enemy.loot_id, count=1))
                    loot = session.execute(
                        select(Item).where(Item.id == enemy.loot_id)
                    ).scalar_one_or_none()
            else:
                await self.take_hit()
            session.commit()
        return win, loot

    async def take_hit(self, value: int = 1):
        """A method that reduces the character's health by a given value.

        :param int value: (optional) The amount of damage to take. Defaults to 1.

        :raises:
            Exception: If the character's health reaches zero or below.
        """
        self.hp -= value
        if self.hp <= 0:
            raise Exception("You died")

    async def heal(self, value: int = 1):
        """A method that increases the character's health by a given value.

        :param int value: (optional) The amount of healing to receive. Defaults to 1.
        """
        self.hp += value

    async def advance_level(self, value: int = 1):
        """A method that increases the character's level by a given value.

        :param int value: (optional) The amount of levels to gain. Defaults to 1.
        """
        self.level += value

    async def go(self, location_id):
        """A method that changes the character's location to a given location id.

        :param int lon_id (int): The id of the destination location.
        """
        with Session() as session:
            session.expire_on_commit = False
            session.add(self)
            self.location_id = location_id
            session.commit()
            session.refresh(self, attribute_names=["location"])

    async def whereami(self):
        """A method that returns the character's current location.

        :returns:
            Location: The location object of the character's current location.
        """
        with Session() as session:
            session.add(self)
            return self.location

    async def use_item(self, item: Inventory):
        """A method that uses an item from the character's inventory.

        :param Inventory item: The inventory object of the item to use.

        :returns:
            str: A message describing the effect of using the item.
        """
        effect = "You can't use this item."
        with Session() as session:
            if item.item.usable:
                session.expire_on_commit = False
                session.add(self)
                item = session.merge(item)
                if "potion of health" in item.item.name.lower():
                    await self.heal()
                    effect = (
                        f"You've used {item.item.name}.\nYour health increased by 1."
                    )
                    item.count -= 1
                if item.count <= 0:
                    session.delete(item)
                session.commit()
                session.refresh(self, attribute_names=["inventory", "inventory_usable"])
        return effect

    async def get_active_quests(self):
        """A method that returns the character's active quests.

        :returns:
            list: A list of dictionaries, each containing the npc, location, and task of a quest.
        """
        with Session() as session:
            session.add(self)
            quests = self.active_quests
            quests = list(map(session.merge, quests))
            if quests:
                return [
                    {
                        "npc": quest.npc.name,
                        "location": quest.npc.location.name,
                        "task": quest.task,
                    }
                    for quest in quests
                ]

    async def get_npc_quest(self, npc: NPC):
        """A method that returns the quest and journal entry for a given NPC.

        :param NPC npc: The NPC to get the quest from.

        :returns:
            tuple: A tuple of (Quest, Journal) or (None, None) if the NPC has no quest.
        """
        with Session() as session:
            data = session.execute(
                select(Quest, Journal)
                .join(
                    Journal,
                    and_(
                        Quest.npc_id == Journal.npc_id, Journal.character_id == self.id
                    ),
                    isouter=True,
                )
                .where(Quest.npc_id == npc.id)
            ).first()
        return data if data else (None, None)

    async def accept_npc_quest(self, npc: NPC):
        """A method that accepts a quest from an NPC and adds it to the character's journal.

        :param NPC npc: The NPC to accept the quest from.
        """
        with Session() as session:
            session.expire_on_commit = False
            session.add(self)
            self.journal.append(
                Journal(character_id=self.id, npc_id=npc.id, completed=False)
            )
            session.commit()
            session.refresh(self, attribute_names=["active_quests"])

    async def complete_npc_quest(self, npc: NPC):
        """A method that completes a quest from an NPC and updates the character's journal and inventory.

        :param NPC npc: The NPC to complete the quest for.

        :returns:
            bool: True if the quest was completed successfully, False otherwise.
        """
        with Session() as session:
            session.add(self)
            item_required = aliased(Inventory)
            item_reward = aliased(Inventory)
            data = session.execute(
                select(Journal, Quest, item_required, item_reward)
                .join(Quest, Journal.npc_id == Quest.npc_id)
                .join(
                    item_required,
                    and_(
                        Journal.character_id == item_required.character_id,
                        item_required.item_id == Quest.required_item_id,
                        item_required.count >= Quest.required_count,
                    ),
                )
                .join(
                    item_reward,
                    and_(
                        Journal.character_id == item_reward.character_id,
                        item_reward.item_id == Quest.reward_item_id,
                    ),
                    isouter=True,
                )
                .where(Journal.character_id == self.id)
                .where(Journal.npc_id == npc.id)
            ).first()
            if data:
                entry, quest, item_required, item_reward = data
                session.expire_on_commit = False
                entry.completed = True
                if item_reward:
                    item_reward.count += quest.reward_count
                else:
                    self.inventory.append(
                        Inventory(
                            item_id=quest.reward_item_id, count=quest.reward_count
                        )
                    )
                if item_required.count == quest.required_count:
                    session.delete(item_required)
                else:
                    item_required.count -= quest.required_count
                session.commit()
                session.refresh(
                    self,
                    attribute_names=["active_quests", "inventory", "inventory_usable"],
                )
                return True
            else:
                return False

    async def die(self):
        """A method that deletes the character from the database."""
        with Session() as session:
            session.add(self)
            session.delete(self)
            session.commit()

    async def get_inventory(self):
        """A method that returns the character's inventory.

        :returns:
            list: A list of dictionaries, each containing the item name and count.
        """
        with Session() as session:
            session.add(self)
            return [
                {"item": item.item.name, "count": item.count} for item in self.inventory
            ]

    async def get_usable_inventory(self):
        """A method that returns the character's usable inventory.

        :returns:
            list: A list of Inventory objects, each representing a usable item.
        """
        with Session() as session:
            session.add(self)
            return self.inventory_usable


async def get_character(id):
    """A function that returns a character object by id.

    :param int id: The id of the character.

    :returns:
        Protagonist: The character object or None if not found.
    """
    with Session() as session:
        return session.execute(
            select(Protagonist).where(Protagonist.id == id)
        ).scalar_one_or_none()


async def create_character(id, name):
    """A function that creates a new character object and adds it to the database.

    :param int id: The id of the character.
    :param str name: The name of the character.

    :returns:
        Protagonist: The new character object.
    """
    new_character = Protagonist(id=id, name=name)
    with Session() as session:
        session.add(new_character)
        session.commit()
    return new_character
