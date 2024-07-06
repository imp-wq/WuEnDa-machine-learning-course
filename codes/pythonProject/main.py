import numpy as np

if __name__ == "__main__":
    data = np.random.rand(3, 4)
    print(f'data:\t{data}')
    print(f'[::]\t{data[::]}')
    print(f'[:,:2]:\t{data[:,:2]}')
    # the second column
    print(f'[:,2]:\t{data[:, 2]}')
    print(f'[:2]:\t{data[:2]}')

    print(f'[2,:]:\t{data[2, :]}')

    # test 1-D
    # a = np.array([1, 2, 3, 4])
    # b = np.array([-1, 4, 3, 2])
    # c = np.dot(a, b)
    # print(f"NumPy 1-D np.dot(a, b) = {c}, np.dot(a, b).shape = {c.shape} ")
    # c = np.dot(b, a)
    # print(f"NumPy 1-D np.dot(b, a) = {c}, np.dot(a, b).shape = {c.shape} ")
    # print(f"a{{-1}} is: {a[-1]}")

    # X = np.array([[1], [2], [3], [4]])
    # w = np.array([2])
    # c = np.dot(X[1], w)
    #
    # print(f"X[1] has shape {X[1].shape}")
    # print(f"w has shape {w.shape}")
    # print(f"c has shape {c.shape}")

    # vector indexing operations on matrices
    # a = np.arange(6).reshape(-1, 2)  # reshape is a convenient way to create matrices
    # print(f"a.shape: {a.shape}, \na= {a}")
    #
    # # access an element
    # print(
    #     f"\na[2,0].shape:   {a[2, 0].shape}, a[2,0] = {a[2, 0]},     type(a[2,0]) = {type(a[2, 0])} Accessing an element returns a scalar\n")
    #
    # # access a row
    # print(f"a[2].shape:   {a[2].shape}, a[2]   = {a[2]}, type(a[2])   = {type(a[2])}")
