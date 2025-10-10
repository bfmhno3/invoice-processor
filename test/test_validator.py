import pytest
from invoice_processor.validator import Validator
from invoice_processor.invoice import Invoice
from datetime import date


def test_validator_with_screenshot(tmp_path):
    """
    测试当截图文件存在时，校验结果为有效
    Args:
        tmp_path:

    Returns:

    """
    invoice_dir = tmp_path
    invoice_filename = "2023-10-23-abc-50_0-12345678901234567890.pdf"
    screenshot_filename = "2023-10-23-abc-50_0-12345678901234567890.png"
    (invoice_dir / screenshot_filename).touch()  # / 操作符被 pathlib 模块重载用于拼接路径

    invoice = Invoice(
        invoice_date=date(2023, 10, 23),
        amount=50.0,
        buyer='abc',
        invoice_number='12345678901234567890',
        original_filename='2023-10-23-abc-50_0-12345678901234567890.pdf',
        screenshot_filename='',
    )

    validator = Validator(str(invoice_dir))
    result = validator.validate(invoice)

    assert result.is_valid is True
    assert len(result.validation_errors) == 0
    assert result.screenshot_filename == screenshot_filename


def test_validator_missing_screenshot(tmp_path):
    """
    测试当截图文件不存在时，校验结果为无效
    Args:
        tmp_path:

    Returns:

    """
    invoice_dir = tmp_path
    invoice_filename = "2023-10-23-abc-50_0-12345678901234567890.pdf"

    invoice = Invoice(
        invoice_date=date(2023, 10, 23),
        amount=50.0,
        buyer="abc",
        invoice_number="12345678901234567890",
        original_filename="2023-10-23-abc-50_0-12345678901234567890.pdf",
        screenshot_filename="",
    )

    validator = Validator(str(invoice_dir))
    result = validator.validate(invoice)

    assert result.is_valid is False
    assert len(result.validation_errors) == 1
    assert "缺少对应截图文件" in result.validation_errors[0]
