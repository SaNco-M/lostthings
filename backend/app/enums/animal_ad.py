from enum import Enum


class AnimalCategory(str, Enum):
    DOGS = "dogs"
    CATS = "cats"
    BIRDS = "birds"
    RABBITS = "rabbits"
    RODENTS = "rodents"
    REPTILES = "reptiles"
    AMPHIBIANS = "amphibians"
    FISH = "fish"
    FERRETS = "ferrets"
    LIVESTOCK = "livestock"
    HORSES = "horses"
    EXOTIC_ANIMALS = "exotic_animals"
    OTHER_ANIMALS = "other_animals"
