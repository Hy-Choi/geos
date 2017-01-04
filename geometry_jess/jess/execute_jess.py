from subprocess import *
from geometry_jess.jess.parse_facts import save_facts


__author__ = "hyunyoung"


def execute_jess(rulepath, filename):
    factpath = "../output/"+filename+"/facts.txt"

    args = ['../geometry_jess_engine.jar',rulepath,factpath] # Any number of args to be passed to the jar file

    result = execute_jar(*args)
    save_facts(filename+"/new_", result)

    return result

def execute_jar(*args):
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    result = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    # print "\n\n"
    print ret
    for fact in ret[1:-1]:
        print fact
        result.append("("+fact.split(":")[2])
    return result

def execute_query(rulepath,filename):
    factpath = "../output/"+filename+"/new_facts.txt"
    querypath = "../output/" + filename+"/query.txt"

    args = ['../query_engine.jar', rulepath, factpath, querypath]

    result = execute_query_jar(*args)
    return result

def execute_query_from_string(rulepath, filename, string):
    # factpath = "../output/"+filename+"/new_facts.txt"
    # factpath = os.path.join(BASE_DIR, "diagram/static/diagram/"+filename+"/new_facts.txt")
    t1 = '/Users/hy/Documents/lab/program/JESS/geoTest/111.txt'
    t2 = '/Users/hy/Documents/lab/program/JESS/geoTest/222.txt'
    queryr = "(bind ?result (run-query* q-line 0 1)) (while (?result next)(printout t (?result getDouble v) crlf))"
    print queryr

    args = ['/Users/hy/Documents/lab/program/JESS/geoTest/query_engine_string.jar', t1, t2, queryr]

    # args = [os.path.join(BASE_DIR, 'query_engine_string.jar'), rulepath, factpath, string] # Any number of args to be passed to the jar file

    result = execute_query_jar(*args)
    print result
    return result


def execute_query_jar(*args):
    process = Popen(['java', '-jar']+list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    result = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')

    return ret

if __name__ == "__main__":
    execute_query_from_string("!","2","3")