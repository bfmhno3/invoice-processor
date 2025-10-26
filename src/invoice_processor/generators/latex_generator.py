import os
from ..invoice import Invoice
import pathlib

class LatexGenerator:
    """
    生成一个包含所有发票和截图图像的 LaTeX 文件，使用相对路径
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def _get_tex_header(self) -> str:
        """
        Returns:
            LaTeX 文档的固定头部
        """
        tex_header: str = r"""
            \documentclass[a4paper, oneside]{article}
            \usepackage[a4paper, margin=0.1cm]{geometry}
            \usepackage{graphicx}
            \pagestyle{empty}
            \begin{document}
        """

        return tex_header

    def _get_tex_footer(self) -> str:
        """
        Returns:
            LaTeX 文档的固定尾部
        """
        tex_footer: str = r"""
            \end{document}
        """

        return tex_footer

    def _get_tex_for_invoice(self, invoice: Invoice) -> str:
        """
        为单个发票生成对应的 LaTeX 代码块
        Args:
            invoice: 发票信息

        Returns:
            LaTeX 代码块
        """
        invoice_path: str = "./resources/" + invoice.original_filename
        return rf"""
            \begin{{center}}
                \includegraphics[width=0.99\textheight, height=\textwidth, keepaspectratio, angle=90]{{{invoice_path}}}
            \end{{center}}
            \newpage
        """

    def _get_tex_for_screenshot(self, invoice: Invoice) -> str:
        """
        为购物截图生成发票信息
        Args:
            invoice: 发票信息

        Returns:
            LaTeX 代码块
        """
        if not invoice.is_valid:
            return ""

        screenshot_path: str = "./resources/" + invoice.screenshot_filename
        return rf"""
            \begin{{center}}
                \includegraphics[width=\textwidth, height=\paperheight, keepaspectratio]{{{screenshot_path}}}
            \end{{center}}
            \newpage
        """

    def generate(self, invoices: list[Invoice]):
        """
        生成包含所有有效发票图像的 .tex 文件
        Args:
            invoices:

        Returns:
            无
        """
        tex_context: str = self._get_tex_header()

        for inv in invoices:
            tex_context += self._get_tex_for_invoice(inv)
            tex_context += self._get_tex_for_screenshot(inv)

        tex_context += self._get_tex_footer()

        try:
            with open(self.output_dir + "/invoices.tex", "w", encoding="utf-8") as f:
                f.write(tex_context)
        except IOError as e:
            print(e.get_message())
