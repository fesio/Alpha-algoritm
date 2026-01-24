# AlphaAgent - GitHub Copilot Custom Agent

The AlphaAgent is now configured as a GitHub Copilot custom agent.

## Location

The agent configuration is at:

```
.github/agents/alpha-agent.agent.md
```

## How to Use

### In GitHub Copilot Chat

1. **Invoke directly:**
   ```
   @alpha-agent How do I optimize a 2-qubit parameterized circuit?
   ```

2. **Auto-activation:**
   - The agent automatically activates when working with quantum circuits
   - Enabled via `infer: true` in the agent configuration

### Example Questions

Ask the alpha-agent:
- "How do I set up an objective function for circuit optimization?"
- "What learning rate should I use for my VQE optimization?"
- "Help me debug why my optimization isn't converging"
- "Show me how to optimize multiple parameters in a quantum circuit"
- "What's the best way to tune AlphaAgentOptions for my problem?"

## Agent Capabilities

The `@alpha-agent` specializes in:
- ✓ Quantum circuit parameter optimization
- ✓ AlphaAgent API guidance and code examples
- ✓ Objective function design and debugging
- ✓ Performance tuning (learning rate, convergence, etc.)
- ✓ Troubleshooting optimization problems
- ✓ Best practices for variational quantum algorithms

## Requirements

To use the AlphaAgent code:
```bash
pip install qsimcirq
```

The GitHub Copilot agent is automatically available when working in this repository.

## Documentation

- **Agent Config**: `.github/agents/alpha-agent.agent.md`
- **API Docs**: `docs/alpha_agent.md`
- **Examples**: `docs/examples/alpha_agent_example.py`
- **Implementation**: `qsimcirq/alpha_agent.py`
- **Tests**: `qsimcirq_tests/alpha_agent_test.py`

## Quick Start

```python
import qsimcirq
import cirq
import sympy

# Create the agent
agent = qsimcirq.AlphaAgent(
    qsimcirq.AlphaAgentOptions(optimization_steps=50)
)

# Define a parameterized circuit
q0 = cirq.LineQubit(0)
theta = sympy.Symbol('theta')
circuit = cirq.Circuit(cirq.X(q0) ** theta)

# Define objective (higher is better)
def objective(circuit, params):
    return -abs(params[0] - 1.5)  # Find params close to 1.5

# Optimize
params, score = agent.optimize(circuit, objective)
```

For help, ask `@alpha-agent` in GitHub Copilot!
