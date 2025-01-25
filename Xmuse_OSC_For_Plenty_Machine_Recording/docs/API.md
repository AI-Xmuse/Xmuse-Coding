# API 文档

## OSCDataReceiver

主要的数据接收器类。

### 初始化

```python
OSCDataReceiver(
    ports: List[int],
    signal_types: Optional[List[str]] = None,
    save_dir: str = "data",
    buffer_size: int = 1000
)
```

#### 参数
- `ports`: OSC 服务器端口列表
- `signal_types`: 需要接收的信号类型列表（可选）
- `save_dir`: 数据保存目录（默认："data"）
- `buffer_size`: 数据缓冲区大小（默认：1000）

### 方法

#### start()
启动数据接收服务。

```python
def start(self) -> None
```

#### stop()
停止数据接收服务。

```python
def stop(self) -> None
```

#### handle_message()
处理接收到的 OSC 消息。

```python
def handle_message(self, port: int, address: str, *args) -> None
```

### 属性
- `running`: 服务运行状态
- `data_buffer`: 数据缓冲区实例
- `signal_manager`: 信号管理器实例

## SignalManager

信号管理器类。

### 初始化

```python
SignalManager()
```

### 方法

#### add_signal()
添加信号。

```python
def add_signal(self, signal: str, callback: Optional[Callable] = None) -> None
```

#### remove_signal()
移除信号。

```python
def remove_signal(self, signal: str) -> None
```

#### is_active()
检查信号是否激活。

```python
def is_active(self, signal: str) -> bool
```

#### get_available_signals()
获取可用的信号类型。

```python
@staticmethod
def get_available_signals() -> Dict[str, List[str]]
```

返回值示例：
```python
{
    "EEG": ["/eeg", "elements/is_good"],
    "生理信号": ["/ppg", "/batt", "/drlref"],
    "运动数据": ["/acc", "/gyro"]
}
```

#### get_signal_description()
获取信号描述。

```python
@staticmethod
def get_signal_description(signal: str) -> str
```

## DataBuffer

数据缓冲区类。

### 初始化

```python
DataBuffer(max_size: int = 1000)
```

### 方法

#### put()
添加数据到缓冲区。

```python
def put(self, data: OSCMessage) -> bool
```

#### get()
从缓冲区获取数据。

```python
def get(self) -> Optional[OSCMessage]
```

#### get_stats()
获取性能统计信息。

```python
def get_stats(self) -> Optional[Dict]
```

返回的统计信息包括：
- `received_rate`: 数据接收速率（条/秒）
- `dropped_rate`: 数据丢弃速率（条/秒）
- `buffer_usage`: 缓冲区使用率（百分比）

## 使用示例

### 基本用法

```python
from osc_receiver import OSCDataReceiver

# 创建接收器实例
receiver = OSCDataReceiver(ports=[8001, 8002])

# 启动接收
receiver.start()

try:
    # 保持程序运行
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # 优雅退出
    receiver.stop()
```

### 自定义信号处理

```python
from osc_receiver import OSCDataReceiver, SignalManager

# 创建自定义回调函数
def handle_eeg(data):
    print(f"接收到 EEG 数据: {data}")

# 初始化接收器
receiver = OSCDataReceiver(ports=[8001])

# 添加信号处理器
receiver.signal_manager.add_signal("/eeg", handle_eeg)

# 启动接收
receiver.start()
```

### 性能监控

```python
from osc_receiver import OSCDataReceiver

receiver = OSCDataReceiver(ports=[8001])
receiver.start()

# 监控性能
while True:
    stats = receiver.data_buffer.get_stats()
    if stats:
        print(f"性能统计: {stats}")
    time.sleep(1)
```

## 数据类型

### OSCMessage

```python
@dataclass
class OSCMessage:
    port: int          # OSC 端口
    address: str       # 信号地址
    args: tuple        # 数据内容
    timestamp: str     # 时间戳（格式：YYYY-MM-DD HH:MM:SS.mmm）
```

## 异常处理

```python
try:
    receiver = OSCDataReceiver(ports=[8001])
    receiver.start()
except Exception as e:
    logging.error(f"启动失败: {e}")
finally:
    receiver.stop()
```

## 最佳实践

1. 资源管理
   - 使用 with 语句或 try-finally 确保资源正确释放
   - 及时调用 stop() 方法关闭服务

2. 性能优化
   - 适当设置缓冲区大小
   - 根据数据量调整批处理大小
   - 定期监控性能统计

3. 错误处理
   - 捕获并处理异常
   - 实现错误恢复机制
   - 记录详细的错误日志

## 命令行参数

### --ports
指定 OSC 服务器端口列表。
- 类型：List[int]
- 默认值：[8001, 8002]
- 示例：`--ports 8001 8002 8003`

### --save-dir
指定数据保存目录。
- 类型：str
- 默认值：'data'
- 示例：`--save-dir data/session1`

### --debug
启用调试模式。
- 类型：bool flag
- 默认值：False
- 示例：`--debug`

### --all-signals
接收所有信号。
- 类型：bool flag
- 默认值：False
- 示例：`--all-signals` 