# AlphaAgent

The `AlphaAgent` is a quantum circuit optimization tool that uses an alpha-beta search algorithm to optimize quantum circuit parameters.

## Overview

The AlphaAgent implements an optimization strategy inspired by alpha-beta pruning algorithms commonly used in game theory and search problems. It can be used to:

- Optimize parameterized quantum circuits
- Tune gate parameters based on custom objective functions
- Explore the parameter space efficiently using alpha-beta bounds

## Usage

### Basic Example

```python
import cirq
import sympy
import qsimcirq
import numpy as np

# Create an agent with default options
agent = qsimcirq.AlphaAgent()

# Create a parameterized circuit
q0 = cirq.LineQubit(0)
theta = sympy.Symbol('theta')
circuit = cirq.Circuit(cirq.X(q0) ** theta)

# Define an objective function
def objective_fn(circuit, params):
    # Return a score (higher is better)
    # This example minimizes distance from a target value
    target = 0.5
    return -abs(params[0] - target)

# Optimize the circuit
optimized_params, best_score = agent.optimize(circuit, objective_fn)
print(f"Optimized parameters: {optimized_params}")
print(f"Best score: {best_score}")
```

### Custom Options

You can customize the agent's behavior using `AlphaAgentOptions`:

```python
options = qsimcirq.AlphaAgentOptions(
    max_depth=10,                    # Maximum search depth
    optimization_steps=100,           # Number of optimization iterations
    learning_rate=0.01,              # Learning rate for parameter updates
    convergence_threshold=1e-6,      # Threshold for early stopping
    alpha_init=-np.inf,              # Initial alpha value
    beta_init=np.inf                 # Initial beta value
)

agent = qsimcirq.AlphaAgent(options)
```

### Monitoring Optimization Progress

The agent keeps track of optimization history:

```python
# Run optimization
agent.optimize(circuit, objective_fn)

# Get optimization history
history = agent.get_optimization_history()
for step in history:
    print(f"Step {step['step']}: score={step['score']}")

# Reset history for a new optimization
agent.reset()
```

## API Reference

### AlphaAgent

Main class for alpha-based quantum circuit optimization.

**Methods:**

- `__init__(options: Optional[AlphaAgentOptions] = None)`: Initialize the agent
- `optimize(circuit, objective_fn, initial_params=None)`: Optimize circuit parameters
  - `circuit`: cirq.Circuit - The quantum circuit to optimize
  - `objective_fn`: Callable - Function that takes (circuit, params) and returns a score
  - `initial_params`: Optional[np.ndarray] - Starting parameters (random if None)
  - Returns: Tuple[np.ndarray, float] - (optimized_parameters, best_score)

- `evaluate_circuit(circuit, params, depth=0, alpha=-inf, beta=inf)`: Evaluate circuit using alpha-beta search
- `get_optimization_history()`: Get the list of optimization steps
- `reset()`: Reset the optimization history

### AlphaAgentOptions

Configuration options for the AlphaAgent.

**Attributes:**

- `max_depth` (int): Maximum depth for alpha-beta search (default: 5)
- `alpha_init` (float): Initial alpha value for pruning (default: -∞)
- `beta_init` (float): Initial beta value for pruning (default: +∞)
- `optimization_steps` (int): Number of optimization steps (default: 100)
- `learning_rate` (float): Learning rate for parameter updates (default: 0.01)
- `convergence_threshold` (float): Threshold for convergence detection (default: 1e-6)

## Algorithm Details

The AlphaAgent uses an optimization approach with alpha bounds:

1. **Initialization**: Parameters are randomly initialized if not provided
2. **Exploration**: Each optimization step explores the parameter space by trying small perturbations
3. **Alpha Bound**: Maintains an alpha lower bound that increases with better solutions
4. **Greedy Update**: Parameters are updated when a better solution is found
5. **Convergence**: Optimization stops when convergence threshold is reached or max steps exceeded

The algorithm uses the alpha bound to track the best solution found so far, inspired by alpha-beta pruning concepts from game theory.

## Examples

### Multi-Parameter Optimization

```python
q0, q1 = cirq.LineQubit.range(2)
theta, phi = sympy.Symbol('theta'), sympy.Symbol('phi')

circuit = cirq.Circuit(
    cirq.X(q0) ** theta,
    cirq.Y(q1) ** phi,
)

def objective_fn(circuit, params):
    # Custom objective based on parameter values
    return -(params[0]**2 + params[1]**2)

agent = qsimcirq.AlphaAgent()
params, score = agent.optimize(circuit, objective_fn)
```

### Circuit Evaluation

```python
# Evaluate a circuit without optimization
agent = qsimcirq.AlphaAgent()
circuit = cirq.Circuit(
    cirq.X(cirq.LineQubit(0)),
    cirq.Y(cirq.LineQubit(1)),
)
score = agent.evaluate_circuit(circuit, np.array([]))
```

## Notes

- The agent is designed for circuits with parameterized gates
- The objective function should return higher scores for better parameter configurations
- Alpha-beta pruning helps avoid exploring unpromising parameter regions
- Convergence detection helps stop optimization early when improvements plateau
