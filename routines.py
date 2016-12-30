# workers
def worker_check_field(r, argv, ret=0):
    if (argv[0] == 'p'):
        if (r.p == argv[1]):
            ret = 1

    if (argv[0] == 'g'):
        if (r.g == argv[1]):
            ret = 1

    if (argv[0] == 's'):
        if (r.s == argv[1]):
            ret = 1

    return ret


def empty_finalizer(r, argv, ret):
    return ret


def reconstruct_finalizer(r, argv, ret):
    ret = argv+"]"


#
# worker_reconstruct: reconstruct the string from sub-tree representation
def worker_reconstruct(r, argv, ret):
    ret = argv + "|" + str(r.p)+" " + str(r.s) + " " + str(r.g) + ";["

# process_graph_routines

def bfs(r, func, func_finalizer, argv, ret=0):
    # type: (representor, worker_func, finalizer, args, vals) -> void
    if not r:
        return

    func(r, argv, ret)
    func_finalizer(r, argv, ret)
    for node in r.children:
        bfs(node, func, func_finalizer, argv, ret)
    return
