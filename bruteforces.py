import routines
import rules
import sys
import copy

g_num = 1


# in general, transform functions runs dfs, but in is unefficient method


# list transformation for
def fork_lst_transform(argv):
    new_lst=list(argv[1])
    print "pid=" +str(argv[0] + 1)
    new_lst.insert(argv[0] + 1, argv[1][argv[0]].children[-1])
    return new_lst


# resync the subtree: argv[1] is node, argv[0] is position
# def resync_subtree(argv):

# make rule steps for each of node then go further
# lst is temporary list with no strict order
# until MAX_PROC_NUM list len is exceeted, then exit.
# rule is transformation rule with correct argv args (no check!)
# log_tree is n-are tree for string notation logging (see
#  'routines.construct' function) .
# r and log_tree are modified "anytree" structures

depth = 0


def perm(r, rls, argv, is_log=0, log_tree=None, max_proc_num=rules.PROC_LIMIT, fd=None):
    lst = [node for node in routines.PreOrderIter(r)]
    if len(lst) >= max_proc_num:
        return

    for num in xrange(0, len(lst)):  # cycle iterates on changable list but r_branch is saved copy of this instance
        for rn, rule in enumerate(rls):
            lst = [node for node in routines.PreOrderIter(r)]
            tmp_r = copy.deepcopy(r)
            argv_ret = getattr(rules, rule)(lst[num], *argv[rn])  #  fork/anything else

            if is_log and fd:
                log_tree = routines.Node([rule, '('+','.join([str(x) for x in argv[rn]])+')', routines.construct(r)], parent=log_tree)
                routines.log_output(log_tree, fd)

            routines.log_output(r, "", 1, 0)
            perm(r, rls, [[argv_ret]], is_log, log_tree, max_proc_num, fd)

            r = tmp_r

    return


def brute_fork(r=routines.Node("|1 1 1;", 1, 1, 1), ns_last_pid=1, is_log=1, log_tree=routines.Node(["", "", "|1 1 1 ;[]"]), proc_limit=rules.PROC_LIMIT):
    lst = []

    routines.dfs(r, routines.worker_list_nodes, routines.worker_empty, [], lst) # lst - list of crafted pointers ptr
    sys.setrecursionlimit(1000000)
    perm(r, ["fork"], [[ns_last_pid]], is_log, log_tree, proc_limit, "lg1.txt")

#    routines.log_output(log_tree, "log_tree.txt")

#    routines.pkl_write(log_tree,"log_tree.pkl")
#    routines.pkl_write(log_tree, "process_tree.repr")
    return r


def gen_diff_len_fork(max, log_tree_fname):
    for i in xrange(2, max):
        N=routines.Node("|1 1 1;",1,1,1)

        brute_fork(N, 2, 1, log_tree, i)
        routines.log_output(log_tree, log_tree_fname, 1, 0)




N=routines.Node("|1 1 1;", 1, 1, 1)
#R=routines.Node("|2 1 1;", 2, 1, 1, parent=N)

brute_fork(N, 2)
