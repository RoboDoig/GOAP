import Action as Action
import World as World
# import Planner2 as Planner
import ReversePlanner as Planner

for key in World.state.keys():
    if key in World.goal.keys():
        World.goal[key] += World.state[key]
    else:
        World.goal[key] = World.state[key]

print(World.goal)
print('---------')

planner = Planner.GoapPlanner("planner", World.world_actions, World.state, World.goal)

planner.generate_plan()

