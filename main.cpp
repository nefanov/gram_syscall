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
void worker_reconstruct(representor* r,void* par) {
    string *s=(string*)par;
    s->append("|");
    s->append(std::to_string(r->p));
    s->append(std::to_string(r->s));
    s->append(std::to_string(r->g));
    s->append("[");
}

void worker_reconstruct_finalizer(representor* r, void* par) {
    string *s=(string*)par;
    s->append("]");
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
void* dfs(representor* r, int (*work)(representor*,void*), void *work_finalizer(representor*,void*),void *ret) {
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

void rule_setsid(representor *parent,unsigned int sid) {
    return;
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

int main()
{

    return 0;
}
