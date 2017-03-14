import re
import rules
from anytree import Node, RenderTree, PreOrderIter, PostOrderIter
import cPickle as pickle


# returns 1 if argtype is int 
def is_link(data):
    if isinstance(data[0], int):
        return 1

    return 0

def is_list(data):
    if isinstance(data[0], list):
        return 1

    return 0


def is_basestring(data):
    if isinstance(data, basestring):
        return 1

    return 0


# crafted pointer-imitation instances
class ptr(object):
    def __init__(self, value): self.value = value
'''
#  example:
y = ptr(obj1)
x = y
x.value = obj2
print y.value
______________
prints obj2
'''

# serialization I/O


def pkl_write(obj, f_name):
    out = open(f_name, 'wb')
    pickle.dump(obj, out, 2)
    out.close()


def pkl_read(obj, f_name):
    inp = open(f_name, 'rb')
    obj = pickle.load(inp)
    inp.close()
    return obj

# log input/output


def log_output(log, f_name, is_full=1, is_debug=1, opt=0, f=None):
    if is_full:
        if not f_name:
            for pre, fill, node in RenderTree(log):
                if is_debug:
                    print("%s%s %d" % (pre, node.name, id(node)))
                else:
                    print("%s%s" % (pre, node.name))

        else:
            if not opt:
                f = open(f_name, 'w')
            for pre, fill, node in RenderTree(log):
                print("%s%s" % (pre, node.name))
                zz = "%s%s" % (pre, node.name)
                f.write(zz.encode("UTF-8"))
            if not opt:
                f.close()
    return


def visualize(src, output=None, is_full=1, is_debug=0):
    f = open(src, 'r')
    if output:
        fout = open(output, 'w')
    r = Node("|0 0 0;", 0, 0, 0)  # in my suggestion, there is a zero process "SCHED"
    reconstruct(f.readline(), r)
    log_output(r, output, is_full, is_debug,1, fout)
    if output:
        fout.close()
    f.close()
    return

# workers


def worker_check_field(r, argv, ret):

    if argv[0] == 'p':
        if r.p == argv[1]:
            if not ret:
                ret = list()
            ret.append(None)
            ret[-1] = ptr(r)  # insert a copy of r

    if argv[0] == 'g':
        if r.g == argv[1]:
            if not ret:
                ret = list()
            ret.append(None)
            ret[-1] = r   # insert a copy of r

    if argv[0] == 's':
        if r.s == argv[1]:
            if not ret:
                ret = list()
            ret.append(None)
            ret[-1] = r   # insert a copy of r

    return


# collects  nodes into the new list
def worker_list_nodes(r, argv, ret):
    ret.append(ptr(r))
    return


def worker_print(r, argv, ret=0):
    if not r:
        return
    print r.p, r.g, r.s
    return


def worker_empty(r, argv, ret):
    return


def worker_get_sid_by_pgid(r, argv, ret):
    if r.g == argv[0]:
        ret = r.s


# worker_reconstruct: reconstruct the string from sub-tree representation
def worker_reconstruct(r, argv, ret):
    ret[0] = argv[0] + "|" + str(r.p) + " " + str(r.g) + " " + str(r.s) + ";["
    return


def worker_string_sync(r, argv, ret):
    r.name = "|" + str(r.p) + " " + str(r.g) + " " + str(r.s) + ";"


def reconstruct_finalizer(r, argv, ret):
    ret[0] = argv[0] + "]"
    return

# adds children to the r steps by step


def fill_lvl(r, lst):
    r_lvl = r
    for num, line in enumerate(lst):

        if line == '':
            continue

        tmp_s = re.findall('\d+', line)
        current = Node("|" + str(r.p) + " " + str(r.g) + " " + str(r.s) + ";", tmp_s[0], tmp_s[1], tmp_s[2], parent=r_lvl)

        if line[-1] == '[':
            r_lvl = current
        elif line[-1] == line[-2] == ']':
            r_lvl = r_lvl.parent

    return r


# extensive string split by cStringIO routines
def split_extensive(ss, r):
    # type: (string, representor) -> representor
    fill_lvl(r, ss.split('|'))
    return r


def reconstruct(ss, r):
    return split_extensive(ss, r)


# process_graph_routines


def dfs(r, func, func_finalizer, argv, ret):
    # type: (representor, worker_func, finalizer, args, retvals) -> void
    if not r:
        return

    func(r, argv, ret)

    for node in r.children:
        dfs(node, func, func_finalizer, argv, ret)

    func_finalizer(r, argv, ret)
    return


def construct(r):
    res = [""]
    dfs(r, worker_reconstruct, reconstruct_finalizer, res, res)
    return res

