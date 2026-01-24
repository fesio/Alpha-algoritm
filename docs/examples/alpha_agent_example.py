#!/usr/bin/env python3
"""
Example demonstrating the AlphaAgent for quantum circuit optimization.

This script shows how to use the AlphaAgent to optimize parameters of a
parameterized quantum circuit.
"""

import cirq
import numpy as np
import sympy
import qsimcirq


def example_single_parameter():
    """Example: Optimize a single-parameter circuit."""
    print("=" * 60)
    print("Example 1: Single Parameter Optimization")
    print("=" * 60)
    
    # Create agent
    agent = qsimcirq.AlphaAgent(
        qsimcirq.AlphaAgentOptions(
            optimization_steps=50,
            learning_rate=0.05,
        )
    )
    
    # Create a parameterized circuit
    q0 = cirq.LineQubit(0)
    theta = sympy.Symbol('theta')
    circuit = cirq.Circuit(
        cirq.X(q0) ** theta,
        cirq.measure(q0, key='result')
    )
    
    print(f"\nCircuit:\n{circuit}")
    
    # Define objective: find theta closest to π/2
    target = np.pi / 2
    
    def objective_fn(circuit, params):
        # Return negative distance (we maximize)
        return -abs(params[0] - target)
    
    # Optimize
    print(f"\nTarget parameter value: {target:.4f}")
    print("Optimizing...")
    
    optimized_params, best_score = agent.optimize(circuit, objective_fn)
    
    print(f"\nOptimized parameter: {optimized_params[0]:.4f}")
    print(f"Target value: {target:.4f}")
    print(f"Difference: {abs(optimized_params[0] - target):.4f}")
    print(f"Best score: {best_score:.4f}")
    
    # Show optimization history
    history = agent.get_optimization_history()
    print(f"\nOptimization converged in {len(history)} steps")
    
    return optimized_params, best_score


def example_multi_parameter():
    """Example: Optimize a multi-parameter circuit."""
    print("\n" + "=" * 60)
    print("Example 2: Multi-Parameter Optimization")
    print("=" * 60)
    
    # Create agent
    agent = qsimcirq.AlphaAgent(
        qsimcirq.AlphaAgentOptions(
            optimization_steps=100,
            learning_rate=0.1,
            convergence_threshold=1e-4,
        )
    )
    
    # Create a two-qubit parameterized circuit
    q0, q1 = cirq.LineQubit.range(2)
    theta, phi = sympy.Symbol('theta'), sympy.Symbol('phi')
    
    circuit = cirq.Circuit(
        cirq.X(q0) ** theta,
        cirq.Y(q1) ** phi,
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    
    print(f"\nCircuit:\n{circuit}")
    
    # Define objective: minimize sum of squared parameters
    def objective_fn(circuit, params):
        # We want parameters close to zero
        return -(params[0]**2 + params[1]**2)
    
    # Optimize
    print("\nObjective: Minimize sum of squared parameters")
    print("Optimizing...")
    
    optimized_params, best_score = agent.optimize(circuit, objective_fn)
    
    print(f"\nOptimized parameters: theta={optimized_params[0]:.4f}, phi={optimized_params[1]:.4f}")
    print(f"Sum of squares: {optimized_params[0]**2 + optimized_params[1]**2:.4f}")
    print(f"Best score: {best_score:.4f}")
    
    # Show optimization history
    history = agent.get_optimization_history()
    print(f"\nOptimization history ({len(history)} steps):")
    for i, step in enumerate(history[:5]):  # Show first 5 steps
        params = step['params']
        print(f"  Step {step['step']}: theta={params[0]:.4f}, phi={params[1]:.4f}, score={step['score']:.4f}")
    if len(history) > 5:
        print("  ...")
        step = history[-1]
        params = step['params']
        print(f"  Step {step['step']}: theta={params[0]:.4f}, phi={params[1]:.4f}, score={step['score']:.4f}")
    
    return optimized_params, best_score


def example_circuit_evaluation():
    """Example: Evaluate circuit quality."""
    print("\n" + "=" * 60)
    print("Example 3: Circuit Evaluation")
    print("=" * 60)
    
    agent = qsimcirq.AlphaAgent()
    
    # Create a few different circuits
    circuits = {
        "Simple": cirq.Circuit(
            cirq.X(cirq.LineQubit(0)),
        ),
        "Medium": cirq.Circuit(
            cirq.X(cirq.LineQubit(0)),
            cirq.Y(cirq.LineQubit(1)),
            cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)),
        ),
        "Complex": cirq.Circuit(
            cirq.X(cirq.LineQubit(0)),
            cirq.Y(cirq.LineQubit(1)),
            cirq.Z(cirq.LineQubit(2)),
            cirq.CNOT(cirq.LineQubit(0), cirq.LineQubit(1)),
            cirq.CNOT(cirq.LineQubit(1), cirq.LineQubit(2)),
        ),
    }
    
    print("\nEvaluating circuit quality metrics:")
    for name, circuit in circuits.items():
        score = agent.evaluate_circuit(circuit, np.array([]))
        gate_count = len(list(circuit.all_operations()))
        qubit_count = len(circuit.all_qubits())
        print(f"\n{name} circuit:")
        print(f"  Gates: {gate_count}, Qubits: {qubit_count}")
        print(f"  Quality score: {score:.4f}")


if __name__ == "__main__":
    print("\nAlphaAgent Examples for Quantum Circuit Optimization\n")
    
    # Run examples
    example_single_parameter()
    example_multi_parameter()
    example_circuit_evaluation()
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
