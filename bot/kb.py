from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_menu_btn = InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")
"""A button that takes the user back to the main menu.

    :meta hide-value:
"""

back_menu = InlineKeyboardMarkup(inline_keyboard=[[back_to_menu_btn]])
"""A keyboard markup that contains the back to menu button.

    :meta hide-value:
"""

create_character_button = [
    [InlineKeyboardButton(text="🎭 Create", callback_data="create_character")],
]
"""A list of lists of buttons that allows the user to create a character.

    :meta hide-value:
"""

create_character_menu = InlineKeyboardMarkup(inline_keyboard=create_character_button)
"""A keyboard markup that contains the create character button.

    :meta hide-value:
"""

main_menu_buttons = [
    [
        InlineKeyboardButton(text="🗺️ Location", callback_data="get_location"),
        InlineKeyboardButton(text="🚶‍♂️ Go to", callback_data="change_location"),
    ],
    [
        InlineKeyboardButton(text="🎒 Inventory", callback_data="get_inventory"),
        InlineKeyboardButton(text="🧪 Use item", callback_data="get_usable_items"),
    ],
    [
        InlineKeyboardButton(text="👥 NPC", callback_data="get_npcs"),
        InlineKeyboardButton(text="🗡️ Enemies", callback_data="get_enemies"),
    ],
    [
        InlineKeyboardButton(text="🏆 Stats", callback_data="get_stats"),
        InlineKeyboardButton(text="📜 Quests", callback_data="get_quests"),
    ],
]
"""A list of lists of buttons that allows the user to access various features of the game.

    :meta hide-value:
"""

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
"""A keyboard markup that contains the main menu buttons.

    :meta hide-value:
"""
