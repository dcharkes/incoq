"""Unit tests for pyconv.py."""


import unittest

import incoq.mars.incast.nodes as L
import incoq.mars.incast.pynodes as P
from incoq.mars.incast.pyconv import *
from incoq.mars.incast.pyconv import IncLangNodeImporter


class TemplaterCase(unittest.TestCase):
    
    def test_name(self):
        tree = Parser.pc('''
            a = a + b
            ''')
        tree = Templater.run(tree, subst={'a': L.Name('c', L.Read())})
        exp_tree = Parser.pc('''
            a = c + b
            ''')
        self.assertEqual(tree, exp_tree)
    
    def test_ident(self):
        tree = Parser.pc('''
            def a(a):
                for a, b in a:
                    a, b = a
                    a.add(a)
                    a.reladd(a)
                    a(a.a)
                    {a for a in a if a}
            ''')
        tree = Templater.run(tree, subst={'a': 'c'})
        exp_tree = Parser.pc('''
            def c(c):
                for c, b in c:
                    c, b = c
                    c.add(c)
                    c.reladd(c)
                    c(c.c)
                    {c for c in c if c}
            ''')
        self.assertEqual(tree, exp_tree)
    
    def test_code(self):
        tree = Parser.pc('''
            a
            C
            ''')
        tree = Templater.run(tree, subst={'<c>C':
                                          L.Expr(L.Name('b', L.Read()))})
        exp_tree = Parser.pc('''
            a
            b
            ''')
        self.assertEqual(tree, exp_tree)
        
        tree = Parser.pc('''
            a
            C
            ''')
        tree = Templater.run(tree, subst={'<c>C':
                                          (L.Expr(L.Name('b', L.Read())),
                                           L.Expr(L.Name('c', L.Read())))})
        exp_tree = Parser.pc('''
            a
            b
            c
            ''')
        self.assertEqual(tree, exp_tree)


class MacroExpanderCase(unittest.TestCase):
    
    def test_expansion(self):
        class A(MacroExpander):
            def handle_ms_add(self_, func, a, b):
                self.assertEqual(func, 'add')
                assert isinstance(a, L.Num)
                assert isinstance(b, L.Num)
                return L.Num(a.n + b.n)
        
        tree = P.Parser.ps('(2).add(3)')
        tree = IncLangNodeImporter.run(tree)
        tree = A.run(tree)
        exp_tree = L.Num(5)
        self.assertEqual(tree, exp_tree)


class ImportCase(unittest.TestCase):
    
    # This is just a simple test suite to verify that some
    # importing is actually being done. These tests do not
    # require that the IncAST parser works. More rigorous,
    # source-level tests are done below that test both
    # importing and round-tripping.
    
    def test_name_and_context(self):
        tree = import_incast(P.Name('a', P.Load()))
        exp_tree = L.Name('a', L.Read())
        self.assertEqual(tree, exp_tree)
        
        tree = import_incast(P.Name('a', P.Store()))
        exp_tree = L.Name('a', L.Write())
        self.assertEqual(tree, exp_tree)
        
        tree = import_incast(P.Name('a', P.Del()))
        exp_tree = L.Name('a', L.Write())
        self.assertEqual(tree, exp_tree)
    
    def test_trivial_nodes(self):
        tree = import_incast(P.Pass())
        exp_tree = L.Pass()
        self.assertEqual(tree, exp_tree)
        
        tree = import_incast(P.BinOp(P.Name('a', P.Load()),
                           P.Add(),
                           P.Name('b', P.Load())))
        exp_tree = L.BinOp(L.Name('a', L.Read()),
                           L.Add(),
                           L.Name('b', L.Read()))
        self.assertEqual(tree, exp_tree)


class ParserCase(unittest.TestCase):
    
    def test_parse(self):
        tree = Parser.pe('a')
        exp_tree = L.Name('a', L.Read())
        self.assertEqual(tree, exp_tree)
    
    def test_subst(self):
        tree = Parser.pe('a + b', subst={'a': L.Name('c', L.Read())})
        exp_tree = L.BinOp(L.Name('c', L.Read()),
                           L.Add(),
                           L.Name('b', L.Read()))
        self.assertEqual(tree, exp_tree)
    
    def test_unparse_basic(self):
        tree = Parser.pe('a + b')
        source = Parser.ts(tree)
        exp_source = '(a + b)'
        self.assertEqual(source, exp_source)
    
    def test_unparse_extras(self):
        # Also check cases of unparsing IncAST nodes that normally
        # don't appear (at least not by themselves) in complete
        # programs.
        ps = Parser.ps
        pe = Parser.pe
        ts = Parser.ts
        
        source = ts(L.GeneralCall(pe('a + b'), [pe('c')]))
        exp_source = '(a + b)(c)'
        self.assertEqual(source, exp_source)
        
        source = ts(L.Member(['x', 'y'], 'R'))
        exp_source = ' for (x, y) in R'
        self.assertEqual(source, exp_source)
        
        source = ts(L.Cond(pe('True')))
        exp_source = 'True'
        self.assertEqual(source, exp_source)
        
        source = ts(L.Read())
        exp_source = '<Unknown node "Load">'
        self.assertEqual(source, exp_source)
        
        source = ts(L.SetAdd())
        exp_source = "'<SetAdd>'"
        self.assertEqual(source, exp_source)


class ParseImportCase(unittest.TestCase):
    
    def test_functions(self):
        tree = Parser.p('''
            def f():
                pass
            ''')
        exp_tree = L.Module([L.fun('f', [], [L.Pass()])])
        self.assertEqual(tree, exp_tree)
        
        # Disallow inner functions.
        with self.assertRaises(TypeError):
            Parser.ps('''
                def f():
                    def g():
                        pass
                ''')
        
        # Modules must consist of functions.
        with self.assertRaises(TypeError):
            Parser.p('x = 1')
    
    def test_setupdates(self):
        tree = Parser.ps('S.add(x)')
        exp_tree = L.SetUpdate(L.Name('S', L.Read()),
                               L.SetAdd(),
                               L.Name('x', L.Read()))
        self.assertEqual(tree, exp_tree)
        
        tree = Parser.ps('S.reladd(x)')
        exp_tree = L.RelUpdate('S', L.SetAdd(), L.Name('x', L.Read()))
        self.assertEqual(tree, exp_tree)
        
        with self.assertRaises(TypeError):
            Parser.ps('(a + b).reladd(x)')
    
    def test_calls(self):
        tree = Parser.pe('f(a)')
        exp_tree = L.Call('f', [L.Name('a', L.Read())])
        self.assertEqual(tree, exp_tree)
        
        tree = Parser.pe('o.f(a)')
        exp_tree = L.GeneralCall(L.Attribute(L.Name('o', L.Read()),
                                             'f', L.Read()),
                                 [L.Name('a', L.Read())])
        self.assertEqual(tree, exp_tree)


class RoundTripCase(unittest.TestCase):
    
    def setUp(self):
        class trip(P.ExtractMixin):
            """Parse source as Python code, round-trip it through
            importing and exporting, then compare that it matches
            the tree parsed from exp_source.
            """
            @classmethod
            def action(cls, source, exp_source=None, *, mode=None):
                if exp_source is None:
                    exp_source = source
                tree = P.Parser.action(source, mode=mode)
                tree = import_incast(tree)
                tree = export_incast(tree)
                exp_tree = P.Parser.action(exp_source, mode=mode)
                self.assertEqual(tree, exp_tree)
        
        self.trip = trip
    
    def test_name_and_context(self):
        self.trip.pe('a')
    
    def test_trivial(self):
        self.trip.pe('a + b')
        self.trip.pe('a and b')
        self.trip.pe('o.f.g')
    
    def test_functions(self):
        self.trip.ps('''
            def f(a, b):
                print(a, b)
            ''')
    
    def test_loops(self):
        self.trip.ps('for x in S: continue')
        self.trip.ps('while True: break')
    
    def test_setupdates(self):
        self.trip.ps('S.add(x)')
        self.trip.ps('S.reladd(x)')
    
    def test_comp(self):
        self.trip.pe('{f(x) for (x, y) in S if y in T}')


if __name__ == '__main__':
    unittest.main()