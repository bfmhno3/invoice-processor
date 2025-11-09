from dataclasses import dataclass, field
from datetime import date


@dataclass
class Invoice:
    """
    用于存储单张发票信息的结构化数据类型
    """
    invoice_date: date                                              # 发票日期
    invoice_number: str                                             # 发票号码
    amount: float                                                   # 金额
    buyer: str                                                      # 购买人
    original_filename: str                                          # 发票文件名
    screenshot_filenames: list[str] = field(default_factory=list)    # 发票文件名列表

    @property
    def is_valid(self) -> bool:
        """
        当发票至少有一个关联的购物截图时，即为有效。
        Returns:

        """
        return len(self.screenshot_filenames) > 0

    @property
    def screenshot_nums(self) -> int:
        """
        返回关联购物截图的数量
        Returns:

        """
        return len(self.screenshot_filenames)
