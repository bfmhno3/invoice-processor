import os
import logging
from .invoice import Invoice
from .parser import FilenameParser
from .validator import Validator
from .generators.excel_generator import ExcelGenerator
from .generators.latex_generator import LatexGenerator


logger = logging.getLogger(__name__)


def process_invoices(directory: str, output_dir: str):
    """
    处理指定目录下的所有发票文件
    Args:
        directory: 发票文件存放目录
        output_dir: 处理结果输出目录

    Returns:

    """
    parser = FilenameParser()
    validator = Validator(directory)

    all_invoices: list[Invoice] = []
    # 数量统计
    total_invoices_count: int = 0
    parsed_invoices_count: int = 0
    skipped_invoices_count: int = 0

    logger.info(f"starting to process invoices in directory: {directory}")
    for filename in os.listdir(directory):
        if filename.split('.')[-1] == 'pdf':
            total_invoices_count += 1
            invoice: Invoice = parser.parse(filename)
            if invoice:
                parsed_invoices_count += 1
                validated_invoice: Invoice = validator.validate(invoice)
                all_invoices.append(validated_invoice)
                logger.info(f"successfully parsed and validated invoice: {filename}")
            else:
                skipped_invoices_count += 1
                logger.warning(f"filename '{filename}' is not in correct format, skipped")

    logger.info(
        f"total PDF files found: {total_invoices_count}, parsed: {parsed_invoices_count}, skipped: {skipped_invoices_count}"
    )

    # 输出校验结果
    invalid_count: int = sum(1 for inv in all_invoices if inv.is_valid)
    logger.info(f"validation completed. total invoices: {invalid_count}")
    if invalid_count > 0:
        for inv in all_invoices:
            if not inv.is_valid:
                logger.error(f"files '{inv.original_filename}' is invalid")

    # 生成输出
    logger.info("starting to generate excel report")
    excel_gen = ExcelGenerator(output_dir)
    excel_gen.generate(all_invoices)
    logger.info("excel report generated successfully")

    logger.info("starting to generate LaTeX report")
    latex_gen = LatexGenerator(output_dir)
    latex_gen.generate(all_invoices)
    logger.info("LaTeX report generated successfully")

    logger.info("all processing completed")
