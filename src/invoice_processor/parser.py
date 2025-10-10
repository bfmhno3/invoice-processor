import re
from datetime import date
from .invoice import Invoice


class FilenameParser:
    """
    从固定格式的文件名中解析发票信息
    发票信息格式示例：YYYY-MM-DD-<buyer>-<amount>-<invoice_number>.pdf
    """
    FILE_PATTERN = re.compile(
        r'^(?P<year>\d{4})-'
        r'(?P<month>\d{2})-'
        r'(?P<day>\d{2})-'
        r'(?P<buyer>[a-z]+)-'
        r'(?P<amount>\d+(?:_\d+)?)-'
        r'(?P<invoice_number>\d+)$'
    )

    def parse(self, filename: str) -> Invoice | None:
        """
        解析文件吗，提取发票信息
        Args:
            filename: 发票文件名（包含扩展名）

        Returns:
            Invoice: 解析成功
            None: 解析失败
        """
        # 去掉扩展名
        name, _ = filename.strip().rsplit('.', 1)
        match = self.FILE_PATTERN.match(name)
        if not match:
            return None

        try:
            year = int(match.group('year'))
            month = int(match.group('month'))
            day = int(match.group('day'))
            invoice_date = date(year, month, day)
            amount = float(match.group('amount').replace('_', '.'))
            buyer = match.group('buyer')
            invoice_number = match.group('invoice_number')
            return Invoice(
                invoice_date=invoice_date,
                invoice_number=invoice_number,
                amount=amount,
                buyer=buyer,
                original_filename=filename,
                screenshot_filename='',
                is_valid=False
            )
        except (ValueError, IndexError) as e:
            return None
