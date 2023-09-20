import sys; sys.path.append('./')
from Package.simulator import QuantumSimulator


def teleportation(tele_sim:QuantumSimulator):
    '''量子隐形传态
    :param tele_sim:   量子隐形传态模拟器      
    '''
    tele_sim.act_gate('ry', 1, angle=0.123) # 制备待传输态
    tele_sim.act_gate('h', 2)
    tele_sim.act_gate('cnot', 3, 2)
    tele_sim.act_gate('cnot', 2, 1)
    tele_sim.act_gate('h', 1)

    if (tmp2:=tele_sim.measure(2)): tele_sim.act_gate('x', 3)
    if (tmp3:=tele_sim.measure(1)): tele_sim.act_gate('z', 3)   
    if tmp2: tele_sim.act_gate('x', 2)
    if tmp3: tele_sim.act_gate('x', 3)

    tele_sim.act_gate('ry', 3, angle=-0.123)  # 检测量子态是否传输成功
    tele_sim.dump()


if __name__ == '__main__':
    tele_sim = QuantumSimulator(3)

    teleportation(tele_sim)
