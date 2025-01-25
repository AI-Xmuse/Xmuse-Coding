import pandas as pd
import numpy as np
import mne


def loadEEGCSV(data_path: str, window: float, frame: float, sample_rate: int, channels: int):
    """
    Description: 加载CSV文件并进行数据分段
    -------------------------------
    Parameters:
    data_path: 输入的csv文件路径
    window: 窗的大小（单位：s）
    frame: 帧的大小，即窗移的大小（单位：s）
    sample_rate: 采样率的大小（单位：Hz）
    channels: 通道数量

    Returns:
    X: 形状为(segments, samples, channels)的numpy数组
    """
    df = pd.read_csv(data_path)
    print("CSV文件形状:", df.shape)
    print("CSV文件列名:", df.columns.tolist())

    data = df.values

    if channels != data.shape[1]:
        print(f"错误：期望{channels}个通道，但数据中有{data.shape[1]}个通道")
        return None

    # 计算窗口和帧的采样点数
    window_samples = int(window * sample_rate)
    frame_samples = int(frame * sample_rate)

    # 计算总段数
    n_segments = max(0, (data.shape[0] - window_samples) // frame_samples + 1)

    if n_segments == 0:
        raise ValueError(f"数据长度不足以分段。需要至少{window_samples}个采样点，但只有{data.shape[0]}个")

    # 创建输出数组
    X = np.zeros((n_segments, window_samples, channels))

    # 使用滑动窗口进行分段
    for i in range(n_segments):
        start_idx = i * frame_samples
        end_idx = start_idx + window_samples
        if end_idx > data.shape[0]:
            # 如果最后一段数据不足，用0填充
            X[i, :(data.shape[0] - start_idx), :] = data[start_idx:, :]
        else:
            X[i] = data[start_idx:end_idx, :]

    return X


def loadEEGNPY(data_path: str, window: float, frame: float, sample_rate: int):
    """
    Description: 加载NPY文件并进行数据分段
    -------------------------------
    Parameters:
    data_path: 输入的NPY文件路径
    window: 窗的大小（单位：s）
    frame: 帧的大小，即窗移的大小（单位：s）
    sample_rate: 采样率的大小（单位：Hz）

    Returns:
    X: 形状为(segments, samples, channels)的numpy数组
    """
    data = np.load(data_path)
    print("原始数据形状:", data.shape)

    if len(data.shape) != 2:
        raise ValueError("NPY文件数据必须是2维数组")

    if data.shape[0] < data.shape[1]:
        data = data.T
        print("数据已转置，新形状:", data.shape)

    FEATURE_NUM = int(window * sample_rate)
    FRAME_NUM = int(frame * sample_rate)

    n_segments = max(0, (data.shape[0] - FEATURE_NUM) // FRAME_NUM + 1)

    if n_segments == 0:
        raise ValueError(f"数据长度不足以分段。需要至少{FEATURE_NUM}个采样点，但只有{data.shape[0]}个")

    X = np.zeros((n_segments, FEATURE_NUM, data.shape[1]))

    for i in range(n_segments):
        start_idx = i * FRAME_NUM
        end_idx = start_idx + FEATURE_NUM
        X[i] = data[start_idx:end_idx]

    return X


def loadEEGEDF(data_path: str, window: float, frame: float, sample_rate: int, channels: list = None):
    """
    Description: 加载EDF文件并进行数据分段
    -------------------------------
    Parameters:
    data_path: 输入的EDF文件路径
    window: 窗的大小（单位：s）
    frame: 帧的大小，即窗移的大小（单位：s）
    sample_rate: 采样率的大小（单位：Hz）
    channels: 需要加载的通道名称列表，如果为None则加载所有通道

    Returns:
    X: 形状为(segments, samples, channels)的numpy数组
    ch_names: 通道名称列表
    """
    try:
        raw = mne.io.read_raw_edf(data_path, preload=True)
        print("EDF文件信息:")
        print(f"采样率: {raw.info['sfreq']} Hz")
        print(f"通道数: {len(raw.ch_names)}")
        print(f"通道名称: {raw.ch_names}")
        print(f"数据时长: {raw.n_times / raw.info['sfreq']:.2f} 秒")

        if channels is not None:
            raw.pick_channels(channels)

        if raw.info['sfreq'] != sample_rate:
            print(f"重采样从 {raw.info['sfreq']} Hz 到 {sample_rate} Hz")
            raw.resample(sample_rate)

        data = raw.get_data()
        ch_names = raw.ch_names

        data = data.T

        FEATURE_NUM = int(window * sample_rate)
        FRAME_NUM = int(frame * sample_rate)

        n_segments = max(0, (data.shape[0] - FEATURE_NUM) // FRAME_NUM + 1)

        if n_segments == 0:
            raise ValueError(f"数据长度不足以分段。需要至少{FEATURE_NUM}个采样点，但只有{data.shape[0]}个")

        X = np.zeros((n_segments, FEATURE_NUM, data.shape[1]))

        for i in range(n_segments):
            start_idx = i * FRAME_NUM
            end_idx = start_idx + FEATURE_NUM
            X[i] = data[start_idx:end_idx]

        return X, ch_names

    except Exception as e:
        print(f"加载EDF文件时出错: {str(e)}")
        raise


def loadEEGData(data_path: str, window: float, frame: float, sample_rate: int, channels: int = None,
                edf_channels: list = None):
    """
    Description: 统一的数据加载接口，支持CSV、NPY和EDF格式
    -------------------------------
    Parameters:
    data_path: 输入文件路径
    window: 窗的大小（单位：s）
    frame: 帧的大小，即窗移的大小（单位：s）
    sample_rate: 采样率的大小（单位：Hz）
    channels: 通道数量（仅CSV格式需要）
    edf_channels: 需要加载的EDF通道名称列表（仅EDF格式可用）

    Returns:
    X: 形状为(segments, samples, channels)的numpy数组
    ch_names: 通道名称列表（仅EDF格式返回）
    """
    file_ext = data_path.split('.')[-1].lower()

    if file_ext == 'csv':
        if channels is None:
            raise ValueError("CSV格式需要指定channels参数")
        return loadEEGCSV(data_path, window, frame, sample_rate, channels)
    elif file_ext == 'npy':
        return loadEEGNPY(data_path, window, frame, sample_rate)
    elif file_ext == 'edf':
        return loadEEGEDF(data_path, window, frame, sample_rate, edf_channels)
    else:
        raise ValueError(f"不支持的文件格式：{file_ext}")