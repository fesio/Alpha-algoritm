# AlphaAgent - Quantum Circuit Parameter Optimizer

## Description

AlphaAgent is an optimization tool for parameterized quantum circuits that uses an alpha-based search algorithm inspired by alpha-beta pruning from game theory. It efficiently explores the parameter space to find optimal gate parameters based on custom objective functions.

## Capabilities

- **Parameter Optimization**: Optimize single or multiple parameters in quantum circuits
- **Alpha Bound Tracking**: Maintains lower bound on solution quality for efficient search
- **Convergence Detection**: Automatically stops when improvements plateau
- **History Tracking**: Records optimization progress for analysis
- **Circuit Evaluation**: Provides quality metrics for quantum circuits

## Use Cases

1. **Variational Quantum Algorithms**: Optimize parameters in VQE, QAOA, and similar algorithms
2. **Gate Calibration**: Fine-tune rotation angles and phase parameters
3. **Circuit Synthesis**: Find optimal parameter values for quantum circuit compilation
4. **Quantum Machine Learning**: Tune parameters in quantum neural networks

## Installation

The AlphaAgent is part of the qsimcirq package:

```bash
pip install qsimcirq
```

## Quick Start

```python
import cirq
import sympy
import qsimcirq
import numpy as np

# Create the agent
agent = qsimcirq.AlphaAgent(
    qsimcirq.AlphaAgentOptions(
        optimization_steps=50,
        learning_rate=0.05
    )
)

# Define a parameterized circuit
q0 = cirq.LineQubit(0)
theta = sympy.Symbol('theta')
circuit = cirq.Circuit(cirq.X(q0) ** theta)

# Define objective function (higher score is better)
def objective_fn(circuit, params):
    target = np.pi / 2
    return -abs(params[0] - target)

# Optimize
optimized_params, best_score = agent.optimize(circuit, objective_fn)
print(f"Optimized: {optimized_params}, Score: {best_score}")
```

## Configuration

### AlphaAgentOptions

Configure the agent's behavior:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_depth` | int | 5 | Maximum depth for search algorithm |
| `alpha_init` | float | -∞ | Initial alpha value |
| `beta_init` | float | +∞ | Initial beta value |
| `optimization_steps` | int | 100 | Maximum optimization iterations |
| `learning_rate` | float | 0.01 | Step size for parameter perturbations |
| `convergence_threshold` | float | 1e-6 | Threshold for early stopping |

### Example Configuration

```python
options = qsimcirq.AlphaAgentOptions(
    optimization_steps=200,
    learning_rate=0.1,
    convergence_threshold=1e-4
)
agent = qsimcirq.AlphaAgent(options)
```

## API Reference

### AlphaAgent Class

**Methods:**

#### `optimize(circuit, objective_fn, initial_params=None)`

Optimize circuit parameters using alpha-based search.

**Parameters:**
- `circuit` (cirq.Circuit): The quantum circuit to optimize
- `objective_fn` (Callable): Function that takes (circuit, params) and returns a score (higher is better)
- `initial_params` (Optional[np.ndarray]): Starting parameters (random if None)

**Returns:**
- `Tuple[np.ndarray, float]`: (optimized_parameters, best_score)

**Example:**
```python
params, score = agent.optimize(circuit, objective_fn)
```

#### `evaluate_circuit(circuit, params)`

Evaluate circuit quality metric.

**Parameters:**
- `circuit` (cirq.Circuit): The quantum circuit to evaluate
- `params` (np.ndarray): Circuit parameters

**Returns:**
- `float`: Quality score

#### `get_optimization_history()`

Get the history of optimization steps.

**Returns:**
- `List[Dict[str, Any]]`: List of step records with 'step', 'score', and 'params'

#### `reset()`

Reset the agent's optimization history.

## Examples

### Single Parameter Optimization

```python
import cirq
import sympy
import qsimcirq

agent = qsimcirq.AlphaAgent()
q0 = cirq.LineQubit(0)
theta = sympy.Symbol('theta')
circuit = cirq.Circuit(cirq.X(q0) ** theta)

# Optimize theta to be close to π/4
def objective(circuit, params):
    import numpy as np
    return -abs(params[0] - np.pi/4)

params, score = agent.optimize(circuit, objective)
```

### Multi-Parameter Optimization

```python
q0, q1 = cirq.LineQubit.range(2)
theta, phi = sympy.Symbol('theta'), sympy.Symbol('phi')

circuit = cirq.Circuit(
    cirq.X(q0) ** theta,
    cirq.Y(q1) ** phi,
    cirq.CNOT(q0, q1)
)

# Minimize sum of squared parameters
def objective(circuit, params):
    return -(params[0]**2 + params[1]**2)

agent = qsimcirq.AlphaAgent(
    qsimcirq.AlphaAgentOptions(optimization_steps=100)
)
params, score = agent.optimize(circuit, objective)
```

### Using Optimization History

```python
agent.optimize(circuit, objective_fn)
history = agent.get_optimization_history()

# Analyze optimization progress
for step in history:
    print(f"Step {step['step']}: score={step['score']:.4f}")

# Reset for new optimization
agent.reset()
```

## Algorithm Details

The AlphaAgent uses a greedy search strategy with alpha bounds:

1. **Initialization**: Parameters are randomly initialized (uniform [0, 2π])
2. **Exploration**: Each iteration perturbs parameters by small random deltas
3. **Alpha Tracking**: Maintains alpha lower bound representing best score found
4. **Greedy Update**: Accepts parameters that improve the objective
5. **Convergence**: Stops when score improvement falls below threshold

The algorithm is inspired by alpha-beta pruning but adapted for continuous parameter optimization rather than discrete game trees.

## Performance Tips

- **Learning Rate**: Use smaller values (0.01-0.05) for fine-tuning, larger (0.1-0.2) for exploration
- **Optimization Steps**: Start with 50-100, increase if not converging
- **Convergence Threshold**: Set based on objective function scale (1e-3 to 1e-6)
- **Initial Parameters**: Provide good initial guess when possible to speed convergence

## Limitations

- **Local Optimization**: May converge to local optima; try multiple runs with different seeds
- **Random Search**: Uses stochastic perturbations; results may vary between runs
- **No Gradient**: Doesn't use gradient information; consider gradient-based methods for smooth objectives

## Integration with Cirq

AlphaAgent works seamlessly with Cirq circuits and operations:

```python
# Compatible with all parameterized Cirq gates
circuit = cirq.Circuit(
    cirq.rx(theta).on(q0),
    cirq.ry(phi).on(q1),
    cirq.FSimGate(theta=alpha, phi=beta).on(q0, q1)
)

# Works with circuit operations
circuit = cirq.Circuit(
    cirq.PhasedXPowGate(phase_exponent=theta).on(q0)
)
```

## Testing

Run the test suite:

```bash
python -m pytest qsimcirq_tests/alpha_agent_test.py -v
```

All tests should pass (9/9 tests).

## Documentation

- **Full API Documentation**: `docs/alpha_agent.md`
- **Examples**: `docs/examples/alpha_agent_example.py`
- **Implementation**: `qsimcirq/alpha_agent.py`

## Support

For issues, questions, or contributions related to AlphaAgent:

1. Check the documentation in `docs/alpha_agent.md`
2. Run the examples in `docs/examples/`
3. Review test cases in `qsimcirq_tests/alpha_agent_test.py`
4. Open an issue on the repository

## Version History

- **v0.23.0.dev0**: Initial implementation
  - Core optimization algorithm
  - History tracking
  - Circuit evaluation
  - Comprehensive tests
  - Full documentation

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.

---

**Author**: AlphaAgent development team
**Repository**: [qsim - Quantum Circuit Simulator](https://github.com/quantumlib/qsim)
**Package**: qsimcirq
