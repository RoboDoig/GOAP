
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

        start = self.Node(None, 0, self.world_state, None)

        success = self.build_graph(start, leaves, usable_actions, self.goal_state)

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

    def build_graph(self, parent, leaves, usable_actions, goal_state):
        self.count += 1

        found_solution = False

        for action in usable_actions:
            # if the parent state has effects matching this state's preconditions, we can use it here
            # - compress to function
            neighbor = True
            for precondition in action.preconditions.keys():
                if parent.state[precondition] < action.preconditions[precondition]:
                    neighbor = False

            # if neighbor, create new node with parent state + this action's effects
            # TODO-running cost should reflect distance from goal
            if neighbor:
                node = self.Node(parent, parent.running_cost+action.cost, {}, action)
                # node.running_cost += self.node_distance_from_state(node, goal_state)
                for state_param in parent.state:
                    node.state[state_param] = parent.state[state_param]

                    if state_param in action.effects.keys():
                        node.state[state_param] += action.effects[state_param]

                    if state_param in action.preconditions.keys():
                        node.state[state_param] -= action.preconditions[state_param]

                # did we reach the goal?
                if self.node_satisfies_state(node, goal_state):
                    leaves.append(node)
                    found_solution = True
                else:
                    # not a solution, so test remaining actions and branch out the tree
                    action_subset = list()
                    for sub_action in usable_actions:
                        if sub_action is not action:
                            action_subset.append(sub_action)
                    found = self.build_graph(node, leaves, action_subset, goal_state)
                    if found:
                        found_solution = True

        return found_solution

    def node_satisfies_state(self, node, state):
        for param in state:
            if node.state[param] < state[param]:
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