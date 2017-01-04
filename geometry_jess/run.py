__author__ = 'hyunyoung'

from geometry_jess.diagram.run_diagram import run_graph
from geometry_jess.jess.parse_facts import parse_save_facts
from geometry_jess.jess.execute_jess import execute_jess
from geometry_jess.parameters import Rulepath
from geometry_jess.jess.parse_nlp import parse_nlp
from geometry_jess.jess.execute_jess import execute_query


def run_all(filepath):

    problem_name = filepath.split("/")[-1].split(".")[0]

    graph_parse = run_graph(filepath)
    # graph_parse.core_parse.display_points()
    
    graph_parse.core_parse.save_points_image(str(problem_name))


    parse_save_facts(name=problem_name, graph_parse=graph_parse)
    execute_jess(Rulepath, problem_name)



def run_diagram(filepath):

    problem_name = filepath.split("/")[-1].split(".")[0]

    graph_parse = run_graph(filepath)

    graph_parse.core_parse.save_points_image(str(problem_name))
    parse_save_facts(name=problem_name, graph_parse=graph_parse)

    return True

def run_jess(filepath,nlp_str):

    problem_name = filepath.split("/")[-1].split(".")[0]

    parse_nlp(problem_name, nlp_str)

    execute_jess(Rulepath, problem_name)

    return True

def run_query(filepath):
    problem_name = filepath.split("/")[-1].split(".")[0]

    result = execute_query(rulepath=Rulepath, filename=problem_name)
    print result

if __name__ == "__main__":
    path = "../output/math1/math1.png"
    # run_all("../input/math1.png")
    # run_diagram(path)

    nlp_str = "line 0,2 = 4\nline 1,2 = 10\nangle 1,2,0 = 90"

    run_jess(path, nlp_str)

    run_query(path)




