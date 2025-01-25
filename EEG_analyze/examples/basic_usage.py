from main import EEGProcessor

def basic_example():
    """基础使用示例"""
    # 创建EEG处理器实例
    processor = EEGProcessor(sample_rate=250)

    # 处理单个文件
    results = processor.process_file(
        'data/sample.csv',
        window_size=2.0,
        overlap=0.5,
        preprocess_methods=['filter', 'normalize']
    )

    print("处理完成!")
    print(f"数据形状: {results['data'].shape}")
    print(f"提取的特征: {list(results['features'].keys())}")

if __name__ == "__main__":
    basic_example() 