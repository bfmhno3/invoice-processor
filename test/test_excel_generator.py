import pytest
import pandas as pd
import numpy as np
from datetime import date

from invoice_processor.invoice import Invoice
from invoice_processor.generators.excel_generator import ExcelGenerator


@pytest.fixture
def sample_invoices():
    return [
        Invoice(
            invoice_date=date(2023, 10, 23),
            amount=50.0,
            buyer="abc",
            invoice_number="12345678901234567890",
            original_filename="2023-10-23-abc-50_0-12345678901234567890.pdf",
            screenshot_filename="2023-10-23-abc-50_0-12345678901234567890.png",
            is_valid=True,
        ),
        Invoice(
            invoice_date=date(2023, 10, 24),
            amount=75.5,
            buyer="def",
            invoice_number="09876543210987654321",
            original_filename="2023-10-24-def-75_5-09876543210987654321.pdf",
            screenshot_filename="2023-10-24-def-75_5-09876543210987654321.png",
            is_valid=True,
        ),
        Invoice(
            invoice_date=date(2023, 10, 2),
            amount=70.5,
            buyer="main",
            invoice_number="09876543290987654321",
            original_filename="2023-10-24-main-75_5-09876543210987654321.pdf",
            screenshot_filename="2023-10-24-main-75_5-09876543210987654321.png",
            is_valid=True,
        ),
    ]


def test_excel_generator_creates_valid_file(tmp_path, sample_invoices):
    """
    测试 ExcelGenerator 是否正确生成 Excel 文件
    Args:
        tmp_path:
        sample_invoices:

    Returns:

    """
    output_file = tmp_path / "invoices.xlsx"
    generator = ExcelGenerator(str(output_file))

    generator.generate(sample_invoices)

    # 读取生成的 Excel 文件进行验证
    df = pd.read_excel(output_file)

    assert len(df) == 4
    assert list(df.columns) == [
        "日期",
        "金额",
        "购买人",
        "发票号码",
        "发票文件名",
        "截图文件名",
        "是否有效",
        "错误信息",
    ]

    # 验证第一行数据
    first_row = df.iloc[0]
    assert first_row["日期"] == pd.Timestamp(date(2023, 10, 23))
    assert first_row["发票号码"] == "12345678901234567890"
    assert first_row["金额"] == 50.0
    assert first_row["购买人"] == "abc"
    assert first_row["发票文件名"] == "2023-10-23-abc-50_0-12345678901234567890.pdf"
    assert first_row["截图文件名"] == "2023-10-23-abc-50_0-12345678901234567890.png"
    assert first_row["是否有效"] == 1.0
    assert first_row["错误信息"] == "[]"
    assert df.iloc[-1]["金额"] == 196.0


def test_excel_generator_no_valid_invoices(tmp_path):
    """
    测试当没有有效发票时，Excel 文件不会生成
    Args:
        tmp_path:

    Returns:

    """
    output_file = tmp_path / "invoices.xlsx"
    generator = ExcelGenerator(str(output_file))

    invalid_invoices = [
        Invoice(
            invoice_date=date(2023, 10, 23),
            amount=50.0,
            buyer="abc",
            invoice_number="12345678901234567890",
            original_filename="2023-10-23-abc-50_0-12345678901234567890.pdf",
            screenshot_filename="",
            is_valid=False,
            validation_errors=["缺少对应截图文件"],
        )
    ]

    generator.generate(invalid_invoices)

    assert not output_file.exists()
