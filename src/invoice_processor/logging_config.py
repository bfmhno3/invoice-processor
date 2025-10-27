import logging
import os
from datetime import datetime


def setup_logging(logs_dir: str = "logs", log_level = logging.INFO) -> None:
    """
    配置日志记录器
    Args:
        log_level: 最低日志级别

    Returns:
        None
    """
    # 创建 logs 目录
    os.makedirs(logs_dir, exist_ok=True)

    # 生成基于当前时间的日志文件名
    # 例如：2025-10-27_13-13-30.log
    log_filename: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_file_path: str = os.path.join(logs_dir, log_filename)

    # 配置日志
    logging.basicConfig(
        level=log_level, # 设置最低日志级别
        # 定义日志格式
        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # 指定日志处理器
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"), # 输出到文件
            logging.StreamHandler(),  # 输出到控制台
        ],
    )

    logging.info("logging system is running, and the log files are located in: %s",
                 os.path.join(os.getcwd(), log_file_path))
