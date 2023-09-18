import numpy as np


def schmidt_decomposition(target_psi:np.ndarray,
                          spaceA_dim:int = 1,
                          spaceB_dim:int = 1) -> None:
    '''两体纯态施密特分解
    :param target_psi:      复合系统待分解量子态
    :param spaceA_dim:      子空间A的维度
    :param spaceB_dim:      子空间B的维度
    '''
    if (tmp:=np.sqrt(target_psi.shape[0])) != int(tmp):
        raise RuntimeError("Please enter the correct quantum state column vector!")
    elif tmp != (spaceA_dim + spaceB_dim):
        raise RuntimeError("Please enter the correct subspace dimension!")
    elif (tmp:=np.linalg.norm(target_psi, ord=2)) != 1:
        target_psi /= tmp
    
    density_operator = target_psi @ target_psi.T.conjugate()
    density_operator_AB = [np.zeros([2, 2]) for _ in range(2)]
    I = np.eye(2)
    ket = [I[:, i, None] for i in range(2)]
    for i in range(2):
        density_operator_AB[0] += np.kron(I, ket[i].T.conjugate()) @ \
                                  density_operator @ \
                                  np.kron(I, ket[i])
        density_operator_AB[1] += np.kron(ket[i].T.conjugate(), I) @  \
                                  density_operator @  \
                                  np.kron(ket[i], I)
    e_val, e_vec = np.linalg.eig(density_operator_AB[0])
    print('子空间 A 密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)
    e_val, e_vec = np.linalg.eig(density_operator_AB[1])
    print('子空间 B 密度矩阵的本征值为：', e_val, '，本征矢为：', e_vec)

    print("直积态" if sum(e_val, 15 == 1) == 1 else "纠缠态")


if __name__ == "__main__":
    psi_test = np.array([[1.],
                         [1.],
                         [0.],
                         [1.]], dtype=np.float64)
    schmidt_decomposition(psi_test)

    