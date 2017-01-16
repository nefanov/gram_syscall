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


def perm(r, rls, argv, is_log=0, log_tree=None, max_proc_num=rules.PROC_LIMIT):
    global depth
    depth += 1
    print "Recursion level: " + str(depth)
    lst = [node for node in routines.PreOrderIter(r)]
    if len(lst) >= max_proc_num:
        print "------------\nPREV RES:"

        routines.log_output(r, "")
        print "-------------return--------------"
        depth -= 1
        return

    for num in xrange(0, len(lst)):  # cycle iterates on changable list but r_branch is saved copy of this instance
        for rn, rule in enumerate(rls):
            lst = [node for node in routines.PreOrderIter(r)]
            print "\nLVL " + str(depth)
            print "DO:"
            routines.log_output(r, "")

            tmp_r = copy.deepcopy(r)
            argv_ret = getattr(rules, rule)(lst[num], *argv[rn])  #  fork/anything else
            print "list dump:"

            print '\n'.join(str(id(p)) for p in lst)
            print "Current node addr: " + str(id(lst[num]))
            print "\nPOSLE:"
#            if is_log:
#                log_tree = routines.Node([rule, '('+','.join([str(x) for x in argv[rn]])+')', routines.construct(r)], parent=log_tree)
            routines.log_output(r, "")
            perm(r, rls, [[argv_ret]], is_log, log_tree, max_proc_num)
            num += 1
            r = tmp_r
            print "AFTER CORRECTION:" + str(depth)
            routines.log_output(r, "")

    return


def brute_fork(r=routines.Node("|1 1 1;", 1, 1, 1), ns_last_pid=1, is_log=1, log_tree=routines.Node(["", "", "|1 1 1 ;[]"])):
    lst = []
    routines.dfs(r, routines.worker_list_nodes, routines.worker_empty, [], lst) # lst - list of crafted pointers ptr
    sys.setrecursionlimit(1000000)
    perm(r, ["fork"], [[ns_last_pid]], is_log, log_tree)

#    routines.log_output(log_tree, "log_tree.txt")

#    routines.pkl_write(log_tree,"log_tree.pkl")
#    routines.pkl_write(log_tree, "process_tree.repr")
    return r


N=routines.Node("|1 1 1;", 1, 1, 1)
R=routines.Node("|2 1 1;", 2, 1, 1, parent=N)

brute_fork(N, 4)
