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
        self._find_screenshots(invoice)

        if not invoice.is_valid:
            logger.error(f"no screenshot found for invoice: '{invoice.original_filename}")

        return invoice

    def _find_screenshots(self, invoice: Invoice) -> None:
        """
        查找与发票对应的截图文件，并更新 invoice.screenshot_filenames 列表
        支持两种命名规则：
        1. 与发票文件具有相同的 basename
        2. 在发票文件 basename 后附加 '-1', '-2', ... 后缀的截图。
        Args:
            invoice:

        Returns:

        """
        logger.debug(f"checking for screenshots for invoice: '{invoice.original_filename}'")
        basename, _ = os.path.splitext(invoice.original_filename)
        possible_extensions = ['.jpg', '.png', '.jpeg']

        # 1. 检查具有相同 basename 的文件
        for extension in possible_extensions:
            screenshot_name = f"{basename}{extension}"
            screenshot_path = os.path.join(self.invoice_dir, screenshot_name)
            if os.path.exists(screenshot_path):
                invoice.screenshot_filenames.append(screenshot_name)
                logger.info(f"found screenshot: '{screenshot_name}' for invoice: '{invoice.original_filename}'")

        # 2. 检查带有 '-1', '-2', ... 后缀的文件
        i = 1
        while True:
            found_in_iteration = False
            suffixed_basename = f"{basename}-{i}"
            for extension in possible_extensions:
                screenshot_name = f"{suffixed_basename}{extension}"
                screenshot_path = os.path.join(self.invoice_dir, screenshot_name)
                if os.path.exists(screenshot_path):
                    invoice.screenshot_filenames.append(screenshot_name)
                    logger.info(f"found screenshot: '{screenshot_name}' for invoice: '{invoice.original_filename}'")
                    found_in_iteration = True

            if not found_in_iteration:
                break

            i += 1

