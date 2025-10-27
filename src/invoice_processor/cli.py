import click
import os
from .main import process_invoices
import logging
from .logging_config import setup_logging


@click.command()
@click.option(
    '--directory', '-d', # 参数名
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True), # 已存在的目录
    help='包含发票文件和截图的目录'
)
@click.option(
    '--output', '-o', # 输出目录，默认当前目录
    default='.',
    type=click.Path(file_okay=False, dir_okay=True),
    help='生成的报告（Excel, TeX）的输出目录'
)
def main(directory: str, output: str):
    """
    一个用于解析发票文件名并生成报销报告的工具
    Args:
        directory: 发票和截图文件所存在的目录
        output: 输出目录
    Returns:
        None
    """
    setup_logging() # 初始化日志系统
    logging.info(f"input directory: {directory}")
    logging.info(f"output directory: {output}")

    try:
        process_invoices(directory, output)
        logging.info("processing successful!")
    except Exception as e:
        logging.error(f"processing failed: {e}")
