
from geometry_jess.diagram.get_instances import get_all_instances
from geometry_jess.diagram.parse_confident_formulas import parse_confident_formulas
from geometry_jess.utils.prep import make_dir
import json


__author__ = "hyunyoung"


def save_facts(name, parse_facts, cord_json={}):

    f = open('../output/' + name + 'facts.txt','w')
    f.write("(deffacts problem-fact\n")
    for fact in parse_facts:
        f.write(fact + "\n")
    f.write(")")
    f.close()


    if cord_json:
        with open('../output/' + name + 'cord_json.json','w') as outfile:
            json.dump(cord_json, outfile)

    return True


def parsing_facts(graph_parse):
    fact = []
    count = 0

    # print("Confident information in the diagram:")
    # for variable_node in parse_confident_formulas(graph_parse):
    #     print variable_node
    points = get_all_instances(graph_parse, 'point')
    lines = get_all_instances(graph_parse, 'line')
    polygons = get_all_instances(graph_parse,'polygon')
    angles = get_all_instances(graph_parse, 'angle')
    circles =get_all_instances(graph_parse, 'circle')

    for key, line in lines.iteritems():
        count += 1
        # (cord1_x 1.24) (cord1_y 1.23) (cord2_x 2.43) (cord2_y 29.32)
        tmp = "(line (id l" + str(count) + ") (point1 " + str(key[0]) + ") (point2 " + str(key[1])+"))"
        # print tmp
        fact.append(tmp)

    count = 0
    # print angles
    for key, angle in angles.iteritems():
        count += 1
        tmp = "(angle (id a"+str(count) + ") (point1 " + str(key[0]) + ") (point2 " + str(key[1]) + ") (point3 " + str(key[2])+ "))"
        # print tmp
        fact.append(tmp)

    count = 0
    # print polygons
    for key, polygon in polygons.iteritems():
        count += 1
        tmp = "("+ str(polygon.signature).lower() + " (id p" + str(count) + ") "
        for i, p_children in zip(xrange(len(polygon.children)), polygon.children):
            tmp += "(point" + str(i+1) + " " + str(key[i]) + ") "
        tmp += ")"
        fact.append(tmp)

    count =0
    for key,circle in circles.iteritems():
        print key, circle
        print circle.center.x
        count += 1
        tmp = "(circle (id c" + str(key[0])+str(key[1]) + ") (center " + str(key[0]) + "))"
        # print tmp
        fact.append(tmp)

    count =0
    for variable_node in parse_confident_formulas(graph_parse):
        print variable_node

    # PointLiesOnLine($point_11:point,Line($point_1:point,$point_2:point))

    count =0
    for variable_node in parse_confident_formulas(graph_parse):
        print variable_node
        if(str(variable_node.signature) == 'PointLiesOnCircle'):
            count+=1
            tmp = "(point-lies-on-circle (id ploc" + str(count) + ") (point " + (str(variable_node.children[1])).split(":")[0].split("_")[1] + ") (circle-id c"+ (str(variable_node.children[2].children[0])).split(":")[0].split("_")[1] + (str(variable_node.children[2].children[1])).split(":")[0].split("_")[1] + "))"
            # print tmp
            fact.append(tmp)
        if(str(variable_node.signature) == 'PointLiesOnLine'):
            count+=1
            tmp = "(point-lies-on-line (id plol" + str(count) + ") (point " + (str(variable_node.children[0])).split(":")[0].split("_")[1] + ") (start-point "+ (str(variable_node.children[1].children[0])).split(":")[0].split("_")[1] +\
                  ") (end-point "+ (str(variable_node.children[1].children[1])).split(":")[0].split("_")[1] + "))"
            # print tmp
            fact.append(tmp)


    for i in fact:
        print i

    return fact    


def parse_facts2(graph_parse):

    fact = []
    count = 0
    cord_json = {}

    # print("Confident information in the diagram:")
    # for variable_node in parse_confident_formulas(graph_parse):
    #     print variable_node
    points = get_all_instances(graph_parse, 'point')
    lines = get_all_instances(graph_parse, 'line')
    polygons = get_all_instances(graph_parse,'polygon')
    angles = get_all_instances(graph_parse, 'angle')
    circles =get_all_instances(graph_parse, 'circle')


    line_list = []
    point_list = []

    for key, line in lines.iteritems():
        count += 1

        # (cord1_x 1.24) (cord1_y 1.23) (cord2_x 2.43) (cord2_y 29.32)
        tmp = "(line (id l" + str(count) + ") (point1 " + str(key[0]) + ") (point2 " + str(key[1]) + "))"
        # print tmp
        fact.append(tmp)


        # for Line json
        cord_line = { 'id': str(key[0])+'_'+str(key[1]), 'x1': float(round(line.a.x,2)), 'y1': float(round(line.a.y,2)),
                 'x2': float(round(line.b.x,2)), 'y2': float(round(line.b.y,2))}

        line_list.append(cord_line)


        # for Point json
        cord_point1 = {'id': str(key[0]), "x": float(round(line.a.x, 2)), "y": float(round(line.a.y, 2))}
        cord_point2 = {'id': str(key[1]), "x": float(round(line.b.x, 2)), "y": float(round(line.b.y, 2))}


        point_list.append(cord_point1)
        point_list.append(cord_point2)

        point_list = [dict(t) for t in set([tuple(d.items()) for d in point_list])]


    cord_json['Line'] = line_list
    cord_json['Point'] = point_list



    count = 0
    # print angles
    for key, angle in angles.iteritems():
        count += 1
        tmp = "(angle (id a"+str(count) + ") (point1 " + str(key[0]) + ") (point2 " + str(key[1]) + ") (point3 " + str(key[2]) + "))"
        # print tmp
        fact.append(tmp)




    count = 0
    # print polygons
    for key, polygon in polygons.iteritems():
        count += 1
        tmp = "("+ str(polygon.signature).lower() + " (id p" + str(count) + ") "
        for i, p_children in zip(xrange(len(polygon.children)), polygon.children):
            tmp += "(point" + str(i+1) + " " + str(key[i]) + ") "
        tmp += ")"
        fact.append(tmp)



    circle_list = []
    count =0
    for key,circle in circles.iteritems():
        print key, circle
        print circle.center.x
        count += 1
        tmp = "(circle (id c" + str(key[0])+str(key[1]) + ") (point " + str(key[0]) + "))"
        # print tmp
        fact.append(tmp)

        cord = {'id': str(key[0]), 'cx': float(round(circle.center.x,2)), 'cy': float(round(circle.center.y,2)),
                'r': float(round(circle.radius, 2))}

        circle_list.append(cord)

    cord_json['Circle'] = circle_list

    # print(json.dumps(cord_json))



    count =0
    for variable_node in parse_confident_formulas(graph_parse):
        print variable_node

    # PointLiesOnLine($point_11:point,Line($point_1:point,$point_2:point))

    count =0
    for variable_node in parse_confident_formulas(graph_parse):
        print variable_node
        if(str(variable_node.signature) == 'PointLiesOnCircle'):
            count+=1
            tmp = "(point-lies-on-circle (id ploc" + str(count) + ") (point " + \
                  (str(variable_node.children[0])).split(":")[0].split("_")[1] + ") (circle "+ \
                  (str(variable_node.children[1].children[1])).split(":")[0].split("_")[2] + "))"
            # print tmp
            fact.append(tmp)
        if(str(variable_node.signature) == 'PointLiesOnLine'):
            count+=1
            tmp = "(point-lies-on-line (id plol" + str(count) + ") (point " + \
                  (str(variable_node.children[0])).split(":")[0].split("_")[1] + ") (start-point "+ \
                  (str(variable_node.children[1].children[0])).split(":")[0].split("_")[1] +\
                  ") (end-point "+ (str(variable_node.children[1].children[1])).split(":")[0].split("_")[1] + "))"
            # print tmp
            fact.append(tmp)


    for i in fact:
        print i



    return {'fact': fact, 'cord_json': cord_json}



def parse_save_facts(graph_parse, name):
    parse_facts = parsing_facts(graph_parse)
    boolean_save = save_facts(name+"/", parse_facts['fact'], parse_facts['cord_json'])
    
    return True



