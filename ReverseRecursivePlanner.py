
class GoapPlanner:
    def __init__(self, agent, available_actions, world_state, goal_state):
        self.agent = agent
        self.available_actions = available_actions
        self.world_state = world_state
        self.goal_state = goal_state

        self.count = 0

    def generate_plan(self):
        # action reset

        # check procedural on actions

        usable_actions = self.available_actions

        leaves = list()

        start = self.Node(None, 0, self.goal_state, None)

        success = self.build_graph(start, leaves, usable_actions, self.world_state)

        # if no plan found
        if not success:
            print('plan not found')
            return None
        else:
            print('plan found!', self.count)

        # get cheapest leaf
        cheapest = None
        for leaf in leaves:
            if cheapest is None:
                cheapest = leaf
            else:
                if leaf.running_cost < cheapest.running_cost:
                    cheapest = leaf

        # get its node and work back through parents
        result = list()
        n = cheapest
        while n is not None:
            if n.action is not None:
                result.insert(0, n.action)
            n = n.parent

        for task in result:
            print(task.name)

    def build_graph(self, parent, leaves, usable_actions, world_state):
        self.count += 1

        found_solution = False

        for action in usable_actions:
            # an action is a neighbor if any of its effects would positively contribute to state parameter of the parent
            neighbor = False
            for effect in action.effects.keys():
                if effect in parent.state.keys() and action.effects[effect] > 0:
                    neighbor = True
                    break

            # if neighbor, create new node with parent state - subtract this action's effects, and add its preconditions
            # TODO-running cost should reflect distance from goal
            if neighbor:
                node = self.Node(parent, parent.running_cost+action.cost, {}, action)
                # copy parent state
                for state_param in parent.state:
                    node.state[state_param] = parent.state[state_param]

                # subtract the action's effects
                for effect in action.effects.keys():
                    if effect not in node.state.keys():
                        node.state[effect] = 0
                    node.state[effect] -= action.effects[effect]

                # add the action's preconditions
                for precondition in action.preconditions.keys():
                    if precondition not in node.state.keys():
                        node.state[precondition] = 0
                    node.state[precondition] += action.preconditions[precondition]

                # did we reach the goal?
                if self.node_satisfies_state(node, world_state):
                    leaves.append(node)
                    found_solution = True
                else:
                    # not a solution, so test remaining actions and branch out the tree
                    action_subset = list()
                    for sub_action in usable_actions:
                        if sub_action is not action:
                            action_subset.append(sub_action)
                    found = self.build_graph(node, leaves, action_subset, world_state)
                    if found:
                        found_solution = True

        return found_solution

    def node_satisfies_state(self, node, state):
        # we satisfy the state if every node state parameter is less than or equal to the value for the defined state
        for param in node.state:
            if node.state[param] > state[param]:
                return False
        return True

    def node_distance_from_state(self, node, state):
        distance = 0
        for param in state:
            if param in node.state.keys():
                distance += (state[param] - node.state[param])
        return distance

    class Node:
        def __init__(self, parent, running_cost, state, action):
            self.parent = parent
            self.running_cost = running_cost
            self.state = state
            self.action = action