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
    if target_psi.shape[0] != 2**(spaceA_bit + spaceB_bit):
        raise RuntimeError("Please enter the correct subspace dimension!")
    elif (tmp:=np.linalg.norm(target_psi, ord=2)) != 1:
        target_psi /= tmp
    
    density_operator = target_psi @ target_psi.T.conjugate()
    density_operator_AB = [np.zeros([dimA:=2**spaceA_bit] * 2), 
                           np.zeros([dimB:=2**spaceB_bit] * 2)]
    
    # 生成每个子空间的基
    ket_AB = [[np.eye(dimA)[:, i, None] for i in range(dimA)],
              [np.eye(dimB)[:, i, None] for i in range(dimB)]]
    
    '''生成子空间的约化密度矩阵
    :param dim:     子空间维度
    :param dim_:    约化子空间维度
    :param flag:    标记约化子空间中的基的索引    
    '''
    def get_rhoAB(dim:int, dim_:int, flag:int) -> None:
        for i in range(dim_):
            density_operator_AB[1-flag] += reduce(np.matmul, 
                                                [tmp:=(np.kron(np.eye(dim), 
                                                       ket_AB[flag][i].T.conjugate()))] + \
                                                [density_operator] + \
                                                [tmp.T.conjugate()]
                                         )
    get_rhoAB(dimA, dimB, 1); get_rhoAB(dimB, dimA, 0)

    e_vals = []; e_vecs = []
    e_val, e_vec = np.linalg.eig(density_operator_AB[0])
    e_vals.append(e_val); e_vecs.append(e_vec)
    print('子空间 A 约化密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)

    e_val, e_vec = np.linalg.eig(density_operator_AB[1])
    e_vals.append(e_val); e_vecs.append(e_vec)
    print('子空间 B 约化密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)

    print('该纯态为：', '直积态' if sum(e_val == 1) == 1 else '纠缠态')


if __name__ == "__main__":
    psi_test = np.array([[1.],
                         [0.],
                         [0.],
                         [1.]])
    schmidt_decomposition(psi_test)
    print()
    psi_test = np.ones([2**3]*2)[:, 1, None]
    schmidt_decomposition(psi_test, 1, 2)