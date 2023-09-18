import numpy as np
from functools import reduce


class QuantumSimulator():
    GATE_DICT = {'x':np.eye(2)[[1, 0], :],
                 'y':np.array([[0. , -1.j],
                               [1.j, 0.  ]]), 
                 'z':np.array([[1., 0. ],
                               [0., -1.]]),
                 'h':np.array([[1.0, 1.0 ],
                               [1.0, -1.0]]) / np.sqrt(2),
                 'rx':lambda theta:np.array([[np.cos(theta/2)    , -1j*np.sin(theta/2)],
                                             [-1j*np.sin(theta/2), np.cos(theta/2)    ]]), 
                 'ry':lambda theta:np.array([[np.cos(theta/2), -np.sin(theta/2)],
                                             [np.sin(theta/2), np.cos(theta/2) ]]), 
                 'rz':lambda theta:np.array([[np.exp(-1j*theta/2), 0                 ],
                                             [0                  , np.exp(1j*theta/2)]])
    }

    def __init__(self, num_qubits:int = 2) -> None:
        self.state = np.zeros((2**num_qubits, 1))
        self.state[0, 0] = 1.0
        self.num_qubits = num_qubits

    # 重置量子态
    def reset_state(self) -> None:
        self.state = np.zeros((2**self.num_qubits, 1))
        self.state[0, 0] = 1.0

    '''对量子态作用量子门
    :param gete_name:       作用于量子比特的量子门
    :param qubit:           目标比特
    :param qubit_control:   控制比特
    :param tehta:           旋转角度
    '''
    def act_gate(self, 
                 gate_name:str,
                 qubit:int,
                 qubit_control:int = None,
                 theta:float = None) -> None:
        try:
            gate = QuantumSimulator.GATE_DICT[gate_name]
        except KeyError:
            raise RuntimeError('Quantum gate does not exist!')
        if not (theta and qubit_control):
            self.state = reduce(np.kron, 
                                ([np.eye(2)] * (qubit - 1) + \
                                 [gate] + \
                                 [np.eye(2) * (self.num_qubits - qubit)])
                         ) @ self.state

        print(self.state)
            
    # 测量量子态
    def measure(self) -> None:
        pass

        
if __name__ == '__main__':
    qs = QuantumSimulator()

    qs.act_gate('h', 1)