import click
import os
from .main import process_invoices


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
@click.option(
    '--template', '-t',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True), # 已存在的文件
    help='LaTeX报告模板文件的路径'
)
def main(directory: str, output: str, template: str):
    """
    一个用于解析发票文件名并生成报销报告的工具
    Args:
        directory: 发票和截图文件所存在的目录
        output: 输出目录
        template: 模板目录

    Returns:

    """
    click.echo(f"输入目录：{directory}")
    click.echo(f"输出目录：{output}")
    click.echo(f"模板文件：{template}")

    try:
        process_invoices(directory, output, template)
        click.secho("\n处理成功！", fg='green')
    except Exception as e:
        click.secho(f"\n处理失败: {e}", fg='red')
