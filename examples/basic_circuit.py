#!/usr/bin/env python3
"""
Basic Quantum Circuit Example
==============================

This example demonstrates the basics of creating and simulating a quantum circuit
using qsim. It's perfect for beginners who are just getting started with quantum
computing.

What this example covers:
- Creating qubits
- Applying basic quantum gates (X, H, CNOT)
- Running simulations
- Measuring results
"""

import cirq
import qsimcirq


def main():
    print("=" * 60)
    print("Basic Quantum Circuit Example")
    print("=" * 60)
    
    # Step 1: Create qubits
    # In quantum computing, qubits are the basic units of information
    print("\n1. Creating qubits...")
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    print(f"   Created qubits: {q0}, {q1}")
    
    # Step 2: Build a quantum circuit
    print("\n2. Building quantum circuit...")
    circuit = cirq.Circuit()
    
    # Add gates to the circuit
    # X gate: Quantum NOT gate (flips |0⟩ to |1⟩ and vice versa)
    circuit.append(cirq.X(q0))
    print("   - Applied X gate to q0 (NOT gate)")
    
    # H gate: Hadamard gate (creates superposition)
    circuit.append(cirq.H(q1))
    print("   - Applied H gate to q1 (creates superposition)")
    
    # CNOT gate: Controlled-NOT gate
    circuit.append(cirq.CNOT(q0, q1))
    print("   - Applied CNOT gate (q0 controls q1)")
    
    # Measure the qubits
    circuit.append(cirq.measure(q0, q1, key='result'))
    print("   - Added measurement")
    
    # Step 3: Display the circuit
    print("\n3. Circuit diagram:")
    print(circuit)
    
    # Step 4: Create a simulator
    print("\n4. Creating qsim simulator...")
    simulator = qsimcirq.QSimSimulator()
    print("   Simulator created successfully!")
    
    # Step 5: Run the simulation
    print("\n5. Running simulation (100 repetitions)...")
    result = simulator.run(circuit, repetitions=100)
    
    # Step 6: Display results
    print("\n6. Results:")
    print(result)
    
    # Analyze the results
    print("\n7. Analysis:")
    measurements = result.measurements['result']
    
    # Count occurrences of each outcome
    from collections import Counter
    counts = Counter(tuple(row) for row in measurements)
    
    print("   Measurement outcomes:")
    for outcome, count in sorted(counts.items()):
        percentage = (count / 100) * 100
        print(f"   |{outcome[0]}{outcome[1]}⟩: {count} times ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    
    # Educational note
    print("\nWhat happened?")
    print("- q0 started in |0⟩, then X gate flipped it to |1⟩")
    print("- q1 started in |0⟩, then H gate created superposition")
    print("- CNOT flipped q1 because q0 was |1⟩")
    print("- Final state should be mostly |10⟩ (q0=1, q1=0)")


if __name__ == "__main__":
    main()
