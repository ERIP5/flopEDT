import numpy as np


def parse_iis(iis_filename):
    f = open(iis_filename, "r")
    data = f.read().split("Subject To\n")[1]
    constraints_declarations = data.split("Bounds")
    constraints_text = constraints_declarations[0]
    # declarations_text = constraints_declarations[1]

    constraints_text = constraints_text.split(":")
    id_constraints = [constraints_text[0]]
    for i in range(1, len(constraints_text) - 1):
        id_constraints.append(constraints_text[i].split("=")[1].split("\n")[1])
    id_constraints = list(map(lambda constraint: int(constraint[1:]), id_constraints))
    return id_constraints


def inc(dic, key):
    if key is not None:
        if key in dic.keys():
            dic[key] += 1
        else:
            dic[key] = 1


# To link the type of the constraint to the parameter occurence
def inc_with_type(dic, keys, c_type):
    if keys is not []:
        for key in keys:
            if key in dic.keys():
                dic[key][0] += 1
                if dic[key][1].count(c_type) == 0:
                    dic[key][1].append(c_type)
            else:
                dic[key] = [1, [str(c_type)]]


# Create result string to print
def make_occur_buf(dic):
    buf = ""
    types = ""
    for x in dic:
        param = dic.get(x)
        n = len(param[1])
        if n > 0:
            types = "("
            for t in range(n - 1):
                types += param[1][t] + ", "
            types += param[1][n - 1] + ")"
        buf += "[" + str(x) + " -> " + str(param[0]) + "] types : " + types + "\n"
    return buf


def handle_occur_type_with_priority(priority_types, occur_type, decreasing):
    nb_occ_init = []
    max_priority = max(occur_type.values()) + len(priority_types)
    min_priority = -len(priority_types) + 1
    for priority_type in priority_types:
        nb_occ_init.append(occur_type[priority_type])
        if priority_type in occur_type:
            occur_type[priority_type] = max_priority if decreasing else min_priority
        max_priority -= 1
        min_priority += 1
    occur_type = {k: v for k, v in sorted(occur_type.items(), key=lambda item: item[1], reverse=decreasing)}
    for i in range(len(priority_types)):
        occur_type[priority_types[i]] = nb_occ_init[i]
    return occur_type


class ConstraintManager:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def get_constraint_by_id(self, id_constraint):
        return self.constraints[id_constraint]

    def get_constraints_by_ids(self, id_constraints):
        return [self.constraints[id_constraint] for id_constraint in id_constraints]

    def get_occurs(self, id_constraints, decreasing=True):
        occur_type = {}
        occur_instructor = {}
        occur_slot = {}
        occur_course = {}
        occur_week = {}
        occur_room = {}
        occur_group = {}
        occur_days = {}
        occur_departments = {}

        # Initiate all occurences
        for i in id_constraints:
            c_type = self.get_constraint_by_id(i).constraint_type
            inc(occur_type, self.get_constraint_by_id(i).constraint_type)
            inc_with_type(occur_instructor, self.get_constraint_by_id(i).instructors, c_type)
            inc_with_type(occur_slot, self.get_constraint_by_id(i).slots, c_type)
            inc_with_type(occur_course, self.get_constraint_by_id(i).courses, c_type)
            inc_with_type(occur_week, self.get_constraint_by_id(i).weeks, c_type)
            inc_with_type(occur_room, self.get_constraint_by_id(i).rooms, c_type)
            inc_with_type(occur_group, self.get_constraint_by_id(i).groups, c_type)
            inc_with_type(occur_days, self.get_constraint_by_id(i).days, c_type)
            inc_with_type(occur_departments, self.get_constraint_by_id(i).departments, c_type)

        priority_types = ["Le cours doit être placé", "Pas_de_cours_le_jeudi_aprem"]
        occur_type = handle_occur_type_with_priority(priority_types, occur_type, decreasing)

        occur_instructor = {k: v for k, v in
                            sorted(occur_instructor.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_slot = {k: v for k, v in sorted(occur_slot.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_course = {k: v for k, v in sorted(occur_course.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_week = {k: v for k, v in sorted(occur_week.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_room = {k: v for k, v in sorted(occur_room.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_group = {k: v for k, v in sorted(occur_group.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_days = {k: v for k, v in sorted(occur_days.items(), key=lambda item: item[1][0], reverse=decreasing)}
        occur_departments = \
            {k: v for k, v in sorted(occur_departments.items(), key=lambda item: item[1][0], reverse=decreasing)}

        return occur_type, occur_instructor, occur_slot, occur_course, occur_week, occur_room, occur_group, \
            occur_days, occur_departments

    def show_reduces_result_brut(self, id_constraints, week, decreasing=True):
        occur_type, occur_instructor, occur_slot, occur_course, occur_week, occur_room, occur_group, occur_days,\
            occur_department = self.get_occurs(id_constraints, decreasing)

        order = list(occur_type.keys())
        constraints = self.get_constraints_by_ids(id_constraints)
        constraints = sorted(constraints, key=lambda x: order.index(x.constraint_type))
        output = ""
        for constraint in constraints:
            output += str(constraint) + "\n"
        filename = "logs/intelligible_constraints%s.txt" % week
        print("writting %s ..." % filename)
        with open(filename, "w+") as file:
            file.write(output)
        # print(output)

    def show_reduces_result(self, id_constraints, week):
        occur_type, occur_instructor, occur_slot, occur_course, occur_week, occur_room, occur_group, occur_days,\
            occur_department = self.get_occurs(id_constraints)

        buf_type = ""
        for x in occur_type:
            buf_type += "[" + str(x) + " -> " + str(occur_type.get(x)) + "] \n"

        buf_instructor = make_occur_buf(occur_instructor)
        buf_slot = make_occur_buf(occur_slot)
        buf_course = make_occur_buf(occur_course)
        buf_week = make_occur_buf(occur_week)
        buf_room = make_occur_buf(occur_room)
        buf_group = make_occur_buf(occur_group)
        buf_days = make_occur_buf(occur_days)
        buf_department = make_occur_buf(occur_department)

        output = "Sommaire des contraintes : \n"
        if buf_type != "":
            output += "\nParametre Type :\n" + buf_type
        if buf_instructor != "":
            output += "\nParametre Instructor :\n" + buf_instructor
        if buf_course != "":
            output += "\nParametre Course : \n" + buf_course
        if buf_week != "":
            output += "\nParametre Week : \n" + buf_week
        if buf_room != "":
            output += "\nParametre Room : \n" + buf_room
        if buf_group != "":
            output += "\nParametre Group : \n" + buf_group
        if buf_days != "":
            output += "\nParametre Days : \n" + buf_days
        if buf_slot != "":
            output += "\nParametre Slot :\n" + buf_slot
        if buf_department != "":
            output += "\nParametre Department :\n" + buf_department

        filename = "logs/intelligible_constraints_factorised%s.txt" % week
        print("writting %s ..." % filename)
        with open(filename, "w+") as file:
            file.write(output)
        # print(output)

    def handle_reduced_result(self, ilp_file_name, week):
        id_constraints = parse_iis(ilp_file_name)
        self.show_reduces_result_brut(id_constraints, week, decreasing=True)
        self.show_reduces_result(id_constraints, week)
