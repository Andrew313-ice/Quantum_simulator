import numpy as np
from functools import reduce
from itertools import chain


I = np.eye(2)
GATE_DICT = {
    'x':np.eye(2)[[1, 0], :],
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
                                [0                  , np.exp(1j*theta/2)]]),
    'cnot':np.eye(4)
}

class QuantumSimulator():
    '''初始化
    :param num_qubits:    量子比特总数
    '''
    def __init__(self, *, 
                 num_qubits) -> None:
        self.state = np.zeros((2**num_qubits, 1))
        self.state[0, 0] = 1.0
        self.num_qubits = num_qubits

    '''打印量子态'''
    def dump(self) -> None:
        print(self.state)

    '''重置量子态'''
    def reset_state(self) -> None:
        self.state = np.zeros((2**self.num_qubits, 1))
        self.state[0, 0] = 1.0

    '''模拟发送发量子态'''
    def send_state(self) -> np.ndarray:
        return self.state

    '''模拟接收量子态
    :param receive_state:    待接收量子态
    '''
    def receive_state(self, 
                      receive_state:np.ndarray) -> None:
        self.state = receive_state
    
    '''对量子态作用量子门
    :param gate_name:       作用于量子比特的量子门
    :param qubit:           目标比特
    :param qubit_control:   控制比特
    :param angle:           旋转角度
    '''
    def act_gate(self, 
                 gate_name:str,
                 qubit:int = 1,
                 qubit_control:int = None,
                 angle:float = None) -> None:
        try:
            gate = GATE_DICT[gate_name]
        except KeyError:
            raise RuntimeError(f'量子门 {gate_name} 不存在')
        if not qubit_control:
            self.state = reduce(np.kron, chain([I] * (qubit - 1),
                                               [gate(angle) if callable(gate) else gate],
                                               [I] * (self.num_qubits - qubit)
                                         )
                         ) @ self.state
        else:
            self.state = \
                reduce(np.kron, chain([I] * (min(qubit, qubit_control) - 1),
                                      [gate[[0, 3, 2, 1], :] 
                                       if qubit < qubit_control else 
                                       gate[[0, 1, 3, 2], :]],
                                      [I] * (self.num_qubits - max(qubit, qubit_control))
                                )
                ) @ self.state

    '''量子态测量
    :param qubit:   待测量比特位
    '''
    def measure(self,
                qubit:int = 1) -> int:
        projection_operator = [
            reduce(np.kron, chain([I] * (qubit - 1),
                                  [(tmp:=I[:, i, None]) @ tmp.T.conjugate()],
                                  [I] * (self.num_qubits - qubit)
                            )
            ) for i in range(2)
        ]
        states = [
            projector @ self.state 
            for projector in projection_operator
        ]
        rand = np.random.choice([0, 1], 
                                p=[np.linalg.norm(states[i]) ** 2 for i in range(2)]
               )
        self.state = (tmp:=states[rand]) / np.linalg.norm(tmp)
        return rand
    

if __name__ == '__main__': 
    qs = QuantumSimulator(num_qubits=2)
    qs.act_gate('h', 1)
    qs.act_gate('cnot', 2, 1)
    qs.dump()

