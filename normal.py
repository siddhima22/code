#first
n = int(input("Enter number of prod: "))
prod = {}

for _ in range(n):
    line = input("Enter production (e.g., A->a|@): ").replace(" ", "")
    lhs, rhs = line.split("->")
    prod[lhs] = rhs.split("|")

# Compute FIRST sets
def compute_first(prod):
    first = {nt: set() for nt in prod}  # FIRST set for each non-terminal
    changed = True
    while changed:
        changed = False
        for nt in prod:
            for exp in prod[nt]:
                for i, sym in enumerate(exp):
                    if not sym.isupper():  # It's a terminal or epsilon (@)
                        if sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        break  # Done with this rule

                    else:  # It's a non-terminal
                        before = len(first[nt])
                        first[nt] |= first[sym] - {'@'}  # Add all except epsilon
                        if '@' not in first[sym]:
                            break  # Stop if no epsilon
                    # If all before had epsilon and we reached the end
                    if i == len(exp) - 1:
                        if '@' not in first[nt]:
                            first[nt].add('@')
                            changed = True
    return first

first_sets = compute_first(prod)

# Display FIRST sets
print("\nFIRST sets:")
for nt in sorted(prod):
    print(f"{nt} : {' '.join(sorted(first_sets[nt]))}")


#ll1
def first_of_string(string, first):
  result = set()
  for sym in string:
    if sym.isupper():
      result |= first[sym] - {'@'}
      if '@' not in first[sym]:
        break
    else:
        result.add(sym)
        break
  else:
      result.add('@')

  return result

def build_ll1_table(productions, first, follow):
  table = {}
  for nt, rules in productions.items():
    for prod in rules:
      first_set = first_of_string(prod, first)
      for sym in first_set - {'@'}:
        table[(nt, sym)] = prod
      if '@' in first_set:
        for sym in follow[nt]:
          table[(nt, sym)] = prod
  return table

def print_ll1_table(table, productions):
    terminals = sorted({t for (_, t) in table if t != '@'} | {'$'})
    column_width = 10  # Fixed width for alignment

    # Print header row
    print(" " * 6, end="")
    for t in terminals:
        print(t.ljust(column_width), end="")
    print()

    # Print each row
    for nt in productions:
        print(nt.ljust(6), end="")
        for t in terminals:
            rule = table.get((nt, t), "")
            print(rule.ljust(column_width), end="")
        print()



n = int(input("Number of productions: "))
productions = {}
for _ in range(n):
    lhs, rhs = input("Enter production: ").split("->")
    productions[lhs.strip()] = [p.strip() for p in rhs.split("|")]

first= {}
print("enter firsts: ")
for nt in productions:
  first[nt] = set(input(f"enter first of {nt}: ").split())

follow= {}
print("enter follow: ")
for nt in productions:
  follow[nt] = set(input(f"enter first of {nt}: ").split())

table = build_ll1_table(productions, first, follow)
print("\nLL(1) Parsing Table:")
print_ll1_table(table, productions)

#follow
def compute_follow(productions, first, start):
    follow = {nt: set() for nt in productions}
    follow[start].add('$')  # The follow set of the start symbol contains $

    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            for rhs in rules:
                for i, sym in enumerate(rhs):
                    if sym.isupper():  # Process only non-terminals
                        temp = set()
                        for nxt in rhs[i + 1:]:
                            if nxt.isupper():
                                temp |= first[nxt] - {'@'}  # Don't add epsilon (@)
                                if '@' not in first[nxt]:  # Stop if epsilon is not present
                                    break
                            else:
                                temp.add(nxt)  # Add terminal
                                break
                        else:
                            temp |= follow[lhs]  # If nothing follows, inherit the follow of LHS

                        if not temp.issubset(follow[sym]):
                            follow[sym] |= temp  # Add to follow set
                            changed = True
   
    return follow


n = int(input("Number of productions: "))
productions = {}
for _ in range(n):
    lhs, rhs = input("ENTER PRODUCTIONS: ").split("->")
    productions[lhs] = rhs.split("|")

first = {}
print("Enter FIRST sets:")
for nt in productions:
    first[nt] = set(input(f"FIRST({nt}): ").split())

start = input("Start symbol: ")

follow = compute_follow(productions, first, start)

# Print FOLLOW sets with '$' instead of '@'
print("\nFOLLOW sets:")
for nt in sorted(follow):
    print(f"{nt} : {' '.join(sorted(follow[nt]))}")

#tac
def prec(op):  # precedence of operator
    if op in ['*', '/']:
        return 2
    elif op in ['+', '-']:
        return 1
    return 0

def is_op(ch):  # is operator
    return ch in '+-*/'

def tac(exp):
    t = 65        #ord('A')  # temporary variable name starts from 'A'
    left = ''     # left side of =

    if '=' in exp:
        left = exp[0]
        exp = exp[2:]  # remove "a=" part

    val = []  # operands
    op = []   # operators

    for ch in exp:
        if ch.isalpha():  # a, b, c, etc.
            val.append(ch)
        elif is_op(ch):
            while op and prec(op[-1]) >= prec(ch):
                o = op.pop()
                y = val.pop()
                x = val.pop()
                print(f"{chr(t)} = {x} {o} {y}")
                val.append(chr(t))
                t += 1
            op.append(ch)

    while op:
        o = op.pop()
        y = val.pop()
        x = val.pop()
        print(f"{chr(t)} = {x} {o} {y}")
        val.append(chr(t))
        t += 1

    if left and val:
        print(f"{left} = {val[0]}")

# 💡 Try it out
expr = input("Enter expression (like a=b+c*d): ")
tac(expr)

#macro parcer
n = int(input("Enter number of lines: "))
print("Enter macro code:")
code = [input().strip() for _ in range(n)]

ALA = []              
MNT = []              
MDT = []              
in_macro = False

i = 0
while i < n:
    line = code[i]

    if line == "MACRO":
        in_macro = True
        i += 1  # Move to macro definition line
        macro_def = code[i]
        parts = macro_def.split()

        macro_name = parts[0]
        args = [arg.strip(",") for arg in parts[1:] if arg.startswith("&")]

        # Add args to ALA if not already present
        for arg in args:
            if arg not in ALA:
                ALA.append(arg)
        # Save macro name and current MDT index
        MNT.append((macro_name, len(MDT) + 1))  # +1 for 1-based indexing
        MDT.append(macro_def)
    
    elif line == "MEND":
        in_macro = False
        MDT.append("MEND")

    elif in_macro:
        # Replace args with #index from ALA
        for arg in ALA:
            if arg in line:
                line = line.replace(arg, f"#{ALA.index(arg)}")
        MDT.append(line)

    i += 1  # Move to next line

print("\nALA (Argument List Array):")
for idx, arg in enumerate(ALA):
    print(f"{idx} {arg}")

print("\nMNT (Macro Name Table):")
for idx, (name, mdt_index) in enumerate(MNT, start=1):
    print(f"{idx} {name} -> MDT index {mdt_index}")

print("\nMDT (Macro Definition Table):")
for idx, line in enumerate(MDT, start=1):
    print(f"{idx} {line}")

#left rec
prods = {}
new_prod = {}

n = int(input("Enter number of productions: "))

# Read the prods productions
for _ in range(n):
    line = input("Enter production (e.g., A->Aa|b): ")
    lhs, rhs = line.split("->")
    rhs_parts = rhs.split("|")

    if lhs not in prods:
        prods[lhs] = []
    prods[lhs] += rhs_parts  # prods[lhs].extend(rhs_parts)

for nt in prods:  # 'nt' for non-terminal
    alpha = []  # Left recursive parts (alpha)
    beta = []   # Non-recursive parts (beta)

    for rhs in prods[nt]:
        if rhs.startswith(nt):
            alpha.append(rhs[len(nt):])  # Remove the non-terminal (A)
        else:
            beta.append(rhs)

    if alpha:
        new_nt = nt + "'"  # New non-terminal (A')
        new_prod[nt] = []
        new_prod[new_nt] = []

        for b in beta:
            new_prod[nt].append(b + new_nt)

        for a in alpha:
            new_prod[new_nt].append(a + new_nt)

        new_prod[new_nt].append('@')  # Epsilon (empty string)
    else:
        new_prod[nt] = prods[nt]

updated_prods = new_prod

# Print the updated prods after removing left recursion
print("\nprods after removing left recursion:")
for lhs, rhs_list in updated_prods.items():
    print(f"{lhs} -> {' | '.join(rhs_list)}")


# OR 
# for lhs, rhs_list in updated_prods.items():
#         print(f"{lhs} -> ", end="")
#         for rhs in rhs_list:
#             print(rhs, end=" | ")
#         print()  # For a new line after each production


#code optimizer

n = int(input("Enter number of 3-address code statements: "))
data = [input(f"Enter statement {i+1}: ").strip() for i in range(n)]

unique, dup, final, rename = {}, {}, {}, {}
count = 1

# Step 1: Eliminate common subexpressions
for line in data:
    lhs, rhs = line.split("=")
    lhs, rhs = lhs.strip(), rhs.strip()

    # Replace duplicates in the expression
    for old, new in dup.items():
        rhs = rhs.replace(old, new)

    if rhs not in unique.values():
        unique[lhs] = rhs
    else:
        for lhsn, rhsn in unique.items():
            if rhsn == rhs:
                dup[lhs] = lhsn
                break

# Step 2: Rename variables to avoid conflict
for lhs, rhs in unique.items():
    new_var = f"t{count}"

    # Replace old names in the expression with renamed versions
    for old, new in rename.items():
        rhs = rhs.replace(old, new)

    final[new_var] = rhs
    rename[lhs] = new_var
    count += 1

# Step 3: Print the optimized code
print("\nOptimized Code:")
for var, expr in final.items():
    print(f"{var} = {expr}")

#lex analyzer
# Define sets of keywords, operators, and separators to look for
keywords = {"int", "float", "char", "continue", "for", "if", "break", "while", "string", "double"}
operators = {"+", "-", "*", "%", "/", "<", ">", "="}
separators = {";", ",", ":", "(", ")", "[", "]", "{", "}"}

# Dictionary to store categorized tokens
ans = {
    "keywords": set(),
    "operators": set(),
    "separators": set(),
    "constants": set(),
    "identifier": set()
}

# Function to split a line of code into tokens
def split_string(s):
    token = []   # List to store the final tokens
    temp = ""    # Temporary string to build multi-character tokens

    for ch in s:
        if ch.isspace():
            if temp:
                token.append(temp)
                temp = ""
        elif ch in separators:
            if temp:
                token.append(temp)
                temp = ""
            token.append(ch)
        else:
            temp += ch

    if temp:
        token.append(temp)

    return token

# Input from the user for number of code lines
n = int(input("Enter number of lines: "))
print("Enter your code line by line:")

# Loop to process each line
for _ in range(n):
    line = input()               # Read the line of code
    tokens = split_string(line) # Split it into tokens

    # Loop through each token using 't' as the loop variable
    for t in tokens:
        if not t:
            continue  # Skip if token is empty

        if t.isdigit():
            ans["constants"].add(t)
        elif t in keywords:
            ans["keywords"].add(t)
        elif t in operators:
            ans["operators"].add(t)
        elif t in separators:
            ans["separators"].add(t)
        elif t.startswith('"') and t.endswith('"'):
            ans["constants"].add(t[1:-1])
        else:
            if len(t) > 1 and t[1] in operators:
                ans["identifier"].add(t[0])
                ans["operators"].add(t[1])
            else:
                ans["identifier"].add(t)

# Print the results
print("\nLexical Analysis Result:")
for key, values in ans.items():
    print(key + ": ", end="")
    for value in values:
        print(  value ,end=" ")
    print()



