import routines
import rules


# in general, transform functions runs dfs, but in is unefficient method


# list transformation for
def fork_lst_transform(argv):
    new_lst=list(argv[1])
    new_lst.insert(argv[0] + 1, argv[1][argv[0]].children[-1])
    return new_lst


# make rule steps for each of node then go further
# lst is temporary list with no strict order
# until MAX_PROC_NUM list len is exceeted, then exit.
# rule is transformation rule with correct argv args (no check!)
# log_tree is n-are tree for string notation logging (see
#  'routines.construct' function) .

def perm(r, lst, rule, argv, func_lst_transform=None, is_log=0, log_tree=None, max_proc_num=rules.PROC_LIMIT):
    if len(lst) >= max_proc_num:
        return

    for num, node in enumerate(lst):
        argv_ret = node.rule(argv)
        if is_log:
            log_tree = routines.Node([rule.__name__, '('+','.join([str(x) for x in lst])+')', routines.construct(r)], parent=log_tree)

        new_lst = func_lst_transform([num, lst])
        perm(r, new_lst, rule, argv_ret, func_lst_transform, is_log, log_tree, max_proc_num)

    return


def brute_fork(r=rules.representor(None, 1, 1, 1, []), ns_last_pid=1, is_log=1, log_tree=routines.Node(["", "", "|1 1 1 ;[]"])):
    lst = []
    routines.dfs(r, routines.worker_list_nodes(), routines.worker_empty, [], lst)
    perm(r, lst, rules.fork, ns_last_pid, fork_lst_transform, 1, log_tree)
    return r
