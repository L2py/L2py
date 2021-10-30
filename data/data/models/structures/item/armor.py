import typing
from dataclasses import dataclass, field

from data.models.structures.skill.skill import Skill

from .item import Item, ItemBases, ItemDefaults


@dataclass
class ArmorBases(ItemBases):
    avoid_modifier: Int32
    physical_defense: Int32
    magic_defense: Int32
    mp_bonus: Int32
    hp_bonus: Int32


@dataclass
class ArmorDefaults(ItemDefaults):
    passive_skill: typing.Union[None, Skill] = None


@dataclass
class Armor(Item, ArmorDefaults, ArmorBases):
    pass