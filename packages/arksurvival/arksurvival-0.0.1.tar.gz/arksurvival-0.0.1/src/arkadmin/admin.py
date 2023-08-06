from requests import RequestException
import requests
import os


class Admin:
    admin = None

    def __init__(self, url=None, key=None):
        self.key = key or os.getenv('ARK_ADMIN')
        self.url = url or "https://ark-admin-manager.herokuapp.com"

    def command(self, code):
        resp = requests.post(self.url + "/command", params={"cheat": code})
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def rename_player(self, current_name, new_name):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def rename_tribe(self, current_name, new_name):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def ban_player(self, player_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def unban_player(self, player_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def disable_spectator(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport(self, command):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_green_obelisk(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_blue_obelisk(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_red_obelisk(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_king_titan_terminal(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_desert_titan_terminal(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_forest_titan_terminal(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_ice_titan_terminal(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_to_playerid(self, player_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_to_player_name(self, name):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_player_id_to_me(self, player_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_player_name_to_me(self, name):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_gps_coords(self, lattitude, longitude, altitude):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_xyz(self, x, y, z):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_target_xyz(self, x, y, z):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def kill_target(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_tribes_dinos(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_tribes_dinos_by_id(self, tribe_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_players_by_tribeid(self, tribe_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_tribe_by_id(self, tribe_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_structures_by_tribeid(self, tribe_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_tribe_structures(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def destroy_wild_dinos(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def force_player_to_join_target_tribe(self, player_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def force_myself_into_target_tribe(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def force_myself_tribe_admin(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def force_myself_tribe_owner(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def give_experience_to_player(self, player_id, amount, from_tribe_share=False, prevent_sharing_with_tribe=True):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def add_experience_on_mounted_dino(self, amount, from_tribe_share=False, prevent_sharing_with_tribe=True):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def enemy_ignores_me(self, condition=True):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def ghost(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def give_item_to_player(self, player_id, blueprint_path, quantity=1, quality=0, force_blueprint=False):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def give_items_to_player(self, player_id, blueprint_paths, quantity=1, quality=0, force_blueprint=False):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def hide_admin_icon(self, condition=True):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def tranquilize_target(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def wake_up_target(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def add_hexagons(self, amount):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def tame(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def spawn_dino(self, blueprint_path, tamed=False, level=0):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def spawn_dinos(self, *blueprint_paths, level=0, tamed=True):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def remove_cryosickness(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def spawn_exact_dino(self, dino_blueprint_path="", saddle_blueprint_path="", saddle_quality=0,
                         base_level=150, extra_levels=0, base_stats="0,0,0,0,0,0,1,1",
                         added_stats="0,0,0,0,0,0,0,0", dino_name="", cloned=0, neutered=0,
                         tamed_on="", uploaded_from="", imprinter_name="", imprinter_player_id=0,
                         imprint_quality=0, colors="0,0,0,0,0,0", dino_id=0, exp=0,
                         spawn_distance=0, y_offset=0, z_offset=0):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def set_target_dino_color(self, color_region: int, color_id: int):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def copy_coords(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def teleport_exact(self, x, y, z, yaw, pitch):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def paste_teleport(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def get_tribe_id_player_list(self, tribe_id):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def spawn_beacon(self, blueprint_path):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def spawn_beaver_dam(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def broadcast(self, message):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def give_engram_to(self, player_id, engram=None):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok

    def restart_application(self):
        resp = requests.post(self.url + "")
        if not resp.ok:
            raise RequestException(f"Error occurred sending a command: {resp.reason}")
        return resp.ok
