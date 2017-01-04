__author__ = "hyunyoung"

def parse_nlp_modify(input_str):

    primitive = input_str.split(" ")[0]
    points = input_str.split(" ")[1].split(",")
    value = input_str.split("=")[1].strip()

    rulename = "(defrule modify-"+primitive
    for point in points:
        rulename += point
    condition = "\n ?"+primitive+" <- " +"("+primitive
    for idx,point in zip(range(1,len(points)+1),points):
        condition += "(point" + str(idx) + " " + point + ") "
    if primitive == "angle":
        conclusion = ")\n => \n (modify ?" + primitive + " (degree " + value + "))\n)"
    else:
        conclusion = ")\n => \n (modify ?" + primitive + " (value " + value + "))\n)"

    return rulename+condition+conclusion

def save_nlp_rule(name, input_str):
    f = open('../output/' + name + '/facts.txt','a')

    for fact in input_str:
        f.write(fact + "\n")
    f.close()
    return True

def parse_nlp(name, nlp_texts):
    print nlp_texts

    rule_list = [parse_nlp_modify(nlp_text) for nlp_text in nlp_texts.split("\n")]
    print rule_list
    save_nlp_rule(name, rule_list)
    return True