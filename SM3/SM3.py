import struct

# IV初始值 
IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
]

#  T 的初始化
T = [0x79CC4519 if i < 16 else 0x7A879D8A for i in range(64)]

# 循环左移n为位数, m为要循环左移的消息
def left_rotate(n, m):
    return ((n << m) & 0xFFFFFFFF) | ((n >> (32 - m)) & 0xFFFFFFFF)

# 填充函数，确保消息长度是 512 位的倍数
def padding(message):
    message = bytearray(message, 'utf-8')
    message_len = len(message) * 8  # 计算消息的位长度
    message.append(0x80)  # 添加' 1 '

    # 填充 '0' ，直到消息长度mod 512 =488
    message.extend([0x00] * ((56 - len(message) % 64) % 64))

    # 添加原始消息长度的64位表示（以比特为单位）
    message += struct.pack('>Q', message_len)
    print (message)
    return message

# 消息扩展函数，将 512 位的消息扩展为 132 个 32 位字
def message_extension(block):
    W = list(struct.unpack('>16L', block))  # 拆分为16个字
    for i in range(16, 68):
        W.append(P1(W[i - 16] ^ W[i - 9] ^ left_rotate(W[i - 3], 15)) ^
                 left_rotate(W[i - 13], 7) ^ W[i - 6])

    # 扩展 W[68] 到 W[131]
    W_ = [W[i] ^ W[i + 4] for i in range(64)]
    return W, W_

# 非线性变换 P1
def P1(X):
    return X ^ left_rotate(X, 15) ^ left_rotate(X, 23)

# 非线性变换 P0
def P0(X):
    return X ^ left_rotate(X, 9) ^ left_rotate(X, 17)

#函数FF，j < 16 时使用or，其他情况下使用and 和 or
def FF(X, Y, Z, j):
    return (X ^ Y ^ Z) if j < 16 else ((X & Y) | (X & Z) | (Y & Z))

# 函数GG
def GG(X, Y, Z, j):
    return (X ^ Y ^ Z) if j < 16 else ((X & Y) | (~X & Z))

# 压缩函数
def compress(V, B):
    W, W_ = message_extension(B)
    A, B, C, D, E, F, G, H = V

    for j in range(64):
        SS1 = left_rotate((left_rotate(A, 12) + E + left_rotate(T[j], j % 32)) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ left_rotate(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) & 0xFFFFFFFF
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = left_rotate(B, 9)
        B = A
        A = TT1
        H = G
        G = left_rotate(F, 19)
        F = E
        E = P0(TT2)

    # 更新 V 值
    return [(V[i] ^ var) & 0xFFFFFFFF for i, var in enumerate([A, B, C, D, E, F, G, H])]
# 判断输入是普通字符串还是十六进制字符串
def process_input(input_data):
    # 判断输入是否为十六进制字符串（只包含十六进制字符和空格）
    is_hex_string = all(c in "0123456789abcdefABCDEF " for c in input_data)
    
    if is_hex_string:
        try:
            return convert_hex_input(input_data)
        except ValueError:
            # 如果转换失败，说明不是有效的十六进制字符串
            pass
    
    # 如果不是十六进制字符串，假设是普通字符串，转换为字节
    return bytearray(input_data, 'utf-8')
# 计算 SM3 哈希值
def sm3_hash(message):
    # 填充
    padded_message = padding(message)
    blocks = [padded_message[i:i + 64] for i in range(0, len(padded_message), 64)]
    V = IV

    # 压缩
    for block in blocks:
        V = compress(V, block)

    # 将最终结果 V 转换为 16 进制字符串
    return ''.join(f'{x:08x}' for x in V)


message = input("输入要加密的消息:")
result = sm3_hash(message)
print(f"SM3 哈希值: {result}")