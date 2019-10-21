from copy import deepcopy

class GoapPlanner:
    def __init__(self, agent, available_actions, world_state, goal_state):
        self.agent = agent
        self.available_actions = available_actions
        self.world_state = world_state
        self.goal_state = goal_state

    def generate_plan(self):
        plan_found = False

        open_nodes = list()
        closed_nodes = list()
        action_plan = list()

        world_state_node = self.Node(None, 0, self.world_state, None, self.available_actions)
        goal_state_node = self.Node(None, 0, self.goal_state, None, list())

        open_nodes.append(world_state_node)
        current_cost = 10000 # placeholder, should technically be some representation of Inf

        while plan_found is False and len(open_nodes) > 0:
            current_node = self.lowest_cost_node(open_nodes)
            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            print(current_node.state)
            plan_found = self.end_state_reached(current_node)

            if plan_found:
                print('plan found')
                while current_node.parent is not None:
                    print(current_node.action.name)
                    current_node = current_node.parent

            # what actions are possible to take from this node?
            neighbors = self.get_neighbors(current_node)

            # add these actions as nodes to the tree
            for neighbor in neighbors:
                # first generate a fresh child node, tick over the running cost, copy the parent's state...
                # add the neighbor action, copy the available actions, then remove the neighbor action
                neighbor_node = self.Node(current_node, current_node.running_cost+neighbor.cost,
                                          deepcopy(current_node.state), neighbor, current_node.available_actions)
                neighbor_node.available_actions.remove(neighbor)

                # update node with action effects (add effects to state)
                for effect in neighbor.effects.keys():
                    if effect not in neighbor_node.state.keys():
                        neighbor_node.state[effect] = 0
                    neighbor_node.state[effect] += neighbor.effects[effect]

                # update node with actions preconditions (subtract preconditions from state)
                for precondition in neighbor.preconditions.keys():
                    if precondition not in neighbor_node.state.keys():
                        neighbor_node.state[precondition] = 0
                    neighbor_node.state[precondition] -= neighbor.preconditions[precondition]

                current_cost = neighbor_node.running_cost
                open_nodes.append(neighbor_node)

    def lowest_cost_node(self, nodes_list):
        lowest_cost = nodes_list[0]
        for node in nodes_list:
            if node.running_cost < lowest_cost.running_cost:
                lowest_cost = node
        return lowest_cost

    def end_state_reached(self, node):
        for goal_param in self.goal_state:
            if goal_param in node.state.keys():
                if node.state[goal_param] < self.goal_state[goal_param]:
                    return False
            else:
                return False
        return True

    def get_neighbors(self, node):
        neighbors = list()
        for action in node.available_actions:
            if self.is_neighbor(action, node):
                neighbors.append(action)

        return neighbors

    def is_neighbor(self, action, node):
        for precondition in action.preconditions.keys():
            if precondition in node.state.keys():
                if node.state[precondition] < action.preconditions[precondition]:
                    return False
            else:
                return False
        return True

    class Node:
        def __init__(self, parent, running_cost, state, action, available_actions):
            self.parent = parent
            self.running_cost = running_cost
            self.state = state
            self.action = action
            self.available_actions = available_actions[:]