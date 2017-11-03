
class PolarBear:
    """
        Solution for https://stepik.org/lesson/59290/step/1

        Args:
            n : `int` basis size for poly
    """

    #
    # Label types
    #
    INPUT, NOT, OR, AND = range(4) # label types
    verbose = [None, "NOT", "OR", "AND",] # verbose label types for printing
    executive = [lambda x: None,
                 lambda x: int(not x[0]),
                 lambda x: int(any(x)),
                 lambda x: int(all(x)),] # related functions

    def __init__(self, n):
        self.n = n
        self.reversed_linklist = {} # graph repr
        self.collected_function_set = []
        self.graph_evaluated = True

        # adding inputs
        for i in range(self.n):
            self._add_vertex(self.INPUT)
        self.collect_functions()


    def __str__(self):
        """
            Returns graph's representation as required in task.
        """
        s = ''
        # printing edges
        for key, (label_ty, links) in self.reversed_linklist.items():
            for v_from in links:
                s += "{v_from} {v_to}\n".format(v_from = v_from, v_to = key)
        # printing functional labels
        for key, (label_ty, links) in self.reversed_linklist.items():
            if label_ty != self.INPUT:
                s += "{v_index} {ty}\n".format(v_index = key, ty = self.verbose[label_ty])
        return s


    def __len__(self):
        return len(self.reversed_linklist)


    def add_vertex(self, label_ty, v_from):
        """
            Adds a new functional vertex if it's addition will
            allow to compute another function

            Args:
                label_ty : `int` : One of the label types
                v_from : `list` : List of parent vertex ids

            Returns:
                `int or None` : New vertex id or None if it's not contibuting
                to the function set
        """
        neo = self._add_vertex(label_ty, v_from)

        new_function = self.evaluate_vertex(neo)

        if new_function not in self.collected_function_set:
            self.collected_function_set.append(new_function)
        else:
            self._delete_vertex(neo)
            return None

        self.graph_evaluated = True
        return neo


    def inputs(self):
        """
            Returns list of ids of graph's inputs.
        """
        if self.reversed_linklist is None:
            self.reversed_linklist = self.reversed_linklist
        return [key for key, (label_ty, _) in self.reversed_linklist.items()
                if label_ty == self.INPUT]


    def evaluate_vertex(self, vtx):
        """
            Forwards values on graph to compute a functions in vtx.
            Args:
                vtx : `int` : Id of vertex in which to compute function.

            Returns:
                `list` : Function as a list with len = 2**self.n
        """
        new_function = []
        for values in self.generate_inputs(length = self.n, ranges = [0, 1]):
            evaluation = self._initiate_evaluation(values = values)
            val = self._evaluate_vertex(v = vtx,
                                        evaluation = evaluation)
            new_function.append(val)
        return new_function


    def collect_functions(self):
        """
            Forwards the graph if needed and computes the reachable functions.
            Returns:
                `list` : list of functions
        """
        if self.graph_evaluated:
            return self.collected_function_set

        collected_functions = {v: [] for v in self.reversed_linklist}
        for values in self.generate_inputs(self.n, ranges = [0, 1]):
            evaluation = self._forward_graph(values)
            for vtx in self.reversed_linklist:
                collected_functions[vtx].append(evaluation[vtx])
        self.graph_evaluated = True
        self.collected_function_set = [func for vtx, func in collected_functions.items()]
        return self.collected_function_set


    def generate_inputs(self, length, ranges, _depth = 0):
        """
            Generator to produce increasing sequences
            Args:
                length : `int` : length of list
                ranges : `list` : possible values

            Yields:
                `list` : next list of `length` elements in order defined by `ranges`
        """
        assert len(ranges) > 0
        if _depth == length:
            yield []
            return
        for value in ranges:
            for called in self.generate_inputs(length, ranges, _depth + 1):
                yield [value,] + called


    def _add_edge(self, v_from, v_to):
        self.reversed_linklist[v_to][1].append(v_from)
        self.graph_evaluated = False


    def _add_vertex(self, label_ty, v_from = []):
        new_index = len(self.reversed_linklist)
        self.reversed_linklist[new_index] = [label_ty, []]
        for v in v_from:
            self._add_edge(v_from = v, v_to = new_index)
        self.graph_evaluated = False
        return new_index


    def _delete_vertex(self, vtx):
        del self.reversed_linklist[vtx]


    def _initiate_evaluation(self, values):
        inputs = self.inputs()
        assert len(inputs) == len(values), 'found {} inputs, not {}'.format(len(inputs), len(values))

        evaluation = {key: None for key in self.reversed_linklist}
        for input_index in inputs:
            evaluation[input_index] = values[input_index]
        return evaluation
        

    def _evaluate_vertex(self, v, evaluation):
        if evaluation[v] is not None:
            return evaluation[v]
        func_ty, edges = self.reversed_linklist[v]
        collected = []
        for to in edges:
            collected.append(self._evaluate_vertex(to, evaluation))
        evaluation[v] = self.executive[func_ty](collected)
        return evaluation[v]


    def _forward_graph(self, values):
        evaluation = self._initiate_evaluation(values)
        for key in self.reversed_linklist:
            evaluation[key] = self._evaluate_vertex(key, evaluation)
        return evaluation

        
def main():

    # initializing and adding 3 inputs
    g = PolarBear(n = 3)

    # 1. adding the -inputs
    basics = g.inputs()
    for i in range(g.n):
        basics.append(g.add_vertex(g.NOT, v_from = [basics[i],]))
    
    # 2.1. adding all 2-conjuctions of basics
    conjs2 = []
    for first in basics:
        for second in basics:
            neo = g.add_vertex(g.AND, v_from = [first, second])
            if neo is not None:
                conjs2.append(neo)

    # 2.2. adding all 3-conjuctions of basics
    conjs3 = []
    for first in basics:
        for second in conjs2:
            neo = g.add_vertex(g.AND, v_from = [first, second])
            if neo is not None:
                conjs3.append(neo)

    # 3. Adding all other functions by disjuction
    combined = basics + conjs2 + conjs3
    newest = []
    for first in combined:
        for second in combined + newest:
            neo = g.add_vertex(g.OR, v_from = [first, second])
            if neo is not None:
                newest.append(neo)

    return g

    
if __name__ == '__main__':
    print(main())
