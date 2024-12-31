import optparse
import socket
import threading
import queue

# 定义端口扫描函数，接受IP地址、端口号和结果队列作为参数
def port_scan(ip, port, result_queue):
    try:
        # 创建一个TCP套接字
        c = socket.socket()
        # 设置超时时间为5秒
        c.settimeout(5)
        # 尝试连接指定的IP和端口，返回连接结果
        r = c.connect_ex((ip, port))
        if r == 0:
            # 如果连接成功，将结果放入结果队列
            result_queue.put(f"{port} 端口开启")
        else:
            # 如果连接失败，将结果放入结果队列
            result_queue.put(f"{port} 端口关闭")
    except Exception as e:
        # 如果发生异常，将错误信息放入结果队列
        result_queue.put(f"扫描 {port} 端口时出错: {e}")
    finally:
        # 关闭套接字
        c.close()

# 定义线程工作函数，接受IP地址、待扫描端口队列和结果队列作为参数
def thread_worker(ip, ports, result_queue):
    while not ports.empty():
        # 从待扫描端口队列中获取一个端口号
        port = ports.get()
        # 调用端口扫描函数进行扫描
        port_scan(ip, port, result_queue)

if __name__ == '__main__':
    # 创建命令行选项解析器
    parser = optparse.OptionParser('<Usage>*** this is usage ***')
    # 添加目标IP地址选项
    parser.add_option('-i', dest='ip', type='string', help='目标IP地址')
    # 添加目标端口范围选项
    parser.add_option('-p', dest='port', type='string', help='目标端口范围（例如：80 或 1-100）')
    # 解析命令行选项
    opts, args = parser.parse_args()
    ip = opts.ip
    port_range = opts.port

    # 检查是否提供了IP地址参数
    if ip is None:
        parser.error("必须提供目标IP地址 (-i)")

    # 检查是否提供了端口范围参数
    if port_range is None:
        parser.error("必须提供目标端口范围 (-p)")

    start_port = 1
    end_port = 65535

    # 检查端口范围是否包含连字符，以确定是单个端口还是端口范围
    if '-' in port_range:
        start_port, end_port = map(int, port_range.split('-'))
    else:
        start_port = int(port_range)
        end_port = start_port

    # 创建一个队列来存储待扫描的端口号
    ports_to_scan = queue.Queue()
    for p in range(start_port, end_port + 1):
        ports_to_scan.put(p)

    # 创建一个列表来存储所有的工作线程
    threads = []
    num_threads = 20  # 设置线程数为20

    # 创建一个队列来存储扫描结果
    result_queue = queue.Queue()

    # 启动指定数量的工作线程
    for _ in range(num_threads):
        t = threading.Thread(target=thread_worker, args=(ip, ports_to_scan, result_queue))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 打印所有扫描结果
    while not result_queue.empty():
        print(result_queue.get())



