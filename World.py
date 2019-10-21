from Action import Action

world_actions = [
    Action("SellWood", {'wood': 1}, {'gold': 1}, False),
    Action("SellWood", {'wood': 1}, {'gold': 1}, False),
    Action("PickUpWood", {}, {'wood': 1}, False),
    Action("PickUpWood", {}, {'wood': 1}, False),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=10),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpStone", {}, {'stone': 1}, False),
]

state = {
    'gold': 0,
    'wood': 0,
    'stone': 0,
    'axe': 0
}

goal = {
    'gold': 2,
    'wood': 1,
    'stone': 1,
}