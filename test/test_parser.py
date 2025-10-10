import pytest
from datetime import date
from invoice_processor.parser import FilenameParser
from invoice_processor.invoice import Invoice


@pytest.fixture
def parser():
    return FilenameParser()


def test_parse_valid_filename(parser):
    filename: str = "2023-10-15-abc-19_9-12345678901234567890.pdf"
    result = parser.parse(filename)

    assert result is not None
    assert isinstance(result, Invoice)
    assert result.invoice_date == date(2023, 10, 15)
    assert result.invoice_number == '12345678901234567890'
    assert result.amount == 19.9
    assert result.buyer == 'abc'
    assert result.original_filename == filename
    assert result.screenshot_filename == ''
    assert result.is_valid == False
    assert result.validation_errors == []


@pytest.mark.parametrize("invalid_filename", [
    # 正确格式：YYYY-MM-DD-<buyer>-<amount>-<invoice_number>.pdf
    "2023-1-15-abc-19_9-12345678901234567890.pdf",  # 月份不是两位数
    "2023-10-1-abc-19_9-12345678901234567890.pdf",  # 日不是两位数
    "23-10-15-abc-19_9-12345678901234567890.pdf",  # 年份不是四位数
    "2023_10_15-abc-19_9-12345678901234567890.pdf",  # 日期分隔符错误
    "2023-10-15-19_9-12345678901234567890.pdf",  # 缺少购买方
    "2023-10-15-abc-12345678901234567890.pdf",  # 缺少金额
    "2023-10-15-abc-19_9.pdf",  # 缺少发票号码
    "2023-10-15-abc-19.9-12345678901234567890.pdf",  # 金额中小数点格式错误
    "2023-10-15-abc-19_9-12345678901234567890.txt",  # 文件扩展名错误
    "just_a_random_string.pdf",  # 完全不匹配的格式
    "2023-10-15-abc-19_9-12345678901234567890",  # 缺少文件扩展名
])
def test_parse_invalid_filename(parser, invalid_filename):
    result = parser.parse(invalid_filename)
    assert result is None
