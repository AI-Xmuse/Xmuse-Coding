import time
from typing import Optional, List
from pylsl import StreamInlet, resolve_stream, StreamInfo
from utils import safe_decode

def get_stream_info(stream_info: StreamInfo) -> dict:
    """
    安全地获取流信息

    Args:
        stream_info: StreamInfo 对象

    Returns:
        包含流信息的字典
    """
    info = {}

    try:
        # 基本信息获取
        info['channel_count'] = stream_info.channel_count()

        # 确保立即创建通道列表
        channels = []
        for i in range(info['channel_count']):
            try:
                raw_label = stream_info.channel_label(i)
                if raw_label:
                    channel_name = safe_decode(raw_label)
                    channels.append(channel_name if channel_name else f"Channel_{i}")
                else:
                    channels.append(f"Channel_{i}")
            except:
                channels.append(f"Channel_{i}")
        info['channels'] = channels

        # 确保基本信息存在，即使出错
        if 'channel_count' not in info:
            info['channel_count'] = 4  # 设置为实际观察到的通道数
        if 'channels' not in info:
            info['channels'] = [f"Channel_{i}" for i in range(info['channel_count'])]

        # 使用更安全的方式获取基本信息
        try:
            raw_name = stream_info.name()
            info['name'] = safe_decode(raw_name) if raw_name else "未知名称"

            raw_type = stream_info.type()
            info['type'] = safe_decode(raw_type) if raw_type else "未知类型"

            info['sampling_rate'] = stream_info.nominal_srate()

            raw_source_id = stream_info.source_id()
            info['source_id'] = safe_decode(raw_source_id) if raw_source_id else "未知源ID"

            info['channel_format'] = str(stream_info.channel_format())

            # 尝试获取额外的流信息
            try:
                info['created_at'] = stream_info.created_at()
                info['uid'] = stream_info.uid()
                info['session_id'] = safe_decode(stream_info.session_id()) if stream_info.session_id() else "未知会话"
                info['hostname'] = safe_decode(stream_info.hostname()) if stream_info.hostname() else "未知主机"
                info['desc'] = safe_decode(stream_info.desc()) if stream_info.desc() else "无描述"
            except:
                pass  # 额外信息获取失败不影响主要功能

        except Exception as e:
            print(f"警告：获取流信息时出错: {str(e)}")

    except Exception as e:
        print(f"警告：获取流信息时出错: {str(e)}")
        # 确保基本信息存在，即使出错
        if 'channel_count' not in info:
            info['channel_count'] = 4  # 设置为实际观察到的通道数
        if 'channels' not in info:
            info['channels'] = [f"Channel_{i}" for i in range(info['channel_count'])]

    return info

def find_stream(stream_type: str = 'EEG', timeout: float = 10.0) -> Optional[StreamInfo]:
    """
    查找指定类型的LSL数据流
    """
    print(f"正在查找 {stream_type} 类型的数据流...")
    streams = resolve_stream('type', stream_type)

    start_time = time.time()
    while not streams and (time.time() - start_time) < timeout:
        time.sleep(0.1)
        streams = resolve_stream('type', stream_type)

    if not streams:
        print(f"未找到 {stream_type} 类型的数据流")
        return None

    print(f"找到 {len(streams)} 个数据流")
    return streams[0]

def create_inlet(stream_info: StreamInfo, max_buflen: int = 360,
                max_chunklen: int = 0) -> Optional[StreamInlet]:
    """
    创建数据流入口
    """
    try:
        inlet = StreamInlet(stream_info, max_buflen=max_buflen, max_chunklen=max_chunklen)
        return inlet
    except Exception as e:
        print(f"创建数据流入口时出错: {e}")
        return None

def process_samples(samples: List[List[float]], timestamps: List[float],
                   channel_names: List[str]) -> None:
    """
    处理接收到的数据样本
    """
    for sample, timestamp in zip(samples, timestamps):
        # 检查是否有实际的数据
        if not sample:
            print(f"警告：在时间戳 {timestamp:.3f} 收到空数据")
            continue

        print(f"\n时间戳: {timestamp:.3f}")

        # 打印原始数据用于调试
        print(f"原始数据: {sample}")

        # 检查数据有效性
        if len(sample) != len(channel_names):
            print(f"警告：数据通道数 ({len(sample)}) 与预期通道数 ({len(channel_names)}) 不匹配")
            continue

        # 显示数据
        data_dict = dict(zip(channel_names, sample))
        for ch_name, value in data_dict.items():
            if value is not None:
                print(f"{ch_name}: {value:.2f}", end=' | ')
            else:
                print(f"{ch_name}: 无数据", end=' | ')
        print()  # 换行 