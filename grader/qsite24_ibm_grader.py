from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import PrimitiveResult, StatevectorSampler
from qiskit.quantum_info import Operator
from qiskit_ibm_runtime.fake_provider import FakeGuadalupeV2
from qiskit.transpiler import CouplingMap
from qiskit_ibm_runtime.ibm_backend import IBMBackend
import numpy as np

##
## Lab 1: First Steps
##

def qsite24_grader_lab1ex1(result: PrimitiveResult):
    
    try:
        counts = result[0].data.c.get_counts()
    except:
        print("Error! The result object is not correctly formatted.")
        return

    if not ('00' in counts and '11' in counts):
        print("Incorrect! The measured states do not correspond to the expected Bell state")
        return
    
    counts00 = float(counts['00']) / float(counts['00'] + counts['11'])
    if counts00 > 0.45 and counts00 < 0.55:
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! The measured states do not correspond to the expected Bell state")

    return


def qsite24_grader_lab1ex2a(circuit: QuantumCircuit):
    
    sampler = StatevectorSampler()
    input_combos = ['00', '01', '10', '11']
    expected_outputs = ['00', '01', '01', '10']

    for input, exp_output in zip(input_combos, expected_outputs):
        
        a = input[0]
        b = input[1]
        qc_in = QuantumCircuit(4, 2)
        if a == '1':
            qc_in.x(0)
        if b == '1':
            qc_in.x(1)
        qc_in = circuit.compose(qc_in, front=True)
        
        pub = (qc_in)
        job = sampler.run([pub], shots=1024)
        c_sum = job.result()[0].data.c_sum.get_counts()
        c_carry = job.result()[0].data.c_carry.get_counts()
        
        if len(c_sum.items()) != 1 or len(c_carry.items()) != 1:
            print("Incorrect! The circuit does not produce correct outputs.")
            return
        
        if exp_output[0] in c_sum and exp_output[1] in c_carry:
            print("Congratulations! 🎉 Your answer is correct.")
        else:
            print("Incorrect! The circuit does not produce correct outputs.")
        
        return
    

def qsite24_grader_lab1ex2b(result: PrimitiveResult):
    
    try:
        c_sum = result[0].data.c_sum.get_counts()
        c_carry = result[0].data.c_carry.get_counts()
    except:
        print("Error! The result object is not correct.")
        return
    
    if len(c_sum.items()) != 1 or len(c_carry.items()) != 1:
        print("Incorrect! The circuit does not produce correct outputs.")
        return
    
    if '0' in c_sum and '1' in c_carry:
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! The circuit does not produce correct outputs.")

    return


##
## LAB 2: Quantum Enigma
##


def qsite24_grader_lab2ex1a(circuit: QuantumCircuit):

    q_reg_squares = QuantumRegister(4, name='squares')
    q_reg_key = QuantumRegister(2, name='key')
    q_reg_afocus = QuantumRegister(2, name='afocus')
    q_reg_bfocus = QuantumRegister(2, name='bfocus')
    c_reg_key_bfocus = ClassicalRegister(4, name='c_key_bfocus')
    qc_soln = QuantumCircuit(q_reg_squares, q_reg_key, q_reg_afocus, q_reg_bfocus, c_reg_key_bfocus)
    
    qc_soln.h(q_reg_squares)
    qc_soln.h(q_reg_key)

    qc_soln.cx(q_reg_squares[1], q_reg_afocus[0])
    qc_soln.cx(q_reg_squares[3], q_reg_afocus[0])
    qc_soln.cx(q_reg_squares[2], q_reg_afocus[1])
    qc_soln.cx(q_reg_squares[3], q_reg_afocus[1])

    qc_soln.cx(q_reg_key[0], q_reg_afocus[0])
    qc_soln.cx(q_reg_key[1], q_reg_afocus[1])

    op_soln = Operator(qc_soln)
    op_submitted = Operator(circuit)

    if op_soln.equiv(op_submitted):
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! Check your circuit.")

    return


def qsite24_grader_lab2ex1b(circuit: QuantumCircuit):

    q_reg_squares = QuantumRegister(4, name='squares')
    q_reg_key = QuantumRegister(2, name='key')
    q_reg_afocus = QuantumRegister(2, name='afocus')
    q_reg_bfocus = QuantumRegister(2, name='bfocus')
    c_reg_key_bfocus = ClassicalRegister(4, name='c_key_bfocus')
    qc_soln = QuantumCircuit(q_reg_squares, q_reg_key, q_reg_afocus, q_reg_bfocus, c_reg_key_bfocus)
    
    qc_soln.h(q_reg_squares)
    qc_soln.h(q_reg_key)

    qc_soln.cx(q_reg_squares[1], q_reg_afocus[0])
    qc_soln.cx(q_reg_squares[3], q_reg_afocus[0])
    qc_soln.cx(q_reg_squares[2], q_reg_afocus[1])
    qc_soln.cx(q_reg_squares[3], q_reg_afocus[1])

    qc_soln.cx(q_reg_key[0], q_reg_afocus[0])
    qc_soln.cx(q_reg_key[1], q_reg_afocus[1])

    qc_soln.mcx(q_reg_afocus, q_reg_squares[3])
    qc_soln.x(q_reg_afocus[0])
    qc_soln.mcx(q_reg_afocus, q_reg_squares[2])
    qc_soln.x(q_reg_afocus[0])
    qc_soln.x(q_reg_afocus[1])
    qc_soln.mcx(q_reg_afocus, q_reg_squares[1])
    qc_soln.x(q_reg_afocus[1])
    qc_soln.x(q_reg_afocus)
    qc_soln.mcx(q_reg_afocus, q_reg_squares[0])
    qc_soln.x(q_reg_afocus)

    op_soln = Operator(qc_soln)
    op_submitted = Operator(circuit)

    if op_soln.equiv(op_submitted):
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! Check your circuit.")

    return


def qsite24_grader_lab2ex1c(result: PrimitiveResult):

    try:
        counts = result[0].data.c_key_bfocus.get_counts()
    except:
        print("Error! The result object is not correctly formatted.")
        return
    
    if len(counts.items()) != 4:
        print("Incorrect! The measured results are not as expected")
        return
    
    if '0000' in counts and '0101' in counts and '1010' in counts and '1111' in counts:
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! The measured results are not as expected")

    return


def qsite24_grader_lab2ex2(result: PrimitiveResult):

    try:
        counts = result[0].data.c_key_focus.get_counts()
    except:
        print("Error! The result object is not correctly formatted.")
        return
    
    if len(counts.items()) != 16:
        print("Incorrect! The measured results are not as expected")
        return
    
    if (    '00000000' in counts and
            '00010001' in counts and
            '00100010' in counts and 
            '00110011' in counts and
            '01000100' in counts and
            '01010101' in counts and
            '01100110' in counts and
            '01110111' in counts and
            '10001000' in counts and
            '10011001' in counts and
            '10101010' in counts and
            '10111011' in counts and
            '11001100' in counts and
            '11011101' in counts and
            '11101110' in counts and
            '11111111' in counts):
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! The measured results are not as expected")

    return


#
# LAB 3: Utility Scale
#

def _gen_rzx_circ():

    qc_rzz = QuantumCircuit(2)
    qc_rzz.sdg(0)
    qc_rzz.sdg(1)
    qc_rzz.ry(np.pi/2, 1)
    qc_rzz.cx(0, 1)
    qc_rzz.ry(-np.pi/2, 1)
    return qc_rzz
     

def qsite24_grader_lab3ex1a(qc: QuantumCircuit):

    if not isinstance(qc, QuantumCircuit):
        print("Error! Input quantum circuit object is not a QuantumCircuit.")
        return   

    qc_rzz = _gen_rzx_circ()

    op_soln = Operator(qc_rzz)
    op_submitted = Operator(qc)

    if op_soln.equiv(op_submitted):
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! Check your circuit.")
    return


def qsite24_grader_lab3ex1b(qc: QuantumCircuit):

    if not isinstance(qc, QuantumCircuit):
        print("Error! Input quantum circuit object is not a QuantumCircuit.")
        return

    n_qubits = 10
    if qc.num_qubits != n_qubits:
        print("Incorrect! Check the number of qubits in your circuit.")
        return

    RZZp2Gate = _gen_rzx_circ().to_gate()
    qc_layered = QuantumCircuit(n_qubits)
    for j in range(2):
        for i in range(n_qubits//2-j):
            qc_layered.append(RZZp2Gate, [2*i+j, 2*i+j+1])
    
    op_soln = Operator(qc_layered)
    op_submitted = Operator(qc)

    if op_soln.equiv(op_submitted):
        print("Congratulations! 🎉 Your answer is correct.")
    else:
        print("Incorrect! Check your circuit.")
    return


def _filter_directed_edges(cm):
    cm_out = CouplingMap()
    for qubit in range(cm.size()): 
        cm_out.add_physical_qubit(qubit)
    for edge in cm.graph.to_undirected(multigraph=False).edge_list():
        cm_out.add_edge(edge[0], edge[1])
    return cm_out


def _check_num_edges_layers(layers, backend):
    device_edges = _filter_directed_edges(backend.coupling_map).get_edges()
    n_edges_in_layers = 0
    for layer in layers:
        n_edges_in_layers += len(layer)
    if n_edges_in_layers == len(device_edges):
        return True
    else:
        return False
    

def qsite24_grader_lab3ex2a(layers: list[list]):

    if not isinstance(layers, list):
        print("Error! The input argument is not a list.")
        return

    if len(layers) != 3:
        print("Incorrect! Check the number of layers in your list.")
        return

    fake_backend = FakeGuadalupeV2()
    if _check_num_edges_layers(layers, fake_backend) == False:
        print("Incorrect! Check the number of edges in your layers.")
        return
    
    cm = fake_backend.coupling_map
    used_edges = []
    for layer in layers:
        nodes_used = []
        for edge in layer:
            if edge not in cm:
                print("Incorrect! Check the edges in your layers.")
                return
            if edge in used_edges:
                print("Incorrect! Edge", edge, "is repeated.")
                return
            else:
                used_edges.append(edge)
            if edge[0] in nodes_used or edge[1] in nodes_used:
                print("Incorrect! You have conflicting edges in a layer.")
                return
            else:
                nodes_used.append(edge[0])
                nodes_used.append(edge[1])

    print("Congratulations! 🎉 Your answer is correct.")
    
    return


def _get_2q_gate_depth(qc):
    return qc.depth(lambda x: len(x.qubits) == 2)


def _check_transpiled_circuit(qc_t, backend, twoqgate):

    if qc_t.num_qubits != backend.num_qubits:
        print("Incorrect! Check the number of qubits in your circuit.")
        return False

    if _get_2q_gate_depth(qc_t) != 3:
        print("Incorrect! Check the two-qubit depth of your transpiled circuit.")
        return False
    
    ops = qc_t.count_ops()
    basis_gates = backend.configuration().basis_gates
    for op in ops:
        if op != 'barrier' and op not in basis_gates:
            print("Incorrect! There are gates in your circuit that are not part of the basis gate set of the backend. Did you transpile your circuit?")
            return False
    if twoqgate not in ops:
        print("Incorrect! Your circuit does not contain CX gates.")
        return False
    
    edges_in_backend = _filter_directed_edges(backend.coupling_map).get_edges()
    if ops[twoqgate] != len(edges_in_backend):
        print("Incorrect! Your circuit does not have the correct number of CX gates.")
        return False

    print("Congratulations! 🎉 Your answer is correct.")

    return True


def qsite24_grader_lab3ex2b(qc_t: QuantumCircuit):

    if not isinstance(qc_t, QuantumCircuit):
        print("Error! The quantum circuit object is not the correct type.")
        return

    backend = FakeGuadalupeV2()
    _check_transpiled_circuit(qc_t, backend, 'cx')
    return


eagle_backend = ['ibm_brisbane', 'ibm_kyiv', 'ibm_sherbrooke', 'ibm_quebec']

def qsite24_grader_lab3ex3(qc_t: QuantumCircuit, backend: IBMBackend):

    if not isinstance(backend, IBMBackend):
        print("Error! The backend object is not the correct type.")
        return
    
    if not isinstance(qc_t, QuantumCircuit):
        print("Error! The quantum circuit object is not the correct type.")
        return

    if backend.name not in eagle_backend:
        print("Error! Are you using one of 127-qubit real backends from QiskitRuntimeService?")
        return
    
    _check_transpiled_circuit(qc_t, backend, 'ecr')
    return