import numpy as np
from functools import reduce


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
                                [0                  , np.exp(1j*theta/2)]])
}

class QuantumSimulator():
    '''初始化
    :param num_qubits:    总比特数
    '''
    def __init__(self, 
                 num_qubits:int = 1) -> None:
        self.state = np.zeros((2**num_qubits, 1))
        self.state[0, 0] = 1.0
        self.num_qubits = num_qubits


    '''打印量子模拟器的信息'''
    def __repr__(self) -> str:
        return f'当前量子模拟器的比特数为：{self.num_qubits}\n量子态矢量为：\n{self.state}'


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
    :param gete_name:       作用于量子比特的量子门
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
        if not (angle and qubit_control):
            self.state = reduce(np.kron, 
                                [I] * (qubit - 1) + \
                                [gate] + \
                                [I] * (self.num_qubits - qubit)
                         ) @ self.state


    '''量子态测量
    :param qubit:   待测量比特位
    '''
    def measure(self,
                qubit:int = 1) -> bool:
        projection_operator = [
            reduce(np.kron, 
                   [I] * (qubit - 1) + \
                   [(tmp:=I[:, i, None]) @ tmp.T.conjugate()] + \
                   [I] * (self.num_qubits - qubit)
            ) for i in range(2)
        ]
        states = [
            projector @ self.state 
            for projector in projection_operator
        ]
        rand = np.random.choice([0, 1], 
                                p=[np.linalg.norm(states[i]) ** 2 for i in range(2)])
        self.state = (tmp:=states[rand]) / np.linalg.norm(tmp)
        return bool(rand)
    

