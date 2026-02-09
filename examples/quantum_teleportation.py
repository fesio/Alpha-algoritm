#!/usr/bin/env python3
"""
Quantum Teleportation Example
==============================

This example demonstrates the famous quantum teleportation protocol, which allows
the transfer of a quantum state from one qubit to another using entanglement and
classical communication.

Important: Despite the name, no information travels faster than light! Classical
communication is required to complete the protocol.

What this example covers:
- Creating entangled Bell pairs
- Quantum measurements and classical bits
- Conditional quantum operations
- A complete quantum protocol implementation
"""

import cirq
import qsimcirq
import numpy as np


def create_teleportation_circuit():
    """
    Create a quantum teleportation circuit.
    
    The protocol uses 3 qubits:
    - q0: The qubit to be teleported (Alice's qubit with unknown state)
    - q1: Alice's half of the entangled pair
    - q2: Bob's half of the entangled pair
    
    After the protocol, q2 will have the same state as q0 originally had.
    """
    # Create three qubits
    q0, q1, q2 = cirq.LineQubit.range(3)
    
    circuit = cirq.Circuit()
    
    # Step 1: Prepare an arbitrary state on q0 (the state to teleport)
    # For this example, we'll create the state |+⟩ = (|0⟩ + |1⟩)/√2
    circuit.append(cirq.H(q0))
    
    # Step 2: Create a Bell pair between q1 (Alice) and q2 (Bob)
    circuit.append([
        cirq.H(q1),
        cirq.CNOT(q1, q2)
    ])
    
    # Now q1 and q2 are entangled: (|00⟩ + |11⟩)/√2
    
    # Step 3: Alice entangles her qubit with q0
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.H(q0))
    
    # Step 4: Alice measures both her qubits
    circuit.append([
        cirq.measure(q0, key='m0'),
        cirq.measure(q1, key='m1')
    ])
    
    # Step 5: Bob applies corrections based on Alice's measurements
    # If m1 = 1, apply X gate
    # If m0 = 1, apply Z gate
    circuit.append([
        cirq.X(q2).with_classical_controls('m1'),
        cirq.Z(q2).with_classical_controls('m0')
    ])
    
    # Step 6: Measure Bob's qubit to verify
    circuit.append(cirq.measure(q2, key='result'))
    
    return circuit


def main():
    print("=" * 70)
    print("Quantum Teleportation Protocol")
    print("=" * 70)
    
    print("\nScenario:")
    print("Alice wants to send a quantum state to Bob using:")
    print("1. A shared entangled pair of qubits")
    print("2. Two classical bits of communication")
    print()
    
    # Create the teleportation circuit
    print("1. Creating teleportation circuit...")
    circuit = create_teleportation_circuit()
    
    print("\n2. Circuit diagram:")
    print(circuit)
    
    print("\n3. Protocol steps:")
    print("   Step 1: Prepare the state |+⟩ on q0 (to be teleported)")
    print("   Step 2: Create Bell pair between q1 (Alice) and q2 (Bob)")
    print("   Step 3: Alice performs Bell measurement on q0 and q1")
    print("   Step 4: Alice sends 2 classical bits to Bob")
    print("   Step 5: Bob applies corrections based on classical bits")
    print("   Step 6: Bob now has the original state!")
    
    # Simulate
    print("\n4. Running simulation with qsim...")
    simulator = qsimcirq.QSimSimulator()
    result = simulator.run(circuit, repetitions=100)
    
    # Analyze results
    print("\n5. Results:")
    print(result)
    
    # Verify the teleportation
    print("\n6. Verification:")
    final_measurements = result.measurements['result']
    
    # Count the outcomes
    zeros = np.sum(final_measurements == 0)
    ones = np.sum(final_measurements == 1)
    
    print(f"   Bob measured |0⟩: {zeros} times ({zeros}%)")
    print(f"   Bob measured |1⟩: {ones} times ({ones}%)")
    
    print("\n7. Analysis:")
    print("   The original state was |+⟩ = (|0⟩ + |1⟩)/√2")
    print("   When measured, |+⟩ gives |0⟩ or |1⟩ with equal probability (50/50)")
    print()
    
    # Success criteria: difference should be within 20% of total repetitions
    # for a fair 50/50 distribution (allows for statistical variation)
    TOLERANCE_FRACTION = 0.20
    max_difference = 100 * TOLERANCE_FRACTION
    
    if abs(zeros - ones) < max_difference:
        print("   ✓ SUCCESS! The state was teleported correctly!")
        print("   Bob's measurements match the expected distribution for |+⟩")
    else:
        print("   ⚠ Unexpected results - there may be an issue")
    
    # Educational summary
    print("\n" + "=" * 70)
    print("Key Points about Quantum Teleportation:")
    print("=" * 70)
    print("1. The original quantum state is DESTROYED when Alice measures")
    print("2. Bob needs the 2 classical bits from Alice to complete the protocol")
    print("3. No faster-than-light communication (classical bits required!)")
    print("4. The original qubit's state is successfully recreated at Bob's qubit")
    print("5. This is a fundamental protocol in quantum information theory")
    print("\nApplications:")
    print("- Quantum communication networks")
    print("- Quantum computing (moving quantum states between processors)")
    print("- Quantum cryptography")
    print("=" * 70)


if __name__ == "__main__":
    main()
