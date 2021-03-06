import gamelib
import random
import math
import warnings
from sys import maxsize
import json
import numpy as np

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))


    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        #  self.scored_on_locations = []
        self.continuous_f_0 = 0

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.execute_strategy(game_state)

        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def execute_strategy(self, game_state):
        """
        Execute the strategy

        Building defenses and creating mobile units on offense.
        """

        turn_number = game_state.turn_number
        if turn_number < 5:
            self.starter_build_defences(game_state)
            self.starter_spawn_attackers(game_state)
        else:
            self.static_defense(game_state)
            self.main_decision(game_state)
            self.extra_static_defense(game_state)


    def starter_build_defences(self, game_state):
        """
        Starter strategy for building defenses
        """
        turn_number = game_state.turn_number

        if turn_number == 0:
            turret_locations = [[3, 12], [24, 12], [10, 10], [17, 10]]
            game_state.attempt_spawn(TURRET, turret_locations)
            game_state.attempt_upgrade(turret_locations)

            wall_locations = [[2, 12], [2, 13], [4, 12], [23, 12], [24, 13], [25, 12]]
            game_state.attempt_spawn(WALL, wall_locations)

            game_state.attempt_remove(wall_locations)
        elif turn_number == 1:
            wall_locations = [[1, 13], [2, 12], [3, 13], [24, 13], [25, 12], [26, 13]]
            game_state.attempt_spawn(WALL, wall_locations)

            support_locations = [[17, 6]]
            game_state.attempt_spawn(SUPPORT, support_locations)

            game_state.attempt_remove(wall_locations + support_locations)
        elif turn_number == 2:
            wall_locations_1 = [[4, 11], [5, 10], [6, 9], [7, 8], [8, 7], [9, 6], [10, 5], [11, 4], [12, 3], [13, 2], [14, 2]]
            game_state.attempt_spawn(WALL, wall_locations_1)

            wall_locations_2 = [[15, 3], [16, 4], [17, 5], [18, 6], [19, 7], [20, 8]]
            game_state.attempt_spawn(WALL, wall_locations_2)

            wall_locations_3 = [[0, 13], [1, 13], [2, 13], [26, 13], [27, 13]]
            game_state.attempt_spawn(WALL, wall_locations_3)

            game_state.attempt_remove(wall_locations_3 + [[10,10],[17,10]])
        elif turn_number == 3:
            wall_locations_1 = [[0, 13], [1, 13], [2, 13], [4, 13], [24, 13], [25, 13], [26, 13], [27, 13]]
            game_state.attempt_spawn(WALL, wall_locations_1)

            wall_locations_2 = [[4, 12], [21, 12], [22, 12],[23, 12], [19, 9], [19, 10], [20, 10]]
            game_state.attempt_spawn(WALL, wall_locations_2)

            turret_locations = [[20, 9], [22, 11]]
            game_state.attempt_spawn(TURRET, turret_locations)

            game_state.attempt_remove(wall_locations_1 + wall_locations_2 + turret_locations)
        elif turn_number == 4:
            turret_locations = [[20, 9], [22, 11]]
            game_state.attempt_spawn(TURRET, turret_locations)
            game_state.attempt_upgrade([[20, 9]])

            wall_locations = [[0, 13], [1, 13], [2, 13], [4, 13], [24, 13], [25, 13], [26, 13], [27, 13], [4, 12], [23, 12]]
            game_state.attempt_spawn(WALL, wall_locations)

            game_state.attempt_remove(wall_locations)
        elif turn_number >= 5:
            return


    def starter_spawn_attackers(self, game_state):
        """
        Starter strategy for preparing attackers for action phase
        """
        turn_number = game_state.turn_number

        if turn_number == 0:
            return
        elif turn_number == 1:
            scount_locations = [[20, 6]]
            scount_count = 7
            game_state.attempt_spawn(SCOUT, scount_locations, scount_count)
        elif turn_number == 2:
            interceptor_locations = [[20, 6]]
            interceptor_count = 1
            game_state.attempt_spawn(INTERCEPTOR, interceptor_locations, interceptor_count)
        elif turn_number == 3:
            interceptor_locations = [[22,8],[23,9]]
            interceptor_count = 2
            game_state.attempt_spawn(INTERCEPTOR, interceptor_locations, interceptor_count)
        elif turn_number == 4:
            interceptor_locations = [[22,8]]
            interceptor_count = 2
            game_state.attempt_spawn(INTERCEPTOR, interceptor_locations, interceptor_count)
        elif turn_number >= 5:
            return


    def static_defense(self, game_state):
        """ Building and repairing static defenses.
        """

        # High priority static defenses
        # (a) self repair 1
        wall_locations_a = [[4,11],[5,10],[6,9],[7,8],[8,7],[9,6],[10,5],[11,4],[12,3],[13,2],\
        [14,2],[15,3],[16,4],[17,5],[18,6],[19,7],[20,8]]
        if not self.self_repair(game_state=game_state, locations=wall_locations_a, unit_type=WALL, hp_percent=.5, upgrade=False):
            return
        
        # (b) self repair 2
        upgraded_turret_locations_b = [[3,12],[24,12]]
        if not self.self_repair(game_state=game_state, locations=upgraded_turret_locations_b, unit_type=TURRET, hp_percent=.5, upgrade=True):
          return
        
        # TODO (c) self repair 3
        upgraded_turret_locations_c = [[20,9],[22,11]]
        if not self.self_repair(game_state=game_state, locations=upgraded_turret_locations_c, unit_type=TURRET, hp_percent=.5, upgrade=True):
          return
        
        # TODO turn based static defenses (d) (e) (f)
        turn_number = game_state.turn_number
        if turn_number >= 5 and turn_number <= 20:
            wall_locations_d = [[2,13],[3,13],[24,13],[25,13],[4,12],[23,12]]
            defenses_built = self.build_defenses(game_state, wall_locations_d, WALL, mark_remove=True)
            if defenses_built != len(wall_locations_d):
                return
        elif turn_number >= 21 and turn_number <= 50:
            wall_locations_e = [[2,13],[3,13],[24,13],[25,13],[4,12],[23,12]]
            if not self.self_repair(game_state=game_state, locations=wall_locations_e, unit_type=WALL, hp_percent=.5, upgrade=False):
                return
        elif turn_number >= 51 and turn_number <= 100:
            upgraded_wall_locations_f = [[2,13],[3,13],[24,13],[25,13],[4,12],[23,12]]
            if not self.self_repair(game_state=game_state, locations=upgraded_wall_locations_f, unit_type=WALL, hp_percent=.5, upgrade=True):
                return


    def extra_static_defense(self, game_state):
        # (g)
        SP_before_extra = game_state.get_resource(SP)
        for unit_type, locations, upgrade in [
                (WALL, [[19,11],[20,11]], False),
                (TURRET, [[20,10]], False),
                (TURRET, [[19,10]], False),
                (TURRET, [[20,10]], True),
                (TURRET, [[19,10]], True),
                (SUPPORT, [[14,9],[15,9]], False),
                (SUPPORT, [[14,9],[15,9]], True),
                (WALL, [[19,11],[20,11]], True),
                (TURRET, [[22,12]], False),
                (TURRET, [[22,12]], True),
                (WALL, [[4,13],[5,13],[6,13],[17,12],[18,12],[19,12],[17,11],[18,11]], False),
                (SUPPORT, [[14,8],[15,8]], False),
                (SUPPORT, [[14,8],[15,8]], True),
                (WALL, [[4,13],[5,13],[6,13],[17,12],[18,12],[19,12],[17,11],[18,11]], True),
                ]:
            if upgrade:
                locations_to_upgrade = [location for location in locations \
                    if game_state.contains_stationary_unit(location) and not game_state.contains_stationary_unit(location).upgraded]
                if locations_to_upgrade:
                    number_upgraded = game_state.attempt_upgrade(locations_to_upgrade)
                    if len(locations_to_upgrade) != number_upgraded:
                        return
            else:
                if not self.self_repair(game_state, locations, unit_type, hp_percent=0.5):
                    return
            if game_state.get_resource(SP) < SP_before_extra * 0.6:
                gamelib.debug_write("\u001b[32m extra static defense in turn {}: {} {} \u001b[0m".format(game_state.turn_number, game_state.get_resource(SP), SP_before_extra))
                return



    def build_defenses(self, game_state, locations, unit_type, upgrade=False, mark_remove=False):
        """ Build defenses at given locations.

        If upgrade==True, try to build as many updated buildings as possible, then try to build the
        unupgraded buildings.
        """
        # TODO check if can afford
        base_unit_cost = game_state.type_cost(unit_type)[SP]
        if upgrade:
            unit_cost = base_unit_cost + game_state.type_cost(unit_type, upgrade=True)[SP]
        else:
            unit_cost = base_unit_cost
        available_SP = game_state.get_resource(SP)
        number_affordable = int(available_SP // unit_cost)
        gamelib.debug_write('\u001b[32m number_affordable: {} \u001b[0m'.format(number_affordable))

        # TODO if yes, build them, else return False
        if number_affordable == 0:
            if upgrade:
                return self.build_defenses(game_state, locations, unit_type, upgrade=False, mark_remove=mark_remove)
            else:
                return False
        else:
            build_status = game_state.attempt_spawn(unit_type, locations[:number_affordable])
            if upgrade:
                upgrade_status = game_state.attempt_upgrade(locations[:number_affordable])
                if build_status != upgrade_status:
                    raise Exception("Number of spawn buildings does not match upgraded buildings.")
                if number_affordable < len(locations):
                    build_status += self.build_defenses(game_state, locations[number_affordable:], unit_type, upgrade=False, mark_remove=mark_remove)
            if mark_remove:
                game_state.attempt_remove(locations[:number_affordable])
            return build_status


    def self_repair(self, game_state, locations, unit_type, hp_percent, upgrade=False):
        """ Self repair buildings

        If the buildings don't exist, build them.
        If the buildings are below the hp_percent, mark them for remove.

        Build defenses with hierarchy.
        """
        building_hierarchy = [TURRET, WALL, SUPPORT]

        hierarchy_index = building_hierarchy.index(unit_type)

        # find buildings to build
        locations_to_build = [location for location in locations if not game_state.contains_stationary_unit(location)]
        number_to_build = len(locations_to_build)

        # find buildings to remove
        locations_to_remove = self.find_low_hp_buildings(game_state=game_state, locations=locations, hp_percent=hp_percent)
        if locations_to_remove:
            game_state.attempt_remove(locations_to_remove)

        # build defenses in hierarchy
        defenses_built = 0
        for target_type in building_hierarchy[hierarchy_index:]:
            if locations_to_build:
                defenses_built += self.build_defenses(game_state, locations=locations_to_build[:], unit_type=target_type, upgrade=upgrade, mark_remove=False)
                locations_to_build = locations_to_build[defenses_built:]
        return defenses_built == number_to_build


    def find_low_hp_buildings(self, game_state, locations, hp_percent):
        """ Find the buildings with hit points below hp_percent.
        """
        low_hp_locations = []

        for location in locations:
            unit = game_state.contains_stationary_unit(location)
            if unit and unit.health/unit.max_health < hp_percent: 
            # TODO Can .max_health give the health of an upgraded unit??
                low_hp_locations.append(location)


        return low_hp_locations


    def main_decision(self, game_state):
        """ The main responsive active defense and offense strategy.
        """
        a, b, c, d, e, f, h, mp, sp, mp_l, sp_l = self.decision_function(game_state)

        gamelib.debug_write(f"\u001b[32m main decision at round {game_state.turn_number}: a={a}, b={b}, c={c}, d={d}, e={e}, f={f}, mp_l={mp_l}, sp_l={sp_l} \u001b[0m")

        if d != 0:
            # Demolisher
            game_state.attempt_spawn(DEMOLISHER, [15,1])
        if e != 0:
            # Interceptor
            game_state.attempt_spawn(INTERCEPTOR, [19,5])
        if h != 0:
            # Scounts
            game_state.attempt_spawn(SCOUT, [15,1], h)
        if f == 0:
            # left & right active defense
            gamelib.debug_write("\u001b[32m active defense on left & right \u001b[0m")
            self.active_defense(game_state, defense_type=0) # left
            self.active_defense(game_state, defense_type=1) # right
        elif f == 1:
            # left active defense
            self.active_defense(game_state, defense_type=0) # left

            if sp >= 9:
                # 9 (c)
                if a != 0:
                    # TODO send scount
                    scount_location_a = [[11,2]]
                    game_state.attempt_spawn(SCOUT, scount_location_a, a)
                if b != 0:
                    scount_location_b = [[10,3]]
                    game_state.attempt_spawn(SCOUT, scount_location_b, b)
                if not self.build_defenses(game_state, [[21, 10]], WALL, mark_remove=True):
                    gamelib.debug_write(f"\u001b[31m building wall at [[21, 10]] failed\u001b[0m")
                    return
            else:
                self.active_defense(game_state, defense_type=1) # right
        elif f == 2:
            # right active defense
            self.active_defense(game_state, defense_type=1) # right

            if sp >= 9:
                # 9 (c)
                if a != 0:
                    # TODO send scount
                    scount_location_a = [[19,5]]
                    game_state.attempt_spawn(SCOUT, scount_location_a, a)
                if b != 0:
                    scount_location_b = [[20,6]]
                    game_state.attempt_spawn(SCOUT, scount_location_b, b)
                if not self.build_defenses(game_state, [[21, 10]], WALL, mark_remove=True):
                    gamelib.debug_write(f"\u001b[31m building wall at [[21, 10]] failed\u001b[0m")
                    return
            else:
                self.active_defense(game_state, defense_type=0) # left
        if (f != 0) and (c != 0):
            # Support
            support_locations = [[13,3],[14,3],[15,4],[16,5],[17,6],[18,7],[14,4],[15,5],[16,6],[17,7]]
            self.build_defenses(game_state=game_state, locations=support_locations[:c], unit_type=SUPPORT, upgrade=False, mark_remove=True)

        return 1


    def decision_function(self, game_state):
        """ The decision function for the main stage of the game.
        """
        x, y, z, x_1, y_1, z_1, w, w_1, mp, sp, health, r, m = self.gather_info_from_gamestate(game_state)
        a, b, c, d, e, f, d, h, mp_l, sp_l = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        gamelib.debug_write(f"\u001b[32m decision_function at round {r}: " \
            f"x={x} y={y} z={z} x_1={x_1} y_1={y_1} z_1={z_1} w={w} w_1={w_1} mp={mp} sp={sp} health={health} r={r} \u001b[0m")

        # TODO main decision for the strategy
        #  e = (5<= r < 20) + 2*(20 <= r <40) + 3*(40 <= r < 60) + 4*(60 <= r < 80) + 5*(r <= 100)
        # TODO if r in [0, 100) the following is the optimal approach
        e = r // 20 + 1
        term_a = self.g_function((x + .25*z)*w, y*w, w)
        term_b = self.g_function(x + 0.25*z, y, w)
        term_a_1 = self.g_function((x_1+.25*z_1)*w_1, y_1*w_1, w_1)
        term_b_1 = self.g_function(x_1+0.25*z_1, y_1, w_1)

        gamelib.debug_write(f"\u001b[32m decision_function at round {r}: term_a={term_a}, term_b={term_b}, term_a_1={term_a_1}, term_b_1={term_b_1} \u001b[0m")

        if (mp <= term_a - 5.5*w + term_b + 4 + r//20) and (mp <= term_a_1 - 5.5*w_1 + term_b_1 + 4 + r//20):
            f = 0
            self.continuous_f_0 += 1
            c = 0
            a = 0
            b = 0
        elif ((term_a - 5.5*w + term_b) == 0) or ((term_a_1 - 5.5*w_1 + term_b_1) == 0):
            if mp >= 10:
                self.continuous_f_0 = 0
                c = 2
                a = 6
                b = mp - a
                if ((term_a - 5.5*w + term_b) == 0) and ((term_a_1 - 5.5*w_1 + term_b_1) != 0):
                    f = 1
                elif ((term_a - 5.5*w + term_b) != 0) and ((term_a_1 - 5.5*w_1 + term_b_1) == 0):
                    f = 2
                else:
                    f = random.randint(1, 2)
            else:
                f = 0
                self.continuous_f_0 += 1
                c = 0
                a = 0
                b = 0
        # TODO the above condition may not be necessary since all variables are intialed as 0
        elif (term_b - 5.5*w)/(term_a - 5.5*w + term_b) >= (term_b_1 - 5.5*w_1)/(term_a_1 - 5.5*w_1 + term_b_1):
            f = 1
            self.continuous_f_0 = 0
            c = 2
            a = term_a_1
            b = mp - a
        elif (term_b - 5.5*w)/(term_a - 5.5*w + term_b) < (term_b_1 - 5.5*w_1)/(term_a_1 - 5.5*w_1 + term_b_1):
            f = 2
            self.continuous_f_0 = 0
            c = 2
            a = term_a
            b = mp - a

        if f == 0 and self.continuous_f_0 == 9:
            if m == 1:
                d = int((mp - e)//3)
            elif m == 0:
                h = int(mp - e)
            self.continuous_f_0 = 0
        else:
            d = 0


        a = int(a)
        b = int(b)

        sp_l = sp - c
        mp_l = mp - a - b - 2*d - e

        return a, b, c, d, e, f, h, mp, sp, mp_l, sp_l

    def g_function(self, i, j, t):
        """A function used in decision_function.
        """
        g = 5.5*t + 2*i + 3*j

        return g

    def gather_info_from_gamestate(self, game_state):
        """ Gather information from GameState for the decision function.
        """
        x, y, z, x_1, y_1, z_1, w, w_1, mp, sp, health, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        # TODO parse information from the GameState object
        r = game_state.turn_number
        health = game_state.my_health # my health
        mp = game_state.get_resource(MP) # my mobile points
        sp = game_state.get_resource(SP) # my structure points
        # total number of Turret(not upgraded)
        locations_z = [[0,14],[1,15],[2,15],[1,14],[2,14],[3,14]]
        for location in locations_z:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == False):
                z += 1

        locations_z_1 = [[25,15],[26,15],[24,14],[25,14],[26,14],[27,14]]
        for location in locations_z_1:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == False):
                z_1 += 1

        # total number of UPGRADED Turret

        locations_x = [[1,15],[2,15]]
        for location in locations_x:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == True):
                x += 1

        locations_y = [[0,14],[1,14],[2,14],[3,14]]
        for location in locations_y:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == True):
                y += 1

        locations_x_1 = [[25,15],[26,15]]
        for location in locations_x_1:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == True):
                x_1 += 1

        locations_y_1 = [[24,14],[25,14],[26,14],[27,14]]
        for location in locations_y_1:
            unit = game_state.contains_stationary_unit(location)
            if unit and (unit.unit_type == TURRET) and (unit.upgraded == True):
                y_1 += 1

        # w=0 represents empty grid, w=1 represents wall, w = 2 represents upgraded wall
        location_w = [0,14]
        unit_w = game_state.contains_stationary_unit(location_w)
        if not unit_w:
            w = 0
        elif (WALL == unit_w.unit_type) and (unit_w.upgraded == False):
            w = 1
        elif (WALL == unit_w.unit_type) and (unit_w.upgraded == True):
            w = 2

        location_w_1 = [27,14]
        unit_w_1 = game_state.contains_stationary_unit(location_w_1)
        if not unit_w_1:
            w_1 = 0
        elif WALL == unit_w_1.unit_type:
            if unit_w_1.upgraded == False:
                w_1 = 1
            else:
                w_1 = 2

        x_start = 7
        x_range = 14
        y_start = 9
        y_range = 4
        locations = np.array(np.unravel_index(np.arange(x_range * y_range), (x_range, y_range))).T + np.array([x_start, y_start])
        s_count = 0
        s_threshold = 14
        m = 0
        for location in locations:
            unit = game_state.contains_stationary_unit(location)
            if unit and unit.unit_type in [WALL, TURRET]:
                s_count += 0
                if s_count > s_threshold:
                    m = 1
                    break


        return x, y, z, x_1, y_1, z_1, w, w_1, mp, sp, health, r, m

    def get_active_defense_locations(self, defense_type):
        """ Return the coordinates for active defense strategy

        defense_type: left(0), right(1)
        """
        if defense_type == 0:
            # Left active defense
            locations_ours = [[0,13],[1,13],[1,12],[2,12]]
            locations_oppo = [[1,14],[2,14],[1,15]]
            return locations_ours, locations_oppo
        elif defense_type == 1:
            # Right active defense
            locations_ours = [[27,13],[26,13],[26,12],[27,12]]
            locations_oppo = [[26,14],[2,15],[25,15]]
            return locations_ours, locations_oppo
        else:
            raise ValueError


    def active_defense(self, game_state, defense_type):
        """ Build active defenses

        defense_type: left(0), right(1)
        """
        active_locations, opponent_sites = self.get_active_defense_locations(defense_type)
        oppo_MP = game_state.get_resource(MP, player_index=1)

        # if certain state is empty or marked deleted
        state_1 = (not game_state.contains_stationary_unit(opponent_sites[0])) or (game_state.contains_stationary_unit(opponent_sites[0]).pending_removal)
        state_2 = (not game_state.contains_stationary_unit(opponent_sites[1])) or (game_state.contains_stationary_unit(opponent_sites[1]).pending_removal)
        state_3 = (not game_state.contains_stationary_unit(opponent_sites[2])) or (game_state.contains_stationary_unit(opponent_sites[2]).pending_removal)
        gamelib.debug_write(f"\u001b[32m active defense at round {game_state.turn_number}: state_1={state_1} state_2={state_2} state_3={state_3} \u001b[0m")
        # trigger == 1, when {[1,14],[2,14]} or {[1,14],[1,15]} are empty or deleted, == 0 otherwise
        #  trigger = (state_1 and state_2) or (state_1 and state_3)
        trigger = state_1 and (state_2 or state_3)
        # marked deleted: game_state.contains_stationary_unit(location).pending_removal
        gamelib.debug_write(f"\u001b[32m building active defense at round {game_state.turn_number} on type {defense_type}\u001b[0m")
        if self.build_defenses(game_state, active_locations[:2], WALL, mark_remove=True) < 2:
            gamelib.debug_write(f"\u001b[31m active defense at round {game_state.turn_number} failed on type {defense_type} \u001b[0m")
            return
        #  if game_state.attempt_spawn(WALL, active_locations[:2]) < 2:
        #      return
        if trigger:
            if oppo_MP >= 15:
                if not game_state.attempt_upgrade(active_locations[:2]):
                    return
            if oppo_MP >= 25:
                if self.build_defenses(game_state, active_locations[2], TURRET, mark_remove=True):
                    return
                #  if not game_state.attempt_spawn(TURRET, active_locations[2]):
                #      return
                if not game_state.attempt_upgrade(active_locations[2]):
                    return
            if oppo_MP >= 35:
                if self.build_defenses(game_state, active_locations[3], TURRET, mark_remove=True):
                    return
                if not game_state.attempt_upgrade(active_locations[3]):
                    return
            #  if oppo_MP >= 45:
            #      if self.build_defenses(game_state, active_locations[3], TURRET, mark_remove=True):
            #          return
            #      #  if not game_state.attempt_spawn(TURRET, active_locations[3]):
            #      #      return
            #      if not game_state.attempt_upgrade(active_locations[3]):
            #          return


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
