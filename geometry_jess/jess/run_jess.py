
from geometry_jess.diagram.run_diagram import run_graph
from geometry_jess.jess.parse_facts import parse_save_facts
from geometry_jess.jess.execute_jess import execute_jess
from geometry_jess.parameters import Rulepath
from geometry_jess.utils.prep import make_dir
from geometry_jess.jess.parse_nlp import parse_nlp

__author__ = 'hyunyoung'



def test_pasing_facts():
    name = "math1"

    graph_parse = run_graph(name)
    graph_parse.core_parse.display_points()
    # graph_parse.line_graph
    parse_save_facts(name=name, graph_parse=graph_parse)
    engine_result = execute_jess(Rulepath, name)



def test_jess_engine():
    rulepath = "../../input/clp/rule.clp"
    factpath = "../../input/clp/fact.clp"
    engine_result = execute_jess(rulepath,factpath)
    for i in engine_result:
        print i

def test_nlp():
    inputs = "line 1,0 = 3\nline 3,1 =5"
    parse_nlp("math1",inputs)




if __name__ == "__main__":
    # test_pasing_facts()
    test_jess_engine()
    # test_nlp()

