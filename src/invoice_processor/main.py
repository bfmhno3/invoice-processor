import os
from .invoice import Invoice
from .parser import FilenameParser
from .validator import Validator
from .generators.excel_generator import  ExcelGenerator


def process_invoices(directory: str, output_dir: str, template_path: str):
    """
    处理指定目录下的所有发票文件
    Args:
        directory: 发票文件存放目录
        output_dir: 处理结果输出目录
        template_path: 模板文件路径

    Returns:

    """
    parser = FilenameParser()
    validator = Validator(directory)

    all_invoices: list[Invoice] = []

    for filename in os.listdir(directory):
        if filename.split('.')[-1] == 'pdf':
            invoice: Invoice = parser.parse(filename)
            if invoice:
                validated_invoice: Invoice = validator.validate(invoice)
                all_invoices.append(validated_invoice)
            else:
                print(f"文件名 '{filename}' 格式不正确，已跳过")

    # 输出校验结果
    print("\n--- 校验结果 ---")
    for inv in all_invoices:
        if not inv.is_valid:
            print(f"文件 '{inv.original_filename}' 无效: {', '.join(inv.validation_errors)}")
    print("------------------\n")

    # 生成输出
    excel_gen = ExcelGenerator(output_dir)
    excel_gen.generate(all_invoices)
