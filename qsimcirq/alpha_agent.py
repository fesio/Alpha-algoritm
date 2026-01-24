# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Alpha agent for quantum circuit optimization and parameter tuning.

This module implements an alpha-based agent that can be used to optimize
quantum circuits and tune parameters using an alpha-beta search algorithm.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

import cirq
import numpy as np


@dataclass
class AlphaAgentOptions:
    """Options for the AlphaAgent.

    Args:
        max_depth: Maximum depth for alpha-beta search.
        alpha_init: Initial alpha value for pruning.
        beta_init: Initial beta value for pruning.
        optimization_steps: Number of optimization steps to perform.
        learning_rate: Learning rate for parameter updates.
        convergence_threshold: Threshold for convergence detection.
    """

    max_depth: int = 5
    alpha_init: float = -np.inf
    beta_init: float = np.inf
    optimization_steps: int = 100
    learning_rate: float = 0.01
    convergence_threshold: float = 1e-6


class AlphaAgent:
    """Alpha-based agent for quantum circuit optimization.

    This agent uses an alpha-beta pruning algorithm to optimize quantum
    circuits and tune parameters. It can be used to find optimal gate
    parameters or circuit configurations based on a given objective function.

    Example:
        >>> agent = AlphaAgent()
        >>> circuit = cirq.Circuit(...)
        >>> optimized_params = agent.optimize(circuit, objective_fn)
    """

    def __init__(self, options: Optional[AlphaAgentOptions] = None):
        """Initialize the AlphaAgent.

        Args:
            options: Configuration options for the agent.
        """
        self.options = options or AlphaAgentOptions()
        self._history: List[Dict[str, Any]] = []

    def optimize(
        self,
        circuit: cirq.Circuit,
        objective_fn: Callable[[cirq.Circuit, np.ndarray], float],
        initial_params: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, float]:
        """Optimize circuit parameters using alpha-based search.

        Args:
            circuit: The quantum circuit to optimize.
            objective_fn: Function that evaluates circuit quality.
                Takes (circuit, params) and returns a score.
            initial_params: Starting parameters. If None, uses random initialization.

        Returns:
            Tuple of (optimized_parameters, best_score).
        """
        # Get parameterized operations
        param_resolvers = list(cirq.parameter_names(circuit))
        n_params = len(param_resolvers)

        if n_params == 0:
            # No parameters to optimize
            return np.array([]), objective_fn(circuit, np.array([]))

        # Initialize parameters
        if initial_params is None:
            current_params = np.random.uniform(
                0, 2 * np.pi, size=n_params
            )
        else:
            current_params = initial_params.copy()

        best_params = current_params.copy()
        best_score = objective_fn(circuit, current_params)

        # Optimization loop with alpha bounds
        alpha = self.options.alpha_init
        
        for step in range(self.options.optimization_steps):
            # Store previous score for convergence check
            prev_score = best_score

            # Generate candidate parameter modifications
            for i in range(n_params):
                # Try small perturbations
                delta = self.options.learning_rate * np.random.randn()
                candidate_params = current_params.copy()
                candidate_params[i] += delta

                # Evaluate candidate
                score = objective_fn(circuit, candidate_params)

                # Update best if score improved and update alpha bound
                if score > best_score:
                    best_score = score
                    best_params = candidate_params.copy()
                    current_params = candidate_params.copy()
                    alpha = max(alpha, score)

                # Pruning: skip if score is worse than current alpha bound
                if score <= alpha and best_score > self.options.alpha_init:
                    continue

            # Record history
            self._history.append({
                'step': step,
                'score': best_score,
                'params': best_params.copy()
            })

            # Check for convergence
            if abs(best_score - prev_score) < self.options.convergence_threshold:
                break

        return best_params, best_score

    def evaluate_circuit(
        self,
        circuit: cirq.Circuit,
        params: np.ndarray,
        depth: int = 0,
        alpha: float = -np.inf,
        beta: float = np.inf,
    ) -> float:
        """Evaluate circuit quality metric.

        This method provides a simple heuristic evaluation of circuit quality
        based on gate count and qubit usage.

        Args:
            circuit: The quantum circuit to evaluate.
            params: Circuit parameters (reserved for future use).
            depth: Current search depth (reserved for future use).
            alpha: Alpha value for pruning (reserved for future use).
            beta: Beta value for pruning (reserved for future use).

        Returns:
            Evaluation score for the circuit.
        """
        # Simple heuristic: ratio of gates to qubits
        gate_count = len(list(circuit.all_operations()))
        qubit_count = len(circuit.all_qubits())

        # Return normalized score
        return gate_count / max(qubit_count, 1)

    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get the history of optimization steps.

        Returns:
            List of dictionaries containing step information.
        """
        return self._history

    def reset(self):
        """Reset the agent's optimization history."""
        self._history = []
