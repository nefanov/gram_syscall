#include <iostream>
#include <vector>
#include <sstream>
#include <cstdlib>

using namespace std;
/* representation structure */
typedef struct repr {
    unsigned int p;
    unsigned int s;
    unsigned int g;
    vector<struct repr> children;

} representor;

/* init the new process without children */
void init(representor *r,unsigned int p,unsigned int s,unsigned int g) {
    r->p=p;
    r->s=s;
    r->g=g;

    return;
}

/* LIST ROUTINES */
/* list_child_add routine adds given child to the tail of children list */
/* 0 - OK, -1 - ERR */

int list_child_add(representor* parent,representor child) {
    parent->children.push_back(child);

    return 0;
}

/* WORKERS */

/* worker: reconstruct the string */
void worker_reconstruct(representor* r,void *par) {
    string *s=(string*)par;
    s->append("|");
    s->append(std::to_string(r->p));
    s->append(std::to_string(r->s));
    s->append(std::to_string(r->g));
    s->append("[");
}

void worker_reconstruct_finalizer(representor* r, void *par) {
    string *s=(string*)par;
    s->append("]");
}

/* worker: search for process with a given pgid and return pid in *par if there are no one,
 * else return -1 */
void worker_pgid_lookup(representor* r, void *par) {
    if (*(int*)par==r->g)
        *(int*)par=-1;
    return;
}

/* stub worker: nothing to do there:) */
void worker_stub(representor* r, void *par) {
    return;
}
/* worker: count the nodes
int worker_count() {
    static int nodes;
    nodes++;
    return nodes;
}
*/
/* /WORKERS */

/* GRAPH ROUTINES */
int dfs(representor* r, void (*work)(representor*,void*), void (*work_finalizer)(representor*,void*),void *ret) {
    (*work)(r,ret);
    for(vector<struct repr>::iterator it = r->children.begin() ; it != r->children.end(); ++it) {
        dfs(&(*it),work,work_finalizer,ret);

    }
    (*work_finalizer)(r,ret);

    return 0;
}

int bfd(representor* r) {
    static int nodes;
    nodes++;

    return nodes;
}

/* RULES */
int rule_fork(representor* parent, unsigned int pid) {
    representor child;
    init(&child,pid,parent->s,parent->g);
    if(list_child_add(parent, child))
        return -1;
    return 0;
}

int rule_setsid(representor *parent) {
    if (parent->p == parent->g) {
        return -1;
    }
    /*else if there are any process with group == parent->pid -> return -1*/
    int pgid=parent->p;
    dfs(parent,&worker_pgid_lookup,&worker_stub,&pgid);
    if (pgid==-1) {
        return -1;
    }
    else {
        parent->s = parent->g = parent->p;
    }
    return 0;
}
void rule_setpgid(representor *parent,unsigned int pgid) {
    return;
}

void exit() {
    return;
}

int abstract_rule(representor *parent,int argc,char** argv) {
    return 0;
}

/* /RULES */

/* SET ROUTINES */
representor* bruteforce(representor*);

representor* optimizer(representor*);

/* /SET ROUTINES */

int main()
{

    return 0;
}
