from cubedata import CubeData
from cards import cards

from js import (
    console,
    document)

def render_card(card: dict, current_player: int, show_hidden: bool = False, tag='li'):
    if show_hidden or "seen" not in card.keys() or card["seen"][current_player]:
        return f"<{tag} class=\"card-{card['color']}\">{card['name']}</{tag}>"
    else:
        return f"<{tag}>**hidden**</{tag}>"


def update_counts(cube):
    pyscript.write('card_count', cube.card_count)
    pyscript.write('main_pile_count', len(cube.shuffled_cards))
    pyscript.write('used_count', cube.cards_used)

def update_pile_panels(cube):
    pile_panel_ids = ["pile-panel-one", "pile-panel-two", "pile-panel-three"]

    for ix, pile_panel_id in enumerate(pile_panel_ids):
        pile_panel = Element(pile_panel_id)

        if ix == cube.current_pile:
            pile_panel.add_class("current-pile-panel")
        else:
            pile_panel.remove_class("current-pile-panel")
            

def update_piles(cube):
    pile_list_ids = ["pile_one", "pile_two", "pile_three"]

    for pile_list_id, pile in zip(pile_list_ids, cube.piles):
        pile_list = Element(pile_list_id)
        pile_list.clear()
        
        list_entries = [render_card(c, cube.current_player, show_hidden=cube.finished_draft) for c in pile]

        pile_list.element.innerHTML = '\n'.join(list_entries)


def update_players(cube):
    player_list_ids = ["player_one_cards_list", "player_two_cards_list"]

    for ix, player_list_id in enumerate(player_list_ids):
        list_entries = [render_card(c, cube.current_player, show_hidden=cube.finished_draft) for c in cube.players[ix]]
        player_list = Element(player_list_id)
        player_list.element.innerHTML = '\n'.join(list_entries)

def update_unused(cube):
    unused_panel = Element("unused_cards")
    unused_list = Element("unused_cards_list")

    if cube.finished_draft:
        unused_panel.remove_class("hidden")
        list_entries = [render_card(c, cube.current_player, show_hidden=cube.finished_draft) for c in cube.unused_cards]
        unused_list.element.innerHTML = '\n'.join(list_entries)
    else:
        unused_panel.add_class("hidden")

        unused_list.element.innerHTML = ""

def update(cube):

    update_counts(cube)

    update_pile_panels(cube)

    update_piles(cube)

    update_players(cube)

    update_unused(cube)


current_cube = CubeData()

def action_skip(*ags, **kws):
    console.log("skip")

    global current_cube
    if not current_cube.finished_draft:
        current_cube.skip()
        current_cube.reveal_cards()
    update(current_cube)


def action_take(*ags, **kws):
    console.log("take")

    global current_cube
    if not current_cube.finished_draft:
        current_cube.take_pile()
        current_cube.reveal_cards()
    update(current_cube)


def action_restart(*ags, **kws):
    console.log("restart")

    global current_cube
    current_cube.init_game()
    update(current_cube)

## Hide modal
modal = Element("loading-modal")
modal.remove_class("active")

## Starting Game
current_cube.cards = cards

current_cube.init_game()

update(current_cube)

