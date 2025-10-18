import pandas as pd
import os
from ..invoice import Invoice


class ExcelGenerator:
    """
    将发票数据列表生成 Excel 文件
    """
    def __init__(self, output_path: str):
        self.output_path = output_path

    def generate(self, invoices: list[Invoice]) -> None:
        valid_invoices = [inv for inv in invoices if inv.is_valid]
        invalid_invoices = [inv for inv in invoices if not inv.is_valid]
        if not valid_invoices:
            print("没有有效的发票可供生成 Excel 文件")
            return

        self._generate_excel_report(valid_invoices, "valid_invoices.xlsx")
        self._generate_excel_report(invalid_invoices, "invalid_invoices.xlsx")

    def _generate_excel_report(self, invoices: list[Invoice], file_name: str) -> None:
        data = [
            {
                "date": inv.invoice_date,
                "amount": inv.amount,
                "buyer": inv.buyer,
                "invoice number": inv.invoice_number,
                "invoice filename": inv.original_filename,
                "screenshot filename": inv.screenshot_filename,
                "valid": inv.is_valid,
                "error": inv.validation_errors,
            }
            for inv in invoices
        ]

        df = pd.DataFrame(data)
        total_amount = df["amount"].sum()
        df.loc["total"] = pd.Series([total_amount], index=["amount"])

        output_file_path = os.path.join(self.output_path, file_name)

        df.to_excel(output_file_path, index=False, engine='openpyxl')
