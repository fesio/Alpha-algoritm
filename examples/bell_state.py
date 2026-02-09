#!/usr/bin/env python3
"""
Bell State Example
==================

This example demonstrates how to create a Bell state, one of the most famous
quantum states that exhibits quantum entanglement.

A Bell state is a maximally entangled state of two qubits. When you measure
one qubit, you instantly know the state of the other qubit, even though they
are in a superposition before measurement.

What this example covers:
- Creating entangled quantum states
- Understanding quantum correlations
- Verifying entanglement through measurements
"""

import cirq
import qsimcirq
from collections import Counter


def create_bell_state():
    """Create a Bell state circuit."""
    # Create two qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create the Bell state: (|00⟩ + |11⟩)/√2
    circuit = cirq.Circuit(
        cirq.H(q0),           # Put q0 in superposition: (|0⟩ + |1⟩)/√2
        cirq.CNOT(q0, q1),    # Entangle q0 and q1
        cirq.measure(q0, q1, key='result')
    )
    
    return circuit


def main():
    print("=" * 60)
    print("Bell State Example - Quantum Entanglement")
    print("=" * 60)
    
    # Step 1: Create the Bell state circuit
    print("\n1. Creating Bell state circuit...")
    circuit = create_bell_state()
    
    print("\n2. Circuit diagram:")
    print(circuit)
    
    print("\n3. Understanding the Bell state:")
    print("   - Start with |00⟩ (both qubits in state 0)")
    print("   - Apply H to q0 → (|0⟩ + |1⟩)/√2 ⊗ |0⟩")
    print("   - Apply CNOT → (|00⟩ + |11⟩)/√2")
    print("   - This is a Bell state (maximally entangled)!")
    
    # Step 2: Simulate
    print("\n4. Running simulation with qsim...")
    simulator = qsimcirq.QSimSimulator()
    result = simulator.run(circuit, repetitions=1000)
    
    # Step 3: Analyze results
    print("\n5. Results (1000 measurements):")
    measurements = result.measurements['result']
    counts = Counter(tuple(row) for row in measurements)
    
    print("\n   Measurement outcomes:")
    for outcome, count in sorted(counts.items()):
        percentage = (count / 1000) * 100
        bar = '█' * int(percentage / 2)  # Visual bar
        print(f"   |{outcome[0]}{outcome[1]}⟩: {count:4d} times ({percentage:5.1f}%) {bar}")
    
    # Step 4: Verify entanglement
    print("\n6. Entanglement verification:")
    print("   Expected: ~50% |00⟩ and ~50% |11⟩")
    print("   Expected: ~0% |01⟩ and ~0% |10⟩")
    print()
    
    # Check if results match expectations
    count_00 = counts.get((0, 0), 0)
    count_11 = counts.get((1, 1), 0)
    count_01 = counts.get((0, 1), 0)
    count_10 = counts.get((1, 0), 0)
    
    total_correlated = count_00 + count_11
    total_uncorrelated = count_01 + count_10
    
    print(f"   Correlated outcomes (|00⟩ + |11⟩): {total_correlated} ({total_correlated/10:.1f}%)")
    print(f"   Uncorrelated outcomes (|01⟩ + |10⟩): {total_uncorrelated} ({total_uncorrelated/10:.1f}%)")
    
    # Success threshold: 95% correlation (allows for small statistical variations)
    CORRELATION_THRESHOLD = 0.95
    success_threshold = 1000 * CORRELATION_THRESHOLD
    
    if total_correlated > success_threshold:
        print("\n   ✓ SUCCESS! The qubits are entangled!")
        print("   Notice: Both qubits always have the same value (both 0 or both 1)")
    else:
        print("\n   ⚠ Unexpected results - check your setup")
    
    print("\n" + "=" * 60)
    print("What is entanglement?")
    print("=" * 60)
    print("When qubits are entangled:")
    print("- They are in superposition before measurement")
    print("- Measuring one instantly determines the other")
    print("- They always show correlated results")
    print("- This correlation exists no matter how far apart they are!")
    print("\nThis is one of the most fascinating aspects of quantum mechanics!")
    print("=" * 60)


if __name__ == "__main__":
    main()
