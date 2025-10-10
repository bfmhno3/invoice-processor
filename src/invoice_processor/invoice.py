from dataclasses import dataclass, field
from datetime import date


@dataclass
class Invoice:
    """
    用于存储单张发票信息的结构化数据类型
    """
    invoice_date: date                                          # 发票日期
    invoice_number: str                                         # 发票号码
    amount: float                                               # 金额
    buyer: str                                                  # 购买人
    original_filename: str                                      # 发票文件名
    screenshot_filename: str                                    # 购物截图文件名
    is_valid: bool = False                                      # 是否有效
    validation_errors: list[str] = field(default_factory=list)  # 验证错误列表
