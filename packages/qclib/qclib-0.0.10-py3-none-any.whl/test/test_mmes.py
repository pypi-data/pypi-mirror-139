# Copyright 2021 qclib project.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests for the mmes.py module.
"""

from unittest import TestCase
from itertools import combinations
from math import factorial
import numpy as np
import qutip
from qclib.state_preparation.util.mmes import create_state

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

class TestMmes(TestCase):
    def _nCr(self, n,r):
        # pylint: disable=invalid-name
        return factorial(n) // factorial(r) // factorial(n-r)

    def test_state_creation(self):
        for n_qubits in range(5, 6):
            state = create_state(n_qubits)
            #                                10                     20                        30
            #        0,1,2,3,4, 5, 6,7,8, 9, 0, 1,2,3,4,5,6,7, 8, 9,0, 1,2, 3, 4,5, 6,7, 8, 9,0,1
            #state = [0,0,0,0,0, 1,-1,0,1, 0, 0,-1,0,0,0,0,0,1, 1, 0,0, 0,0, 0, 1,0, 0,0, 0, 0,0,1 ]
            state = [1,1,1,1,1,-1,-1,1,1,-1,-1, 1,1,1,1,1,1,1,-1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,1,1]
            state = state/np.linalg.norm(state)

            print(state)
            ket = qutip.Qobj(state, dims=[[2] * (n_qubits), [1] * (n_qubits)]).unit()

            pi_a_sum = 0                    # sum of purity of the subsystems
            n_a = n_qubits//2
            combs = combinations(range(n_qubits), n_a)
            for subsystem_a in combs:
                rho_sq = ket.ptrace(subsystem_a)**2
                pi_a = rho_sq.tr()          # purity of subsystem_a
                pi_a_sum += pi_a
                print(subsystem_a)
                print(pi_a)
                self.assertTrue(1/2**n_a<=pi_a<=1)

            # potential of multipartite entanglement measures the average
            # bipartite entanglement over all possible balanced bipartition
            # 1/2^n_a <= pi_me <= 1.
            print('nCr', self._nCr(n_qubits, n_a))
            pi_me = ( 1/self._nCr(n_qubits, n_a) ) * pi_a_sum
            print('pi_a_sum', pi_a_sum)
            print('pi_me', pi_me)
            self.assertTrue(1/2**n_a<=pi_me<=1)
