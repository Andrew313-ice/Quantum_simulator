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
    key = array('b')

    def send_receive(num:int) -> (array, array, array, array):
        alice_bases = array('b'); alice_keys = array('b')
        bob_bases = array('b'); bob_keys = array('b')
        for _ in range(2*num):
            # 生成随机密钥，并随机选择基
            if (tmp:=np.random.choice([0, 1])):
                alice_simulator.act_gate('x')
            alice_keys.append(tmp)
            if (tmp:=np.random.choice([0, 1])):
                alice_simulator.act_gate('h')
            alice_bases.append(tmp)

            # 模拟发送和接受量子比特的过程
            bob_simulator.receive_state(alice_simulator.send_state())
            bob_bases.append(np.random.choice([0, 1]))
            if bob_bases[-1]:
                bob_simulator.act_gate('h')
            bob_keys.append(bob_simulator.measure())

            # 重置量子态
            alice_simulator.reset_state(); bob_simulator.reset_state()
        return alice_bases, alice_keys, bob_bases, bob_keys

    while len(key) < key_len:
        alice_bases, alice_keys, bob_bases, bob_keys = \
            send_receive(key_len - len(key))
        right_index = np.array(alice_bases) == np.array(bob_bases)
        assert np.sum(
                (right_keys:=np.array(alice_keys)[right_index]) == \
                np.array(bob_keys)[right_index]
               ) != np.sum(right_keys)
        key.extend(right_keys)
        
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
    print(f'密钥为：{bin_to_hex(key)}')

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
