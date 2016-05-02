"""Cost analysis."""


__all__ = [
    'analyze_costs',
    'annotate_costs',
]


from incoq.mars.incast import L

from .costs import *
from .algebra import *


class BaseCostAnalyzer(L.NodeVisitor):
    
    """Base class for a visitor that traverses code and returns an
    asymptotic term.
    
    This class allows a subclass to specify three lists
    of node types:
    
        - nodes that have a constant cost
        
        - nodes that have a cost that is the sum of their children
        
        - and nodes that have an unknown cost
    
    Any node that is not handled in one of these lists must either have
    its own visit handler defined or else it raises an exception. The
    lists may include non-terminal node types (such as "operator") that
    summarize all the corresponding terminal types.
    
    Additionally, there are another three lists as above for names of
    functions that have the associated costs.
    """
    
    @property
    def const_nodes(self):
        raise NotImplementedError
    
    @property
    def sum_nodes(self):
        raise NotImplementedError
    
    @property
    def unknown_nodes(self):
        raise NotImplementedError
    
    @property
    def const_funcs(self):
        raise NotImplementedError
    
    @property
    def sum_funcs(self):
        raise NotImplementedError
    
    @property
    def unknown_funcs(self):
        raise NotImplementedError
    
    def process(self, tree):
        res = super().process(tree)
        res = normalize(res)
        return res
    
    def visit(self, tree):
        if isinstance(tree, L.AST):
            res = self.node_visit(tree)
        elif isinstance(tree, tuple):
            res = self.seq_visit(tree)
        else:
            # Primitive values are considered to have unit cost,
            # so they don't affect the costs of their parent nodes.
            res = Unit()
        
        return res
    
    def generic_visit(self, node):
        # Dispatch based on the lists.
        if isinstance(node, self.const_nodes):
            return Unit()
        
        elif isinstance(node, self.sum_nodes):
            costs = []
            for field in node._fields:
                value = getattr(node, field)
                cost = self.visit(value)
                costs.append(cost)
            return Sum(costs)
        
        elif isinstance(node, self.unknown_nodes):
            return Unknown()
        
        else:
            raise AssertionError('Unhandled node type: ' +
                                 type(node).__name__)
    
    def seq_visit(self, seq):
        # Sum up the costs of a sequence of nodes.
        costs = []
        for item in seq:
            cost = self.visit(item)
            costs.append(cost)
        return Sum(costs)
    
    def visit_Call(self, node):
        # Check if it matches one of the known function cases.
        if node.func in self.const_funcs:
            return Unit()
        
        elif node.func in self.sum_funcs:
            costs = []
            for arg in node.args:
                cost = self.visit(arg)
                costs.append(cost)
            return Sum(costs)
        
        elif node.func in self.unknown_funcs:
            return Unknown()
        
        else:
            raise NotImplementedError('Unknown function call')


class TrivialCostAnalyzer(BaseCostAnalyzer):
    
    """Determine a cost for a piece of code that does not contain loops
    or calls to unknown functions.
    """
    
    # The three lists are populated with names and programmatically
    # replaced with nodes below.
    
    const_nodes = [
        'Comment',
        'Fun', 'Class',
        'Import', 'ImportFrom',
        'Global',
        'Pass', 'Break', 'Continue',
        'ResetDemand',
        'RelUpdate', 'RelClear',
        'MapAssign', 'MapDelete', 'MapClear',
        'Num', 'Str', 'NameConstant', 'Name',
        'mask', 'alias',
        'boolop', 'operator', 'unaryop', 'cmpop',
        'setupop', 'setbulkop', 'dictbulkop', 'aggrop',
    ]
    
    sum_nodes = [
        'Module',
        'Raise', 'Try', 'Assert',
        'Return',
        'If',
        'Expr',
        'Assign', 'DecompAssign',
        'SetUpdate', 'SetClear',
        'DictAssign', 'DictDelete', 'DictClear',
        'AttrAssign', 'AttrDelete',
        # These operations might be more than constant-time to execute
        # if their operands are sets. We'll ignore this for cost
        # analysis since we don't generate this kind of code in our
        # maintenance functions.
        'UnaryOp', 'BoolOp', 'BinOp', 'Compare',
        'IfExp',
        'List', 'Set', 'Dict', 'Tuple',
        'Attribute', 'Subscript', 'DictLookup',
        'FirstThen',
        # Cost analysis assumes ImgLookup and other set indexing
        # operations are incrementalized.
        'ImgLookup', 'SetFromMap', 'Unwrap', 'Wrap',
        'IsSet', 'HasField', 'IsMap', 'HasArity',
        'excepthandler',
    ]
    
    unknown_nodes = [
        # Should not appear at cost analysis stage.
        'SetBulkUpdate', 'DictBulkUpdate',
        # Should not appear in our generated code.
        'GeneralCall',
        'ListComp', 'Comp', 'Aggr', 'AggrRestr',
        'clause', 'comprehension',
    ]
    
    const_nodes = tuple(getattr(L, n) for n in const_nodes)
    sum_nodes = tuple(getattr(L, n) for n in sum_nodes)
    unknown_nodes = tuple(getattr(L, n) for n in unknown_nodes)
    
    # Note that non-nullary functions cannot be constant-time since
    # we need to spend time to evaluate their arguments.
    const_funcs = []
    sum_funcs = []
    unknown_funcs = []
    
    def notimpl_helper(self, node):
        raise NotImplementedError('Cannot handle {} node'.format(
                                  node.__class__.__name__))
    
    visit_For = notimpl_helper
    visit_DecompFor = notimpl_helper
    visit_While = notimpl_helper
    
    def visit_Query(self, node):
        return self.visit(node.query)


class SizeAnalyzer(BaseCostAnalyzer):
    
    """Given an expression, determine its cardinality as a cost term."""
    
    const_nodes = [
        'UnaryOp', 'BoolOp', 'BinOp', 'Compare',
        'Num', 'Str', 'NameConstant',
        'List', 'Set', 'Dict', 'Tuple',
        'IsSet', 'HasField', 'IsMap', 'HasArity',
        # Assuming aggregate results can't be sets.
        # E.g., no min({a, b}, {a}).
        'Aggr', 'AggrRestr',
    ]
    
    sum_nodes = [
        'Unwrap', 'Wrap',
    ]
    
    unknown_nodes = [
        'GeneralCall',
        'Attribute', 'Subscript', 'DictLookup',
        'ListComp',
        'SetFromMap',
        'Comp',
    ]
    
    const_nodes = tuple(getattr(L, n) for n in const_nodes)
    sum_nodes = tuple(getattr(L, n) for n in sum_nodes)
    unknown_nodes = tuple(getattr(L, n) for n in unknown_nodes)
    
    def visit_IfExp(self, node):
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return Sum([body, orelse])
    
    def visit_Call(self, node):
        try:
            return super().visit_Call(node)
        except NotImplementedError:
            return Unknown()
    
    def visit_Name(self, node):
        return Name(node.id)
    
    def visit_FirstThen(self, node):
        return self.visit(node.then)
    
    def visit_ImgLookup(self, node):
        if isinstance(node.set, L.Name):
            return DefImgset(node.set.id, node.mask, node.bounds)
        else:
            return Unknown()
    
    def visit_Query(self, node):
        return self.visit(node.query)


class LoopCostAnalyzer(TrivialCostAnalyzer):
    
    """Extends the trivial cost analyzer to handle loops."""
    
    def visit_For(self, node):
        # For loops take the one-time cost of evaluating the iter,
        # plus the size of the iter times the cost of running the
        # body.
        iter_size = SizeAnalyzer.run(node.iter)
        iter_cost = self.visit(node.iter)
        body_cost = self.visit(node.body)
        return Sum([iter_cost, Product([iter_size, body_cost])])
    
    # DecompFor is the same since we don't care about target/vars.
    visit_DecompFor = visit_For
    
    def visit_While(self, node):
        # Return the body cost times an unknown number of iterations.
        body_cost = self.visit(node.body)
        return Product([Unknown(), body_cost])


class CallCostAnalyzer(LoopCostAnalyzer):
    
    """Extends the loop cost analyzer to handle function calls."""
    
    def __init__(self, func_params, func_costs):
        super().__init__()
        self.func_params = func_params
        """Map from function name to list of formal parameter names."""
        self.func_costs = func_costs
        """Map from function name to known cost for it, in terms of its
        formal parameters.
        """
    
    def visit_Call(self, node):
        arg_cost = Sum([self.visit(arg) for arg in node.args])
        
        # Check for one of the special cases.
        try:
            call_cost = super().visit_Call(node)
        except NotImplementedError:
            call_cost = None
        
        if call_cost is None:
            # Try retrieving and instantiating the cost from the map.
            name = node.func
            if name in self.func_costs:
                cost = self.func_costs[name]
                params = self.func_params[name]
                assert len(params) == len(node.args)
                
                # Create a substitution from formal parameter name to
                # argument variable name, or None if the argument is not
                # a variable.
                arg_names = [arg.id if isinstance(arg, L.Name) else None
                             for arg in node.args]
                subst = dict(zip(params, arg_names))
                # Instantiate.
                call_cost = ImgkeySubstitutor.run(cost, subst)
            else:
                call_cost = Unknown()
        
        return Sum([arg_cost, call_cost])


def analyze_costs(tree, funcs):
    """Analyze the costs of the functions whose names are given in
    funcs, and return a map from function name to cost. The functions
    must be defined in the program, top-level, and non-recursive.
    """
    graph = L.analyze_functions(tree, funcs)
    
    # Analyze the functions in topological order, constructing
    # func_costs as we go.
    func_costs = {}
    func_params = graph.param_map
    for f in graph.order:
        body = graph.body_map[f]
        cost = CallCostAnalyzer.run(body, func_params, func_costs)
        
        # Eliminate image key terms that aren't formal parameters.
        key_filter = lambda p: p if p in func_params[f] else None
        cost = ImgkeySubstitutor.run(cost, key_filter)
        
        func_costs[f] = cost
    
    return func_costs


def annotate_costs(tree, symtab):
    """Analyze and annotate the costs of maintenance functions."""
    func_costs = analyze_costs(tree, symtab.maint_funcs)
    
    class Trans(L.NodeTransformer):
        def visit_Fun(self, node):
            node = self.generic_visit(node)
            
            if node.name in func_costs:
                cost = 'Cost: O({})'.format(func_costs[node.name])
                comment = (L.Comment(cost),)
                node = node._replace(body=comment + node.body)
            return node
    tree = Trans.run(tree)
    
    symtab.func_costs = func_costs
    
    return tree