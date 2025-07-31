import re
from collections import deque, defaultdict

#STEP 1: PARSE TEXT FILE
def parsing_file (filename):
    with open (filename, 'r') as f:
        lines = f.readlines()
    kb = []
    query = ""
    mode = None
    for line in lines:
        line = line.strip()
        if line == "TELL":
            mode = "TELL"
            continue
        elif line == "ASK":
            mode = "ASK"
            continue
    
        if mode == "TELL":
            clauses = line.split(';')
            for clause in clauses:
                clause = clause.replace(" ", "")
                if clause:
                    kb.append(clause)
        elif mode == "ASK":
            query = line.strip()
    print("PARSED KB:", kb)
    print("QUERY: ", query)
    return kb, query
            

# STEP 2: TT table
"""
function TT-ENTAILS?(KB,α) returns true or false
    inputs: KB, the knowledge base, a sentence in propositional logic
        α, the query, a sentence in propositional logic
    
    symbols ← a list of the proposition symbols in KB and α
    return TT-CHECK-ALL(KB,α, symbols, { })
-----------------------------------------------------------------------
function TT-CHECK-ALL(KB,α, symbols , model) returns true or false
    if EMPTY?(symbols) then
        if PL-TRUE?(KB, model) then return PL-TRUE?(α, model)
        else return true // when KB is false, always return true
    else do
        P ← FIRST(symbols)
        rest ← REST(symbols)
        return (TT-CHECK-ALL(KB,α, rest, model ∪ {P = true})
            and
            TT-CHECK-ALL(KB,α, rest, model ∪ {P = false }))
"""
def TT_entails(kb, query):
    all_expr = kb + [query]
    all_expr_str = ' '.join(all_expr)
    symbols = sorted(set(re.findall("[a-zA-Z][a-zA-Z0-9_]*", all_expr_str)))
    
    print(list(symbols))

    result = TT_check_all(kb, query, symbols, {})
    if result:
        print(f"YES: {result}")
    else:
        print("NO")


def pl_true(clause, model):
    # Step 1: Bi-conditional: A <=> B becomes (A == B)
    clause = clause.replace("<=>", " == ")

    # Step 2: Implication: A => B becomes (not (A) or B)
    # Convert all implications safely
    while "=>" in clause:
        match = re.search(r'\(([^()]+)\)\s*=>\s*\(([^()]+)\)', clause) # (a & b) => (c || d)
        if not match:
            match = re.search(r'([^\s()]+)\s*=>\s*\(([^()]+)\)', clause) # p1 => (a & b)
        if not match:
            match = re.search(r'\(([^()]+)\)\s*=>\s*([^\s()]+)', clause) # (a & b) => c
        if not match:
            match = re.search(r'([^\s()]+)\s*=>\s*([^\s()]+)', clause) # ex: a => b

        if match:
            A = match.group(1).strip()
            B = match.group(2).strip()
            clause = clause.replace(match.group(0), f"(not ({A}) or ({B}))")
        else:
            break

    # Step 3: Negation: replace ~X with not (X)
    clause = re.sub(r'~\s*([a-zA-Z_][a-zA-Z0-9_]*)', r' not (\1)', clause) # ~a -> not (a)

    # Step 4: Replace AND, OR
    clause = clause.replace("&", " and ")
    clause = clause.replace("||", " or ")

    # Step 5: Replace propositional symbols with model values
    for symbol in model:
        clause = re.sub(r'\b' + re.escape(symbol) + r'\b', str(model[symbol]), clause) # a -> True

    return eval(clause)

def TT_check_all(kb, query, symbols, model, count_mode = True):
    if symbols == []:
        kb_true = all(pl_true(clause, model) for clause in kb)
        query_true = pl_true(query, model) 

        if count_mode:
            return int(kb_true and query_true)
        else:
            return query_true if kb_true else True
    else:
        P = symbols[0]
        rest = symbols[1:]

        model_true = model.copy()
        model_true[P] = True

        model_false = model.copy()
        model_false[P] = False

    return (TT_check_all(kb, query, rest, model_true, count_mode) +
            TT_check_all(kb, query, rest, model_false, count_mode)) if count_mode else \
            (TT_check_all(kb, query, rest, model_true, count_mode) and
            TT_check_all(kb, query, rest, model_false, count_mode))

# STEP 3: FC algorithm
"""
PSEUDOCODE: 
function PL-FC-ENTAILS?(KB, q) returns true or false
    inputs: KB, the knowledge base, a set of propositional definite clauses
        q, the query, a proposition symbol
    count ← a table, where count[c] is the number of symbols in c’s premise
    inferred ← a table, where inferred[s] is initially false for all symbols
    agenda ←a queue of symbols, initially symbols known to be true in KB
    
    while agenda is not empty do
        p ← POP(agenda)
        if p = q then return true
        if inferred[p] = false then
            inferred[p] ←true
            for each clause c in KB where p is in c.PREMISE do
                decrement count[c]
                if count[c]=0 then add c.CONCLUSION to agenda
    return false
# """

class NonHornClauseError(Exception):
    pass

def rule_and_facts (kb):
    rules = []
    facts = []

    for clause in kb:
        if "||" in clause or "<=>" in clause:
            raise NonHornClauseError("Non-Horn clause detected: contains disjunction or biconditional")
        if "=>" in clause:
            premise, conclusion = clause.split("=>")
            if (any(op in conclusion for op in  ["&", "||", "<=>", "=>"])):
                raise NonHornClauseError("Conclusion is a single symbol. Ex: p1=> p2")
            premise_symbols = [p.strip() for p in premise.strip().split("&")]
            rules.append((premise_symbols, conclusion.strip()))
        else:
            facts.append(clause.strip())
    return facts, rules

def FC_entails(kb, query):
    facts, rules = rule_and_facts(kb)

    agenda = deque(facts)
    inferred = defaultdict(bool)
    count = {}

    entailed = [] # tracking what has been inferred

    for premise, conclusion in rules:
        count [(tuple(premise), conclusion.strip())] = len(premise)

    while agenda:
        p = agenda.popleft()
        if p == query:
            print("YES: ", ', '.join(entailed + [p]))
            return True
        
        if not inferred[p]:
            inferred[p] = True
            entailed.append(p)
            for premise, conclusion in rules:
                if p in premise:
                    count[(tuple(premise), conclusion.strip())] -= 1
                    if count[(tuple(premise), conclusion.strip())] == 0:
                        agenda.append(conclusion)
    
    print("NO")
    return False
        

# STEP 4: BC algorithm
"""
function PL-BC-ENTAILS?(KB, q) returns true or false 
    inputs: KB, the knowledge base, a set of propositional definite clauses
            q, the query, a proposition symbol
    
    return BC-OR(KB, q, [])

----------------------------------------------------
/// prove a single goal. /////
function BC-OR(KB, goal, visited) returns true or false
    if goal is in visited then return false      // prevent loops
    if goal is a known fact in KB then return true

    for each rule in KB where CONCLUSION = goal do
        if BC-AND(KB, rule.PREMISE, visited ∪ {goal}) then
            return true

    return false
----------------------------------------------------
////////  prove a set of goals /////////
function BC-AND(KB, goals, visited) returns true or false
    if goals is empty then return true
    for each subgoal in goals do
        if not BC-OR(KB, subgoal, visited) then
            return false
    return true
"""
def BC_entails(kb, query):
    facts, rules = rule_and_facts(kb)
    visited = set()
    entailed = []   

    def BC_or(goal, visited):
        if goal in facts: 
            if goal not in entailed:
                entailed.append(goal)
            return True
        if goal in visited: 
            return False
        
        visited = visited.union({goal}) 
        
        for premises, conclusion in rules:
            if conclusion == goal:
                if BC_and(premises, visited):
                    if goal not in entailed:
                        entailed.append(goal)
                    return True
        return False

    def BC_and(premises, visited):
        for premise in premises:
            if not BC_or(premise, visited.copy()):
                return False
        return True
    
    if BC_or(query, visited):
        print("YES: " + ", ".join(entailed))
        return True
    else:
        print("NO")
        return False