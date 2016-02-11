import time

def read_file(file):
    with open(file) as f:
        return f.readlines()

def file_into_array(file):
    return [ read_dsl_line(l) for l in read_file(file) if is_dsl_line_valid(l)]

def is_dsl_line_valid(line):
    return (line.rstrip() == "" or line.startswith("#")) == False

def read_dsl_line(line):
    return line.rstrip('\n').split('|')

def map_dsl_array(dslarray):
    vars = getVariables(dslarray)
    return [get_tables(dslarray, vars), vars]

def puts(l):
    print(l)
    return l

def puts_array(a):
    [puts(x) for x in a]

def get_tables(dslarray, vars, tables=[]):
    return (getCommands(dslarray, vars, 0, [], []))

def is_Start_CCC(element):
    return element.startswith(" ") == False

def getCommands(arr, vars, i ,lists, list):
    return i == len(arr)-1 and lists+[list] or appendCommand(arr, vars, i ,lists, list)

def appendCommand(arr, vars, i ,lists, list):
    return isVariable(arr[i][0]) and getCommands(arr, vars, i+1, lists, list) or collectCommand(arr, vars, i ,lists, list)

def setVariable(value, vars):
    return (value[0].strip() in vars[0]) and [vars[0].get(value[0].strip())]+value[1:] or value;

def collectCommand(arr, vars, i ,lists, list):
    return is_Start_CCC(arr[i][0]) and getCommands(arr, vars, i+1, lists+[list],  [setVariable(arr[i], vars)]) or getCommands(arr, vars, i+1, lists, list+[setVariable(arr[i], vars)]) 

def getVariables(dslarray, vars={}):
    return [add_variable(e[0], vars) for e in dslarray ]

def add_variable(member, bucket):
    return isVariable(member) and add_to_buckets(member, bucket) or bucket

def isVariable(member):
    return member.startswith('$') 

def add_to_hash(hash, arr):
    hash[arr[0].strip()] = arr[1].strip()
    return hash

def add_to_buckets(member, bucket):
    return add_to_hash(bucket, member.split("="))

def makeQueries(file, tpf=""):
    return makeQueriesSubRoutine(map_dsl_array(file_into_array(file)), tpf)

def makeQueriesSubRoutine(arr, tpf):
    return [makeQuery(x, arr[1], tpf) for x in arr[0] if len(x) > 0]

def makeQuery(arrs, vars, tpf):
    return "create table %s (%s) %s" % (arrs[0][0]+tpf , combine(arrs[1:]), getTail(arrs[1:], vars) )

def getTail(list, vars):
    res = [getTailSubRoutine(x[0].strip().split("="), vars) for x in list if "=" in x[0]]
    return len(res) > 0 and res[0] or ""

def getTailSubRoutine(x, vars):
    return x[0].strip() == "$tail" and vars[0].get(x[1].strip()) or [""]  

def remove_g(arr):
    return [puts(x) for x in arr if ("$tail" in x) == False]

def combine(list):
    return reduce(concat, remove_g([ mold(fit_array(x)) for x in list ])).rstrip(",")

def fit_array(x):
    return [y.strip() for y in x]

def mold(x):
    return len(x) > 2  and "%s %s(%s)," % (x[0], x[1], x[2]) or x[0]

def concat(a, b):
    return a+" "+b

def main():
    print(makeQueries("sample.dsl"))

main()
