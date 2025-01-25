import time
from stream_handler import find_stream, get_stream_info, create_inlet, process_samples
from data_saver import DataSaver

def main():
    # 查找数据流
    stream_info = find_stream()
    if not stream_info:
        return

    # 获取流信息
    try:
        info = get_stream_info(stream_info)

        print("\n=== 数据流信息 ===")
        print(f"名称: {info.get('name', '未知')}")
        print(f"类型: {info.get('type', '未知')}")
        print(f"通道数: {info.get('channel_count', 0)}")
        print(f"采样率: {info.get('sampling_rate', 0)} Hz")
        print(f"源ID: {info.get('source_id', '未知')}")
        print(f"数据格式: {info.get('channel_format', '未知')}")

        # 打印额外信息（如果有）
        if 'created_at' in info:
            print(f"创建时间: {info['created_at']}")
        if 'hostname' in info:
            print(f"主机名: {info['hostname']}")
        if 'session_id' in info:
            print(f"会话ID: {info['session_id']}")
        if 'desc' in info:
            print(f"描述: {info['desc']}")

        print("\n通道列表:")
        for i, ch in enumerate(info.get('channels', [])):
            print(f"  {i+1}. {ch}")
        print("================\n")

    except Exception as e:
        print(f"显示流信息时出错: {e}")
        return

    # 创建数据流入口
    inlet = create_inlet(stream_info)
    if not inlet:
        return

    # 设置批量读取参数
    try:
        sampling_rate = float(info['sampling_rate']) if info.get('sampling_rate', 0) > 0 else 100
        chunk_size = max(1, int(sampling_rate / 10))
        print(f"批量读取大小: {chunk_size}")
    except Exception as e:
        print(f"设置批量读取参数时出错，使用默认值: {e}")
        chunk_size = 10

    print("\n开始读取数据流...")
    print("按 Ctrl+C 停止读取\n")

    # 添加计数器用于调试
    sample_count = 0
    empty_sample_count = 0
    last_print_time = time.time()
    start_time = time.time()

    # 确保通道列表不为空
    if not info.get('channels'):
        info['channels'] = [f"Channel_{i}" for i in range(info['channel_count'])]

    # 创建数据保存器
    data_saver = DataSaver()

    try:
        while True:
            samples, timestamps = inlet.pull_chunk(timeout=0.0,
                                                max_samples=chunk_size)

            current_time = time.time()

            if samples:
                sample_count += len(samples)
                # 检查是否有空数据
                empty_samples = sum(1 for s in samples if not s)
                empty_sample_count += empty_samples

                # 保存数据
                for sample, timestamp in zip(samples, timestamps):
                    if sample:  # 只保存非空数据
                        data_saver.add_data(sample, timestamp)

                process_samples(samples, timestamps, info['channels'])

            # 每5秒打印一次统计信息
            if current_time - last_print_time >= 5:
                print(f"\n=== 数据统计 ===")
                print(f"总接收样本数: {sample_count}")
                print(f"空样本数: {empty_sample_count}")
                if sample_count > 0:
                    print(f"有效样本率: {((sample_count-empty_sample_count)/sample_count*100):.2f}%")
                    print(f"当前采样率: {sample_count/(current_time-start_time):.2f} Hz")
                print("===============\n")
                last_print_time = current_time

            if len(samples) < chunk_size:
                time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n用户中断数据流读取")
    except Exception as e:
        print(f"读取数据流时出错: {e}")
    finally:
        # 关闭数据保存器
        data_saver.close()
        print(f"\n数据已保存到目录: {data_saver.session_path}")
        
        # 打印最终统计信息
        end_time = time.time()
        print("\n=== 最终统计 ===")
        print(f"总运行时间: {end_time - start_time:.2f} 秒")
        print(f"总接收样本数: {sample_count}")
        print(f"空样本数: {empty_sample_count}")
        if sample_count > 0:
            print(f"有效样本率: {((sample_count-empty_sample_count)/sample_count*100):.2f}%")
            print(f"平均采样率: {sample_count/(end_time-start_time):.2f} Hz")
        print("===============\n")
        print("数据流读取结束")

if __name__ == '__main__':
    main()

