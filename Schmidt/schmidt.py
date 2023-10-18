import numpy as np
from functools import reduce
from itertools import chain


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
            tmp = np.kron(np.eye(dim), 
                          ket_AB[flag][i].T.conjugate()) \
                  if flag else \
                  np.kron(ket_AB[flag][i].T.conjugate(), 
                          np.eye(dim))
            density_operator_AB[1-flag] += \
                reduce(np.matmul, chain([tmp],
                                        [density_operator],
                                        [tmp.T.conjugate()])
                )
            
    get_rhoAB(dimA, dimB, 1); get_rhoAB(dimB, dimA, 0)
    e_vals = [0, 0]
    e_vals[0], e_vecA = np.linalg.eig(density_operator_AB[0])
    print('子空间 A 约化密度矩阵的本征值为：\n', e_vals[0], '\n本征矢为：\n', e_vecA)

    e_vals[1], e_vecB = np.linalg.eig(density_operator_AB[1])
    print('子空间 B 约化密度矩阵的本征值为：\n', e_vals[1], '\n本征矢为：\n', e_vecB)

    min_dim_index = 0 if e_vals[0].shape[0] <= e_vals[1].shape[0] else 1
    print('该纯态为：', '直积态' if np.round(max(e_vals[min_dim_index]), 10) == 1 
                               else '纠缠态', '\n')


if __name__ == "__main__":
    psi_test = np.array([[0.],
                         [1.],
                         [1.],
                         [0.]])
    schmidt_decomposition(psi_test)

    psi_test = np.ones([2**3]*2)[:, 1, None]
    schmidt_decomposition(psi_test, 1, 2)