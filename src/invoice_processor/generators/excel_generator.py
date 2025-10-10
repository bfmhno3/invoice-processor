import pandas as pd
from ..invoice import Invoice


class ExcelGenerator:
    """
    将发票数据列表生成 Excel 文件
    """
    def __init__(self, output_path: str):
        self.output_path = output_path

    def generate(self, invoices: list[Invoice]) -> None:
        valid_invoices = [inv for inv in invoices if inv.is_valid]
        if not valid_invoices:
            print("没有有效的发票可供生成 Excel 文件")
            return

        data = [
            {
                "日期": inv.invoice_date,
                "金额": inv.amount,
                "购买人": inv.buyer,
                "发票号码": inv.invoice_number,
                "发票文件名": inv.original_filename,
                "是否有效": inv.is_valid,
                "错误信息": inv.validation_errors,
            }
            for inv in valid_invoices
        ]

        df = pd.DataFrame(data)
        total_amount = df["金额"].sum()
        df.loc['总计'] = pd.Series([total_amount], index=['金额'])

        df.to_excel(self.output_path, index=False, engine='openpyxl')
        print(f"Excel 文件已生成: {self.output_path}")
