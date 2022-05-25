from cubedata import CubeData
import urllib
import json
import pyodide

from js import (
    console,
    document)

current_cube = CubeData()

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

    modal = Element("cube-modal")
    modal.add_class("active")

def action_start_from_url(*ags, **kws):
    console.log("start_from_url")

    url_input = Element("url-input")
    url = url_input.value

    global current_cube
    current_cube.read_cube_url(url)
    current_cube.init_game()
    update(current_cube)

    cube_modal = Element("cube-modal")
    cube_modal.remove_class("active")

def action_start_from_text(*ags, **kws):
    console.log("start_from_text")

    text_input = Element("text-input")
    text = text_input.value

    global current_cube
    current_cube.read_cube_text(text)
    current_cube.init_game()
    update(current_cube)

    cube_modal = Element("cube-modal")
    cube_modal.remove_class("active")

def get_image_uri(card_name):
    scryfall_api_url = f"https://api.scryfall.com/cards/named?exact={urllib.parse.quote_plus(card_name)}"
    response = pyodide.open_url(scryfall_api_url)
    scryfall_data = json.loads(response.read())
    return str(scryfall_data["image_uris"]["normal"])

def action_click_card(*ags, **kws):
    if ags[0].path[0].localName != "li":
        return
    
    card_name = ags[0].path[0].innerHTML

    if card_name != "**hidden**":
        modal = Element("card-modal")
        modal.add_class("active")

        image_uri = get_image_uri(card_name)

        image = Element("card-image")
        image.element.setAttribute('src', image_uri)




def action_close_card_modal(*ags, **kws):
    modal = Element("card-modal")
    modal.remove_class("active")

## Start Here

modal = Element("loading-modal")
modal.remove_class("active")

cube_modal = Element("cube-modal")
cube_modal.add_class("active")
