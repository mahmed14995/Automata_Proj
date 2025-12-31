from flask import Flask, render_template, request
app = Flask(__name__)

# ==================================================
# DFA CREATION FUNCTION
# ==================================================
def create_dfa(regex_name):
    """
    Creates DFA manually according to the selected regex
    """
    # Initialize default values
    states = {"q0"}
    alphabet = {"0", "1"}
    start_state = "q0"
    final_states = {"q0"}
    transitions = {}
    description = "Unknown"
    regex = ""
    
    # DFA for contains "01" as substring
    if regex_name == "contains_01":
        states = {"q0", "q1", "q2"}
        alphabet = {"0", "1"}
        start_state = "q0"
        final_states = {"q2"}
        transitions = {
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q1",
            ("q1", "1"): "q2",
            ("q2", "0"): "q2",
            ("q2", "1"): "q2",
        }
        description = "Contains '01' as substring"
        regex = "(0|1)*01(0|1)*"
    
    # DFA for alternating string
    elif regex_name == "alternating":
        states = {"q0", "q1", "q2", "qDead"}
        alphabet = {"0", "1"}
        start_state = "q0"
        final_states = {"q0", "q1", "q2"}
        transitions = {
            ("q0", "0"): "q1",
            ("q0", "1"): "q2",
            ("q1", "0"): "qDead",
            ("q1", "1"): "q2",
            ("q2", "0"): "q1",
            ("q2", "1"): "qDead",
            ("qDead", "0"): "qDead",
            ("qDead", "1"): "qDead",
        }
        description = "Alternating 0s and 1s"
        regex = "ε | 0 | 1 | (01)* | (10)* | 0(10)* | 1(01)*"
    
    # DFA for even number of 0s
    elif regex_name == "even_0s":
        states = {"q0", "q1"}
        alphabet = {"0", "1"}
        start_state = "q0"
        final_states = {"q0"}
        transitions = {
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q0",
            ("q1", "1"): "q1",
        }
        description = "Even number of 0s"
        regex = "1*(01*01*)*"
    
    # DFA for contains "ab" as substring
    elif regex_name == "contains_ab":
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        start_state = "q0"
        final_states = {"q2"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q0",
            ("q1", "a"): "q1",
            ("q1", "b"): "q2",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
        }
        description = "Contains 'ab' as substring"
        regex = "(a|b)*ab(a|b)*"
    
    # DFA for does NOT end with "01"
    elif regex_name == "not_ends_01":
        states = {"q0", "q1", "q2"}
        alphabet = {"0", "1"}
        start_state = "q0"
        final_states = {"q0", "q1"}
        transitions = {
            ("q0", "0"): "q1",
            ("q0", "1"): "q0",
            ("q1", "0"): "q1",
            ("q1", "1"): "q2",
            ("q2", "0"): "q1",
            ("q2", "1"): "q0",
        }
        description = "Does NOT end with '01'"
        regex = "ε | (0|1)*(00|10|11)"
    
    # DFA for odd number of 1s
    elif regex_name == "odd_1s":
        states = {"q0", "q1"}
        alphabet = {"0", "1"}
        start_state = "q0"
        final_states = {"q1"}
        transitions = {
            ("q0", "0"): "q0",
            ("q0", "1"): "q1",
            ("q1", "0"): "q1",
            ("q1", "1"): "q0",
        }
        description = "Odd number of 1s"
        regex = "0*1(0|10*1)*0*"
    
    # DFA for contains "aa" as substring
    elif regex_name == "contains_aa":
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        start_state = "q0"
        final_states = {"q2"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q0",
            ("q1", "a"): "q2",
            ("q1", "b"): "q0",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
        }
        description = "Contains 'aa' as substring"
        regex = "(a|b)*aa(a|b)*"
    
    return {
        "states": states,
        "alphabet": alphabet,
        "start": start_state,
        "final": final_states,
        "transitions": transitions,
        "description": description,
        "regex": regex
    }

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def generate_transition_table(dfa):
    """Generate transition table as HTML"""
    states_list = sorted(list(dfa["states"]))
    alphabet_list = sorted(list(dfa["alphabet"]))
    
    table_html = '<table class="transition-table">'
    table_html += '<tr><th>State</th>'
    for symbol in alphabet_list:
        table_html += f'<th>{symbol}</th>'
    table_html += '</tr>'
    
    for state in states_list:
        is_final = "+" if state in dfa["final"] else ""
        is_start = "→" if state == dfa["start"] else ""
        table_html += f'<tr><td>{is_start} {state} {is_final}</td>'
        
        for symbol in alphabet_list:
            next_state = dfa["transitions"].get((state, symbol), "-")
            table_html += f'<td>{next_state}</td>'
        table_html += '</tr>'
    
    table_html += '</table>'
    return table_html

def generate_transition_function(dfa):
    """Generate transition function notation"""
    transitions_list = []
    for (state, symbol), next_state in sorted(dfa["transitions"].items()):
        transitions_list.append(f"δ({state}, {symbol}) = {next_state}")
    return transitions_list

def generate_diagram_data(dfa):
    """Generate data for visualization diagram"""
    nodes = []
    edges = []
    
    for state in dfa["states"]:
        node_type = "start" if state == dfa["start"] else ""
        node_type += " final" if state in dfa["final"] else ""
        nodes.append({"id": state, "type": node_type.strip()})
    
    for (from_state, symbol), to_state in dfa["transitions"].items():
        existing_edge = None
        for edge in edges:
            if edge["from"] == from_state and edge["to"] == to_state:
                existing_edge = edge
                break
        
        if existing_edge:
            existing_edge["label"] += f", {symbol}"
        else:
            edges.append({"from": from_state, "to": to_state, "label": symbol})
    
    return {"nodes": nodes, "edges": edges}

# ==================================================
# ROUTE
# ==================================================
@app.route("/", methods=["GET", "POST"])
def index():
    steps = []
    result = ""
    selected_regex = "contains_01"
    transition_table = ""
    transition_function = []
    diagram_data = None
    input_string = ""
    dfa_info = None
    
    if request.method == "POST":
        selected_regex = request.form["regex"]
        input_string = request.form.get("string", "")
        
        # CREATE DFA
        dfa = create_dfa(selected_regex)
        dfa_info = dfa
        
        # Generate visualizations
        transition_table = generate_transition_table(dfa)
        transition_function = generate_transition_function(dfa)
        diagram_data = generate_diagram_data(dfa)
        
        if input_string:
            current_state = dfa["start"]
            steps.append(f"Start State: {current_state}")
            
            valid = True
            for i, ch in enumerate(input_string):
                if ch not in dfa["alphabet"]:
                    result = f"❌ STRING INVALID - Character '{ch}' at position {i+1} is not in alphabet {{{', '.join(sorted(dfa['alphabet']))}}}"
                    valid = False
                    break
                
                if (current_state, ch) not in dfa["transitions"]:
                    steps.append(f"Read '{ch}': {current_state} → [No transition]")
                    result = "❌ STRING REJECTED (No valid transition)"
                    valid = False
                    break
                
                next_state = dfa["transitions"][(current_state, ch)]
                steps.append(f"Read '{ch}': {current_state} → {next_state}")
                current_state = next_state
            
            if valid:
                steps.append(f"Final State: {current_state}")
                
                if current_state in dfa["final"]:
                    result = f"✅ STRING VALID & ACCEPTED - String '{input_string}' matches the pattern '{dfa['description']}'"
                else:
                    result = f"⚠️ STRING VALID BUT REJECTED - String '{input_string}' does not match the pattern '{dfa['description']}'"
    else:
        # Just show visualizations for default regex
        dfa = create_dfa(selected_regex)
        dfa_info = dfa
        transition_table = generate_transition_table(dfa)
        transition_function = generate_transition_function(dfa)
        diagram_data = generate_diagram_data(dfa)
    
    return render_template(
        "index.html",
        steps=steps,
        result=result,
        selected_regex=selected_regex,
        transition_table=transition_table,
        transition_function=transition_function,
        diagram_data=diagram_data,
        input_string=input_string,
        dfa_info=dfa_info
    )

# ==================================================
# RUN APPLICATION
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)