import numpy as np
from array import array
import sys; sys.path.append('./')
from Package.simulator import QuantumSimulator


def bin_to_hex(bits:np.ndarray) -> str:
    '''二进制转化为十六进制
    :param bits:    待转化二进制数组
    '''
    return hex(int(''.join(['1' if bit else '0' for bit in bits]), 2))


def generate_key(alice_simulator:QuantumSimulator, 
                 bob_simulator:QuantumSimulator,
                 key_len:int) -> np.ndarray:
    '''生成密钥
    :param alice:   发送方
    :param bob:     接收方
    :param key_len: 所需密钥长度（二进制）
    '''
    key = []; count = 0
    alice_basis = array('b'); alice_key = array('b')
    bob_basis = array('b'); bob_key = array('b')

    while len(key) < key_len:
        count += 1
        # 生成随机密钥，并随机选择基
        if (alice_key:=np.random.choice([0, 1])):
            alice_simulator.act_gate('x')
        if (alice_basis:=np.random.choice([0, 1])):
            alice_simulator.act_gate('h')

        # 模拟发送和接受量子比特的过程
        bob_simulator.receive_state(alice_simulator.send_state())
        if (bob_basis:=np.random.choice([0, 1])):
            bob_simulator.act_gate('h')
        bob_key = bob_simulator.measure()

        # 对比 Alice 和 Bob 选择的基，选取合适的密钥
        if alice_basis == bob_basis:
            assert alice_key == bob_key;  key.append(alice_key)

        # 重置量子态
        alice_simulator.reset_state(); bob_simulator.reset_state()
    print(f'经过{count}次迭代，生成{key_len}位密钥')
    return np.array(key)


def encrypt_decode(message:np.ndarray, 
                   key:np.ndarray) -> np.ndarray:
    '''加密、解密
    :param message:     待加密或解密的信息
    :param key:         密钥
    '''
    return np.array([
        message_bit ^ key_bit
        for (message_bit, key_bit) in zip(message, key)
    ])


def bb84(message:np.ndarray) -> None:
    '''bb84协议模拟
    :param message:     待传递信息
    '''
    alice_simulator = QuantumSimulator()
    bob_simulator = QuantumSimulator()
    print(f'Alice发送的信息为：{bin_to_hex(message)}')

    # 获取密钥
    key = generate_key(alice_simulator, bob_simulator, message.shape[0])

    # 信息加密
    message_encrypt = encrypt_decode(message, key)      
    print(f'Alice发送的信息加密后为：{bin_to_hex(message_encrypt)}')

    # 信息解密
    message_decode = encrypt_decode(message_encrypt, key)
    print(f'Bob接收到加密信息后，解密为：{bin_to_hex(message_decode)}')
    

if __name__ == '__main__':
    # 生成64个随机0、1作为要传递的信息
    message = np.random.randint(0, 2, 2**6)

    bb84(message)
