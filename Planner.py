import Action as Action


class GoapPlanner:
    def __init__(self, agent, available_actions, world_state, goal_state):
        self.agent = agent
        self.available_actions = available_actions
        self.world_state = world_state
        self.goal_state = goal_state

    def generate_plan(self):
        plan_found = False

        available_nodes = self.actions_to_nodes(self.available_actions)

        open_nodes = list()
        closed_nodes = list()
        world_state_node = self.node(None, 0, self.world_state, None)
        start_node = self.node(None, 0, self.goal_state, Action.Action("start", {}, {}, False))

        action_plan = list()
        open_nodes.append(start_node)
        current_cost = 10000 # TODO - change to some representation of infinity

        while plan_found is False and len(open_nodes) > 0:
        # for i in range(10):
            # print('iteration: ' + str(i))
            current_node = self.lowest_cost_node(open_nodes)
            print(current_node.action.name, current_node.running_cost)
            print(current_node.state)
            if current_node.parent is not None:
                print(current_node.parent.action.name)

            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            plan_found = self.end_state_reached(current_node)
            if plan_found:
                print('Plan Found')
                print(current_node.state)

                n = current_node
                while n.parent is not None:
                    print(n.action.name)
                    n = n.parent

            neighbor_nodes = self.get_node_neighbors(current_node, available_nodes)
            for node in neighbor_nodes:

                if node in closed_nodes:
                    continue

                # copy current node state
                for key in current_node.state.keys():
                    node.state[key] = current_node.state[key]

                # update neighbor state
                for effect in node.action.effects.keys():
                    node.state[effect] -= node.action.effects[effect]

                for precondition in node.action.preconditions.keys():
                    if precondition not in node.state.keys():
                        node.state[precondition] = 0
                    node.state[precondition] += node.action.preconditions[precondition]

                # update cost
                node.running_cost += node.action.cost
                current_cost = node.running_cost
                node.parent = current_node

                open_nodes.append(node)

                print(node.action.name, node.state, node.running_cost)

            print('---')

    def actions_to_nodes(self, available_actions):
        nodes_list = list()
        for action in available_actions:
            nodes_list.append(self.node(None, action.cost, {}, action))

        return nodes_list

    def lowest_cost_node(self, nodes_list):
        lowest_cost = nodes_list[0]
        for node in nodes_list:
            if node.running_cost < lowest_cost.running_cost:
                lowest_cost = node
        return lowest_cost

    def end_state_reached(self, node):
        for world_param in self.world_state.keys():
            if world_param in node.state.keys():
                if node.state[world_param] > self.world_state[world_param]:
                    return False
        return True

    def get_node_neighbors(self, current_node, available_nodes):
        node_neighbors = list()
        for available_node in available_nodes:
            for node_effect in available_node.action.effects:
                if node_effect in current_node.state.keys():
                    node_neighbors.append(available_node)
                    # node_neighbors.append(self.node(None, current_node.running_cost, available_node.state, available_node.action))
                    # node_neighbors.append(self.node(None, current_node.running_cost, {}, available_node.action))
        return node_neighbors

    class node:
        def __init__(self, parent, running_cost, state, action):
            self.parent = parent
            self.running_cost = running_cost
            self.state = state
            self.action = action