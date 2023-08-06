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
Maximally multipartite entangled state (MMES).
https://journals.aps.org/pra/abstract/10.1103/PhysRevA.77.060304
https://link.springer.com/article/10.1007/s10773-018-3956-3
"""

from itertools import combinations
import numpy as np

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

def create_state(n_qubits):
    bell_phi_plus  = np.array([1, 0, 0, 1]).reshape((4, 1)) # 1/sqrt(2) (|00>+|11>)
    bell_phi_minus = np.array([1, 0, 0, -1]).reshape((4, 1)) # 1/sqrt(2) (|00>-|11>)
    #bell_psi_plus  = np.array([0, 1, 1, 0]).reshape((4, 1)) # 1/sqrt(2) (|01>+|10>)
    #bell_psi_minus  = np.array([0, -1, 1, 0]).reshape((4, 1)) # 1/sqrt(2) (-|01>+|10>)

    #psi = [bell_phi_plus, bell_psi_plus, bell_phi_minus, bell_psi_minus]
    #psi = [bell_phi_plus, bell_psi_minus, bell_psi_plus, bell_phi_minus]
    #psi = [bell_phi_plus, bell_psi_minus] # , bell_psi_plus, bell_phi_minus]
    psi = [bell_phi_plus, bell_phi_minus] # , bell_psi_plus, bell_phi_minus]

    return _create_state(n_qubits, psi) #, bell_psi_plus)
    #return _create_state(n_qubits, bell_phi_plus, bell_phi_minus, bell_psi_plus)

def _create_state(n_qubits, psi): #, psi2): #, psi3):
    #if not _ortho(psi):
    #    raise ValueError(
    #        "The state vectors do not satisfy the orthogonality condition."
    #    )

    previous_n = int(np.log2(psi[0].shape[0]))
    if previous_n == n_qubits:
        vector = psi[0].reshape(2**n_qubits)
        return vector/np.linalg.norm(vector)

    eye  = np.eye(2)
    zero = eye[:,[0]]
    one  = eye[:,[1]]

    #for qubit in range(previous_n):
    #    psi4 = _pauli_x(qubit, previous_n).dot(psi3)
    #    if _ortho(psi1, psi4) and _ortho(psi2, psi4) and _ortho(psi3, psi4):
    #        print('break')
    #        break
    #    if qubit > 0:
    #        psi4 = _pauli_z(qubit-1, previous_n).dot(psi4)
    #    if _ortho(psi1, psi4) and _ortho(psi2, psi4) and _ortho(psi3, psi4):
    #        print('break')
    #        break

    #signal = (-1)**previous_n
    new_psi = []
    for pair in combinations(psi, 2):
        #for signal in [(-1)**previous_n, (-1)**(previous_n+1)]:
        vector = np.kron(pair[0], zero) + np.kron(pair[1], one)
        if _ortho([*new_psi, vector]):
            new_psi.append(vector)
        vector = np.kron(pair[0], zero) - np.kron(pair[1], one)
        if _ortho([*new_psi, vector]):
            new_psi.append(vector)
        """
        vector = np.kron(pair[1], zero) + np.kron(pair[0], one)
        if _ortho([*new_psi, vector]):
            new_psi.append(vector)
        vector = np.kron(pair[1], zero) - np.kron(pair[0], one)
        if _ortho([*new_psi, vector]):
            new_psi.append(vector)
        """

    psi.clear()
    return _create_state(n_qubits, new_psi) # , new_psi2)

def _count(vector):
    return sum([abs(i) > 10**-15 for i in vector])

def _ortho(vectors):
    if len(vectors) == 1:
        return True
    for pair in combinations(vectors, 2):
        if np.abs(_braket(pair[0], pair[1])) > 10**-15:
            return False
    return True

def _braket(vector1, vector2):
    return np.conj(vector1.T).dot(vector2)

def _pauli_z(qubit, n_qubits):
    return _pauli(qubit, n_qubits, [[1,0], [0,-1]])

def _pauli_x(qubit, n_qubits):
    return _pauli(qubit, n_qubits, [[0,1], [1,0]])

def _pauli(qubit, n_qubits, pauli):
    i_gate = np.identity(2)
    gates = [[1]]
    for i in range(n_qubits):
        if i == qubit:
            gates = np.kron(gates, pauli)
        else:
            gates = np.kron(gates, i_gate)

    return gates
