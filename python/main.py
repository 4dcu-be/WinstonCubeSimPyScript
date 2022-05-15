from cubedata import CubeData
from cards import cards

from js import (
    console,
    document)

def render_card(card: dict, current_player: int, show_hidden: bool = False):
    if show_hidden or "seen" not in card.keys() or card["seen"][current_player]:
        return f"<li>{card['name']}</li>"
    else:
        return "<li>**hidden**</li>"


def update_counts(cube):
    pyscript.write('card_count', cube.card_count)
    pyscript.write('main_pile_count', len(cube.shuffled_cards))
    pyscript.write('used_count', cube.cards_used)


def update_piles(cube):
    pile_list_ids = ["pile_one", "pile_two", "pile_three"]

    for pile_list_id, pile in zip(pile_list_ids, cube.piles):
        pile_list = Element(pile_list_id)
        pile_list.clear()
        
        list_entries = [render_card(c, cube.current_player) for c in pile]

        pile_list.element.innerHTML = '\n'.join(list_entries)


def update_players(cube):
    player_list_ids = ["player_one_cards_list", "player_two_cards_list"]

    for ix, player_list_id in enumerate(player_list_ids):
        list_entries = [render_card(c, cube.current_player) for c in cube.players[ix]]
        player_list = Element(player_list_id)
        player_list.element.innerHTML = '\n'.join(list_entries)


def update(cube):

    update_counts(cube)

    update_piles(cube)

    update_players(cube)


current_cube = CubeData()

## Starting Game
current_cube.cards = cards
current_cube.shuffle_cards()

current_cube.piles = [
    [current_cube.shuffled_cards.pop()],
    [current_cube.shuffled_cards.pop()],
    [current_cube.shuffled_cards.pop()],
]

current_cube.players = [[], []]

current_cube.reveal_cards()

update(current_cube)

