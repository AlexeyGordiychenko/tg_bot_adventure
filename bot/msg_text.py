MAX_LINE_WIDTH = 200
"""A constant that defines the maximum line width for the messages.

    :meta hide-value:
"""

SPEC_MSG_END = "&#x200D;"
"""A constant that defines the special character to mark the end of a message.

    :meta hide-value:
"""

msg_welcome_new = "Welcome! Please, create a character to start playing."
"""A message that welcomes a new user and prompts them to create a character.

    :meta hide-value:
"""

msg_welcome = "Welcome, {name}!"
"""A message that welcomes an existing user by their name.

    :meta hide-value:
"""

msg_enter_name = "Enter your character name:"
"""A message that asks the user to enter their character name.

    :meta hide-value:
"""

msg_create_succ = "Character created."
"""A message that confirms the successful creation of a character.

    :meta hide-value:
"""

msg_current_location = "Current location: {location}."
"""A message that displays the current location of the character.

    :meta hide-value:
"""

msg_stats = "Current level: {level}.\nCurrent health: {health}."
"""A message that displays the current level and health of the character.

    :meta hide-value:
"""

spec_msg_current_inventory = "Current inventory:\n"
"""A message that displays the current inventory of the character.

    :meta hide-value:
"""

msg_choose_item_to_use = "Choose an item to use:"
"""A message that prompts the user to choose an item to use from their inventory.

    :meta hide-value:
"""

msg_no_usable_items = "No usable items available."
"""A message that informs the user that they have no usable items in their inventory.

    :meta hide-value:
"""

msg_change_location_ask = "Where do you want to go?"
"""A message that asks the user where they want to go.

    :meta hide-value:
"""

msg_change_location_succ = "You've moved to {location}.\nDescription: {desc}"
"""A message that confirms the successful change of location and displays the description of the new location.

    :meta hide-value:
"""

msg_pick_npc = "Which NPC do you want to interact with?"
"""A message that prompts the user to choose an NPC to interact with.

    :meta hide-value:
"""

msg_leave_npc = "You left."
"""A message that confirms the user has left the interaction with the NPC.

    :meta hide-value:
"""

msg_no_npcs_in_location = "There are no NPCs in this location."
"""A message that informs the user that there are no NPCs in their current location.

    :meta hide-value:
"""

msg_pick_enemy = "Which enemy do you want to fight:"
"""A message that prompts the user to choose an enemy to fight.

    :meta hide-value:
"""

msg_no_enemies_in_location = "There are no enemies in this location."
"""A message that informs the user that there are no enemies in their current location.

    :meta hide-value:
"""

msg_choose_action = "Choose an action:"
"""A message that prompts the user to choose an action to perform.

    :meta hide-value:
"""

msg_fight_succ = "You've defeated the {enemy}!\nYour level is increased by 1.\nCurrent level is {level}.\nYou've looted 1 {loot}."
"""A message that displays the result of a successful fight, the level increase, and the loot obtained.

    :meta hide-value:
"""

msg_fight_succ_no_loot = "You've defeated the {enemy}!\nYour level is increased by 1.\nCurrent level is {level}."
"""A message that displays the result of a successful fight and the level increase, but no loot obtained.

    :meta hide-value:
"""

msg_fight_fail = (
    "{enemy} has defeated you.\nYour health is reduced by 1.\nCurrent health is {hp}."
)
"""A message that displays the result of a failed fight and the health decrease.

    :meta hide-value:
"""

msg_fight_die = (
    "{enemy} has defeated you. You've died.\nType /start to create a new character."
)
"""A message that displays the result of a fatal fight and prompts the user to create a new character.

    :meta hide-value:
"""

msg_npc_no_quest = "No quests available."
"""A message that informs the user that the NPC has no quests to offer.

    :meta hide-value:
"""

msg_no_quests = "You have no quests."
"""A message that informs the user that they have no quests in their journal.

    :meta hide-value:
"""

spec_msg_current_quests = "Current quests:\n"
"""A message that displays the current quests in the user's journal.

    :meta hide-value:
"""

msg_quest = "{npc} at {location}: {task}"
"""A message that displays the details of a quest, including the NPC, the location, and the task.

    :meta hide-value:
"""

msg_quest_complete_succ = "You've completed the quest."
"""A message that confirms the successful completion of a quest.

    :meta hide-value:
"""

msg_quest_complete_deny = "You don't have required items to complete this quest."
"""A message that informs the user that they don't have the required items to complete a quest.

    :meta hide-value:
"""

msg_no_character = "An error occured. Please, use /start to reload."
"""A message that informs the user that an error has occurred and prompts them to reload the bot.

    :meta hide-value:
"""

msg_gen_welcome = "This is a bot to generate names for various characters and items."
"""A message that introduces the bot's functionality of generating names.

    :meta hide-value:
"""

msg_gen_choose_type = "Choose a type:"
"""A message that prompts the user to choose a type of name to generate.

    :meta hide-value:
"""

msg_gen_choose_category = "Choose a category:"
"""A message that prompts the user to choose a category of name to generate.

    :meta hide-value:
"""

btn_menu = "🏠 Main Menu"
"""A button that takes the user to the main menu.

    :meta hide-value:
"""

btn_back = "🔙 Back"
"""A button that takes the user to the previous menu.

    :meta hide-value:
"""

btn_dialog = "💬 Dialogue"
"""A button that initiates a dialogue with an NPC.

    :meta hide-value:
"""

btn_quest = "📜 Quest"
"""A button that displays the quest details of an NPC.

    :meta hide-value:
"""

btn_accept = "✅ Accept"
"""A button that accepts a quest from an NPC.

    :meta hide-value:
"""

btn_complete_quest = "🎉 Complete"
"""A button that completes a quest for an NPC.

    :meta hide-value:
"""

btn_quest_not_available = "❌ required level {level}"
"""A button that indicates that a quest is not available due to the character's level.

    :meta hide-value:
"""


def format_string(input_string, line_length=MAX_LINE_WIDTH):
    """A function that formats a string to fit a given line width and adds a special character at the end.

    :param str input_string: The string to format.
    :param int line_length: (optional) The maximum line width. Defaults to MAX_LINE_WIDTH.

    :returns:
        str: The formatted string with the special character at the end.
    """
    return f"{input_string:<{line_length}}" + SPEC_MSG_END


def _apply_formatting():
    """A function that applies the formatting function to all the global variables that start with 'msg_'."""
    globals_to_format = {
        k: v
        for k, v in globals().items()
        if isinstance(v, str) and k.startswith("msg_") and k != __name__
    }
    for name, value in globals_to_format.items():
        formatted_value = format_string(value)
        globals()[name] = formatted_value


_apply_formatting()
