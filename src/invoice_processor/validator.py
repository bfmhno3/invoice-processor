import os
import logging
from .invoice import Invoice


logger = logging.getLogger(__name__)


class Validator:
    """
    校验发票数据的规则集
    """
    def __init__(self, invoice_dir: str):
        self.invoice_dir = invoice_dir
        logger.debug(f"validator initialized with directory: {self.invoice_dir}")

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
        logger.info(f"starting validation for invoice from file: '{invoice.original_filename}'")
        self._check_screenshot_exists(invoice)

        if not invoice.validation_errors:
            invoice.is_valid = True
            logger.info(f"validation successful for invoice: '{invoice.original_filename}'")
        else:
            invoice.is_valid = False
            logger.warning(f"validation failed for invoice: '{invoice.original_filename}")

        return invoice

    def _check_screenshot_exists(self, invoice: Invoice) -> bool:
        """
        检查截图文件是否存在
        Args:
            invoice: Invoice 对象

        Returns:
            bool: 截图文件存在返回 True，否则返回 False
        """
        logger.debug(f"checking for screenshot for invoice: '{invoice.original_filename}'")

        base_name, _ = os.path.splitext(invoice.original_filename)
        possible_extensions = ['.jpg', '.png', '.jpeg']
        screenshot_found = False

        for extension in possible_extensions:
            screenshot_name = f"{base_name}{extension}"
            screenshot_path = os.path.join(self.invoice_dir, screenshot_name)
            logger.debug(f"checking for screenshot at path: '{screenshot_path}'")
            if os.path.exists(screenshot_path):
                invoice.screenshot_filename = screenshot_name
                screenshot_found = True
                logger.info(f"found screenshot for invoice: '{screenshot_name}")
                break

        if not screenshot_found:
            error_message: str = "missing corresponding screenshot file"
            invoice.validation_errors.append(error_message)
            logger.warning(f"no screenshot found for invoice: '{invoice.original_filename}'")
