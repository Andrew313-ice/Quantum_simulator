import numpy as np
import sys; sys.path.append('./')
from Package.simulator import QuantumSimulator


def quantum_optimal_strategy(bell_state:QuantumSimulator, 
                             alice_input:np.int32, 
                             bob_input:np.int32) -> list:
    '''量子最优策略
    :param bell_state:      Bell态系统
    :param alice_input:     Alice收到的信息
    :param bob_input:       Bob收到的信息
    '''
    result = []
    alice_angles = [90 * np.pi / 180, 0]
    bob_angles = [45 * np.pi / 180, 135 * np.pi / 180]

    bell_state.act_gate('ry', 1, angle=alice_angles[alice_input])
    result.append(bell_state.measure(1))

    bell_state.act_gate('ry', 2, angle=bob_angles[bob_input])
    result.append(bell_state.measure(2))

    return result


def chsh_game(chsh_simulator:QuantumSimulator, 
              num:int) -> None:
    '''chsh游戏量子策略模拟
    :param chsh_simulator:      用于制备共享贝尔态
    :param int:                 chsh游戏进行的次数
    '''
    n = 0
    for _ in range(num):
        chsh_simulator.act_gate('h', 1)
        chsh_simulator.act_gate('cnot', 2, 1)
        alice_input, bob_input = [
            np.random.choice([0, 1]) for _ in range(2)
        ]
        alice_output, bob_output = quantum_optimal_strategy(chsh_simulator, 
                                                            alice_input, 
                                                            bob_input)
        n += 1 if ((alice_input and bob_input) == \
                   (alice_output ^ bob_output)) \
               else 0
        chsh_simulator.reset_state()
        
    print(f'经过{num}轮游戏后，玩家获胜的概率为：{100 * n / num}%')


if __name__ == '__main__':
    for _ in range(3):
        chsh_game(QuantumSimulator(num_qubits=2), 1000)
    