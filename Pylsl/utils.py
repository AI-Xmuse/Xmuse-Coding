def safe_decode(byte_data, encodings=['utf-8', 'gbk', 'gb2312', 'ascii']):
    """
    安全地尝试多种编码方式解码数据

    Args:
        byte_data: 要解码的字节数据
        encodings: 要尝试的编码列表

    Returns:
        解码后的字符串或原始数据的字符串表示
    """
    if not isinstance(byte_data, bytes):
        return str(byte_data)

    for encoding in encodings:
        try:
            return byte_data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return str(byte_data)  # 如果所有编码都失败，返回原始字符串表示 