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
    #  ! lst is crafted pointer list
    global depth
    depth += 1
    print "Recurion step: depth " + str(depth)
    lst = [node for node in routines.PreOrderIter(r)]
    routines.log_output(r, "")
#    print str(len(lst))
#    print lst
    if len(lst) >= max_proc_num:
        depth -= 1
        return
    cnt = 0
    for num, node in enumerate(lst): # cycle iterates on changable list but r_branch is saved copy of this instance
#        routines.log_output(r, "")
        print "             num " + str(num)
#        print num
        for rn, rule in enumerate(rls):
            tmp_r = copy.deepcopy(r)
            argv_ret = getattr(rules, rule)(node, *argv[rn])

            if is_log:
                log_tree = routines.Node([rule, '('+','.join([str(x) for x in argv[rn]])+')', routines.construct(r)], parent=log_tree)
                #print "node #" + str(num+1) + " of " + str(len(lst)) + ":" + routines.construct(r)[0] + " ; "
#                print argv_ret
#                routines.log_output(r, "")

            perm(r, rls, [[argv_ret]], is_log, log_tree, max_proc_num)
            r = tmp_r
#            print "    leave"
            depth -= 1
    return


def brute_fork(r=routines.Node("|1 1 1;", 1, 1, 1), ns_last_pid=1, is_log=1, log_tree=routines.Node(["", "", "|1 1 1 ;[]"])):
    lst = []
    routines.dfs(r, routines.worker_list_nodes, routines.worker_empty, [], lst) # lst - list of crafted pointers ptr
    sys.setrecursionlimit(1000000)
    perm(r, ["fork"], [[ns_last_pid]], is_log, log_tree)

    routines.log_output(log_tree, "log_tree.txt")

#    routines.pkl_write(log_tree,"log_tree.pkl")
#    routines.pkl_write(log_tree, "process_tree.repr")
    return r


brute_fork()
