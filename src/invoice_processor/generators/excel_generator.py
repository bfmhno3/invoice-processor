import pandas as pd
import logging
import os
from ..invoice import Invoice


logger: logging.Logger = logging.getLogger(__name__)


class ExcelGenerator:
    """
    将发票数据列表生成 Excel 文件
    """
    def __init__(self, output_path: str):
        self.output_path = output_path
        logger.info(f"excel report file output directory: '{output_path}'")

    def generate(self, invoices: list[Invoice]) -> None:
        logger.info(f"starting excel generation process")

        if not invoices:
            logger.warning("no invoices to process")
            return

        logger.info(f"found {len(invoices)} invoices to process")
        logger.info(f"generating report for all invoices")
        self._generate_excel_report(invoices, "invoices.xlsx")

        logger.info("excel generation process finished")

    def _generate_excel_report(self, invoices: list[Invoice], file_name: str) -> None:
        logger.info(f"generating excel report for {len(invoices)} invoices")
        data = [
            {
                "date": inv.invoice_date,
                "amount": inv.amount,
                "buyer": inv.buyer,
                "invoice number": inv.invoice_number,
                "invoice filename": inv.original_filename,
                "screenshot filenames": inv.screenshot_filenames,
                "valid": inv.is_valid,
            }
            for inv in invoices
        ]

        df = pd.DataFrame(data)
        total_amount = df["amount"].sum()
        total_row = pd.DataFrame([{"amount": total_amount}], index=["total"])
        df = pd.concat([df, total_row])

        output_file_path = os.path.join(self.output_path, file_name)
        logger.info(f"saving excel report to '{output_file_path}'")

        try:
            df.to_excel(output_file_path, index=True, engine="openpyxl")
            logger.info(f"successfully generated excel report: '{output_file_path}'")
        except Exception as e:
            logger.error(f"failed to generate excel report: '{output_file_path}': {e}", exc_info=True)
