import numpy as np
import points as pt
from characters import barbarians, dragons, balloons, archers, stealth_archers, healers


class Building:
    def destroy(self):
        self.destroyed = True
        if self.type == 'wall':
            self.V.remove_wall(self)
        elif self.type == 'hut':
            self.V.remove_hut(self)
        elif self.type == 'cannon':
            self.V.remove_cannon(self)
        elif self.type == 'wizardtower':
            self.V.remove_wizard_tower(self)
        elif self.type == 'townhall':
            self.V.remove_town_hall(self)


class Hut(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 40
        self.max_health = 40
        self.type = 'hut'


class Cannon(Building):
    var=0
    def __init__(self, position, V, level):
        if level==1:
            if Cannon.var >= len(pt.config_level_1['cannons_level']):
                Cannon.var = 0
            bd_level = pt.config_level_1['cannons_level'][Cannon.var]
        elif level==2:
            if Cannon.var >= len(pt.config_level_2['cannons_level']):
                Cannon.var = 0
            bd_level = pt.config_level_2['cannons_level'][Cannon.var]
        elif level==3:
            if Cannon.var >= len(pt.config_level_3['cannons_level']):
                Cannon.var = 0
            bd_level = pt.config_level_3['cannons_level'][Cannon.var]
        Cannon.var=Cannon.var+1

        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 60 + (30*bd_level)
        self.max_health = 60 + (30*bd_level)
        self.type = 'cannon'
        self.attack = 4 + bd_level
        self.attack_radius = 5 + (bd_level/2)
        self.isShooting = False

    def scan_for_targets(self, King):
        self.isShooting = False

        troops = barbarians + archers + stealth_archers + healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop)
                return

        # for barb in barbarians:
        #     if (barb.position[0] - self.position[0])**2 + (barb.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(barb)
        #         return
        # for dragon in dragons:
        #     if (dragon.position[0] - self.position[0])**2 + (dragon.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(dragon)
        #         return

        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King)

    def attack_target(self, target):
        if(self.destroyed == True):
            return
        target.deal_damage(self.attack)


class Wall(Building):
    var=0
    def __init__(self, position, V, level, King):
        if Wall.var >= len(pt.config_level_1['walls_level']):
            Wall.var = 0
        bd_level = pt.config_level_1['walls_level'][Wall.var]
        Wall.var = Wall.var + 1

        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 20
        self.max_health = 20 + (40*bd_level)
        self.type = 'wall'
        self.King = King
        self.level = bd_level

    def destroy(self):
        print(self.health)
        if self.level >= 3:
            troops = barbarians + archers + stealth_archers + healers + [self.King]
            for troop in troops:
                if ((abs(troop.position[0] - self.position[0]) + abs(troop.position[1] - self.position[1])) <= 2):
                    troop.deal_damage(200)
            self.V.remove_wall(self)
            Wall.var = Wall.var - 1

class TownHall(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (4, 3)
        self.V = V
        self.destroyed = False
        self.health = 100
        self.max_health = 100
        self.type = 'townhall'


class WizardTower(Building):
    var=0
    def __init__(self, position, V, level):
        if level==1:
            if WizardTower.var >= len(pt.config_level_1['wizard_towers_level']):
                WizardTower.var = 0
            bd_level = pt.config_level_1['wizard_towers_level'][WizardTower.var]
        elif level==2:
            if WizardTower.var >= len(pt.config_level_2['wizard_towers_level']):
                WizardTower.var = 0
            bd_level = pt.config_level_2['wizard_towers_level'][WizardTower.var]
        elif level==3:
            if WizardTower.var >= len(pt.config_level_3['wizard_towers_level']):
                WizardTower.var = 0
            bd_level = pt.config_level_3['wizard_towers_level'][WizardTower.var]
        WizardTower.var = WizardTower.var + 1

        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 60 + (30*bd_level)
        self.max_health = 60 + (30*bd_level)
        self.type = 'wizardtower'
        self.attack = 4 + bd_level
        self.attack_radius = 5 + (bd_level/2)
        self.isShooting = False

    def scan_for_targets(self, King):
        self.isShooting = False
        troops = barbarians+ archers + dragons + balloons + stealth_archers + healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop,0)
                return

        print(self.health)
        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King,1)

    def attack_target(self, target, isKing):
        if(self.destroyed == True):
            return

        if isKing == 1:
            target.deal_damage(self.attack)
        i = target.position[0] - 1
        j = target.position[1] - 1
        troops = barbarians+ archers + dragons + balloons + stealth_archers
        for row in range(i, i+3):
            for col in range(j, j+3):
                if(row < 0 or col < 0):
                    continue
                for troop in troops:
                    if(troop.position[0] == row and troop.position[1] == col):
                        troop.deal_damage(self.attack)


def shoot_cannons(King, V):
    for cannon in V.cannon_objs:
        V.cannon_objs[cannon].scan_for_targets(King)


def shoot_wizard_towers(King, V):
    for tower in V.wizard_tower_objs:
        V.wizard_tower_objs[tower].scan_for_targets(King)
