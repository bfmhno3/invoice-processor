import os
from .invoice import Invoice


class Validator:
    """
    校验发票数据的规则集
    """
    def __init__(self, invoice_dir: str):
        self.invoice_dir = invoice_dir

    def validate(self, invoice: Invoice) -> Invoice:
        """
        对单个 Invoice 对象执行所有校验规则
        直接修改传入的 Invoice 对象，标记其是否有效并添加错误信息
        Args:
            invoice: Invoice 对象

        Returns:
            Invoice: 修改后的 Invoice 对象

        Notes:
            需在调用前检查 invoice 不为 None
        """
        self._check_screenshot_exists(invoice)

        if not invoice.validation_errors:
            invoice.is_valid = True

        return invoice

    def _check_screenshot_exists(self, invoice: Invoice) -> bool:
        """
        检查截图文件是否存在
        Args:
            invoice: Invoice 对象

        Returns:
            bool: 截图文件存在返回 True，否则返回 False
        """
        base_name, _ = os.path.splitext(invoice.original_filename)
        possible_extensions = ['.jpg', '.png', '.jpeg']
        screenshot_found = False
        for extension in possible_extensions:
            screenshot_name = f"{base_name}{extension}"
            screenshot_path = os.path.join(self.invoice_dir, screenshot_name)
            if os.path.exists(screenshot_path):
                invoice.screenshot_filename = screenshot_name
                screenshot_found = True
                break

        if not screenshot_found:
            invoice.validation_errors.append("缺少对应截图文件")
