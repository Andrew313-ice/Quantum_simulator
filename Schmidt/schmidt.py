import numpy as np
from functools import reduce


def schmidt_decomposition(target_psi:np.ndarray,
                          spaceA_bit:int = 1,
                          spaceB_bit:int = 1) -> None:
    '''复合系统纯态施密特分解
    :param target_psi:      复合系统待分解量子态
    :param spaceA_bit:      子空间A的比特数
    :param spaceB_bit:      子空间B的比特数
    '''
    if (tmp:=np.sqrt(target_psi.shape[0])) != int(tmp):
        raise RuntimeError("Please enter the correct quantum state column vector!")
    elif tmp != (spaceA_bit + spaceB_bit):
        raise RuntimeError("Please enter the correct subspace dimension!")
    elif (tmp:=np.linalg.norm(target_psi, ord=2)) != 1:
        target_psi /= tmp
    
    density_operator = target_psi @ target_psi.T.conjugate()
    density_operator_AB = [np.zeros([dimA:=2**spaceA_bit] * 2), 
                           np.zeros([dimB:=2**spaceB_bit] * 2)]
    ket_AB = [[np.eye(dimA)[:, i, None] for i in range(dimA)],
              [np.eye(dimB)[:, i, None] for i in range(dimB)]]
    
    # 得到约化密度矩阵
    def get_rhoAB(dim:int, flag:int) -> None:
        for i in range(dim):
            density_operator_AB[flag] += reduce(np.matmul, 
                                                [np.kron(np.eye(dim), 
                                                        ket_AB[flag][i].T.conjugate())] + \
                                                [density_operator] + \
                                                [np.kron(np.eye(dim), ket_AB[flag][i])]
                                         ) 
    get_rhoAB(dimA, 0); get_rhoAB(dimB, 1)
    # I = np.eye(2)
    # ket = [I[:, i, None] for i in range(2)]
    # for i in range(2):
    #     density_operator_AB[0] += np.kron(I, ket[i].T.conjugate()) @ \
    #                               density_operator @ \
    #                               np.kron(I, ket[i])
    #     density_operator_AB[1] += np.kron(ket[i].T.conjugate(), I) @  \
    #                               density_operator @  \
    #                               np.kron(ket[i], I)
    e_val, e_vec = np.linalg.eig(density_operator_AB[0])
    print('子空间 A 密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)
    e_val, e_vec = np.linalg.eig(density_operator_AB[1])
    print('子空间 B 密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)

    print("直积态" if sum(e_val == 1) == 1 else "纠缠态")


if __name__ == "__main__":
    psi_test = np.array([[1.],
                         [0.],
                         [0.],
                         [1.]], dtype=np.float64)
    schmidt_decomposition(psi_test)

    