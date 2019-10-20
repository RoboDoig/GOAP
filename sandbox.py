import Action as Action
import World as World
import ReverseRecursivePlanner as Planner

planner = Planner.GoapPlanner("planner", World.world_actions, World.state, World.goal)

planner.generate_plan()

