from pprint import pprint


class PolarBear:
    INPUT, NOT, OR, AND = range(4) # label types
    verbose = [None, "NOT", "OR", "AND",] # verbose label types for printing
    executive = [lambda x: None, lambda x: int(not x[0]), lambda x: int(any(x)), lambda x: int(all(x)),]

    collected_function_set = []
    collected_function_vtx = []
    graph_evaluated = True
    
    def __init__(self, n):
        self.n = n
        self.reversed_linklist = {} # graph repr

        # adding inputs
        for i in range(self.n):
            self._add_vertex(self.INPUT)
        self.collect_functions()


    def __str__(self):
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


    def inputs(self, graph = None):
        if graph is None:
            graph = self.reversed_linklist
        return [key for key, (label_ty, _) in graph.items() if label_ty == self.INPUT]

    def _add_edge(self, v_from, v_to):
        self.reversed_linklist[v_to][1].append(v_from)
        self.graph_evaluated = False

    def add_vertex(self, label_ty, v_from):
        neo = self._add_vertex(label_ty, v_from)
        
        new_function = self.evaluate_vertex(neo)
    
        if new_function not in self.collected_function_set:
            self.collected_function_set.append(new_function)
        else:
            self.delete_vertex(neo)
            return None

        self.graph_evaluated = True
        return neo

    def _add_vertex(self, label_ty, v_from = []):
        new_index = len(self.reversed_linklist)
        self.reversed_linklist[new_index] = [label_ty, []]
        for v in v_from:
            self._add_edge(v_from = v, v_to = new_index)
        self.graph_evaluated = False
        return new_index


    def delete_vertex(self, vtx):
        del self.reversed_linklist[vtx]


    def evaluate_vertex(self, vtx):
        new_function = []
        # forward new vertex
        for values in self.generate_inputs(length = self.n, ranges = [0, 1]):
            val = self._evaluate_vertex(v = vtx, 
                graph = self.reversed_linklist, 
                evaluation = self.initiate_evaluation(graph = self.reversed_linklist, values = values))
            new_function.append(val)
        return new_function
       

    def generate_inputs(self, length, ranges, _depth = 0):
        assert len(ranges) > 0
        if _depth == length:
            yield []
            return
        for value in ranges:
            for called in self.generate_inputs(length, ranges, _depth + 1):
                yield [value,] + called
        

    def _evaluate_vertex(self, v, graph, evaluation):
        if evaluation[v] is not None:
            return evaluation[v]
        func_ty, edges = graph[v]
        collected = []
        for to in edges:
            collected.append(self._evaluate_vertex(to, graph, evaluation))
        #assert len(collected) == self.valences[func_ty], 'error in building, self.valences {} != {}'.format(len(collected), self.valences[func_ty])
        evaluation[v] = self.executive[func_ty](collected)
        return evaluation[v]


    def initiate_evaluation(self, graph, values):
        inputs = self.inputs(graph = graph)
        assert len(inputs) == len(values), 'found {} inputs, not {}'.format(len(inputs), len(values))

        evaluation = {key: None for key in graph}
        for input_index in inputs:
            evaluation[input_index] = values[input_index]
        return evaluation

    def _forward_graph(self, values, graph):
        evaluation = self.initiate_evaluation(graph, values)
        
        for key in graph:
            evaluation[key] = self._evaluate_vertex(key, graph, evaluation)
        return evaluation
        

    def collect_functions(self):
        if self.graph_evaluated:
            return self.collected_function_set

        collected_functions = {v: [] for v in self.reversed_linklist}
        for values in self.generate_inputs(self.n, ranges = [0, 1]):
            evaluation = self._forward_graph(values, graph = self.reversed_linklist)
            for vtx in self.reversed_linklist:
                collected_functions[vtx].append(evaluation[vtx])
        self.graph_evaluated = True
        self.collected_function_set = [func for vtx, func in collected_functions.items()]
        self.collected_function_vtx = [vtx  for vtx, func in collected_functions.items()]
        return self.collected_function_set
        
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

    '''
    # pre-3. Find all functions with only one True 
    bricks = [v for i, v in enumerate(g.collected_function_vtx) if g.collected_function_set[i].count(1) == 1]
    # 3. Adding all other functions by disjuction
    for f in sorted(g.generate_inputs(length = 8, ranges = [0, 1]), key = lambda item: item.count(1)):
        g.add_vertex(g.OR, v_from = [b for i, b in enumerate(bricks) if f[i] == 1])
    '''

    '''for f in sorted(g.generate_inputs(length = 8, ranges = [0, 1]), key = lambda item: item.count(1)):
                    for pos, value in enumerate(f):
                        if value == 0:
                            continue'''


    
    def report():
        print ('Lost:')
        diff = sorted([sq for sq in g.generate_inputs(length = 8, ranges = [0, 1]) if sq not in g.collect_functions()], key = lambda x: x.count(1))
        pprint (diff)
        print ('total {} functions lost'.format(len(diff)))    
    #report()
    
    return g

    
if __name__ == '__main__':
    g = main()
    print (g)
