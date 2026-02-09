# Quick Start Guide for qsim

Welcome! This guide will help you get started with qsim, a high-performance quantum circuit simulator.

## What is qsim?

qsim is a state-vector simulator for quantum circuits. It helps you:
- Simulate quantum circuits with high performance
- Test quantum algorithms before running them on real quantum hardware
- Learn about quantum computing through experimentation

## Installation

### Step 1: Install Python
Make sure you have Python 3.10 or higher installed. Check your version:
```bash
python3 --version
```

### Step 2: Install qsimcirq
The easiest way to get started is to install qsimcirq via pip:

```bash
pip3 install qsimcirq
```

This will install qsimcirq along with Cirq, Google's quantum computing framework.

## Your First Quantum Circuit

Here's a simple example to get you started. This creates a basic quantum circuit and simulates it:

```python
import cirq
import qsimcirq

# Create a simple quantum circuit with 2 qubits
q0, q1 = cirq.LineQubit.range(2)

# Build a circuit
circuit = cirq.Circuit(
    cirq.H(q0),           # Hadamard gate on qubit 0
    cirq.CNOT(q0, q1),    # CNOT gate
    cirq.measure(q0, q1, key='result')  # Measure both qubits
)

print("Circuit:")
print(circuit)

# Create a qsim simulator
simulator = qsimcirq.QSimSimulator()

# Run the simulation
result = simulator.run(circuit, repetitions=10)

print("\nResults:")
print(result)
```

## What's Next?

### Learn More Examples
Check out the `examples/` directory for more comprehensive examples:
- **bell_state.py**: Creating entangled Bell states
- **basic_circuit.py**: Understanding quantum gates
- **quantum_teleportation.py**: Advanced quantum protocol

### Explore Documentation
- **README.md**: Project overview and features
- **docs/usage.md**: Detailed usage instructions
- **docs/cirq_interface.md**: Working with Cirq
- **docs/tutorials/**: Interactive Jupyter notebooks

### Advanced Usage

#### Using GPU Acceleration
If you have a CUDA-capable GPU, qsim will automatically detect and use it for better performance.

#### Simulating Larger Circuits
For circuits with many qubits, you can adjust simulation parameters:

```python
simulator = qsimcirq.QSimSimulator(
    qsim_options=qsimcirq.QSimOptions(
        max_fused_gate_size=4,  # Control gate fusion
        cpu_threads=8           # Number of CPU threads
    )
)
```

## Getting Help

- **Documentation**: https://quantumai.google/qsim
- **Issues**: Report bugs or ask questions on GitHub
- **Email**: quantum-oss-maintainers@google.com

## Common Issues

### Import Error
If you get an import error, make sure qsimcirq is installed:
```bash
pip3 install --upgrade qsimcirq
```

### Performance Issues
For large circuits, consider:
- Using GPU acceleration (if available)
- Adjusting the number of CPU threads
- Using the qsimh (hybrid) simulator for very large circuits

## Next Steps

1. Try running the example above
2. Modify it to experiment with different quantum gates
3. Explore the examples in the `examples/` directory
4. Read the tutorials to learn advanced techniques

Happy quantum computing! 🎯
