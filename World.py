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
    Action("Build", {'wood': 2, 'stone': 1}, {'house': 1, 'gold': 2}, False, cost=1),
    Action("SellWood", {'wood': 1}, {'gold': 1}, False),
    Action("SellWood", {'wood': 1}, {'gold': 1}, False),
    Action("PickUpWood", {}, {'wood': 1}, False),
    Action("PickUpWood", {}, {'wood': 1}, False),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=10),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpGold", {}, {'gold': 1}, False, cost=2),
    Action("PickUpStone", {}, {'stone': 1}, False),
    Action("Build", {'wood': 2, 'stone': 1}, {'house': 1, 'gold': 2}, False, cost=1)
]

state = {
    'gold': 2,
    'wood': 0,
    'stone': 0,
    'axe': 0,
    'house': 0
}

goal = {
    'gold': 2,
    'house': 1,
    'stone': 1
}