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

    return


def worker_empty(r, argv, ret):
    return


def worker_get_sid_by_pgid(r, argv, ret):
    if r.g == argv[0]:
        ret = r.s


def reconstruct_finalizer(r, argv, ret):
    ret = argv+"]"
    return


#
# worker_reconstruct: reconstruct the string from sub-tree representation
def worker_reconstruct(r, argv, ret):
    ret = argv + "|" + str(r.p)+" " + str(r.s) + " " + str(r.g) + ";["

# process_graph_routines


def dfs(r, func, func_finalizer, argv, ret=0):
    # type: (representor, worker_func, finalizer, args, retvals) -> void
    if not r:
        return

    func(r, argv, ret)
    func_finalizer(r, argv, ret)
    for node in r.children:
        dfs(node, func, func_finalizer, argv, ret)
    return


def construct(r):
    res=""
    dfs(r, worker_reconstruct, worker_empty, res, res)
    return res
