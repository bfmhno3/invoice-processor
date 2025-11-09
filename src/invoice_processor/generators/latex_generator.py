import os
import logging
from PIL import Image
from ..invoice import Invoice
from textwrap import dedent


logger = logging.getLogger(__name__)


class LatexGenerator:
    """
    生成一个包含所有发票和截图图像的 LaTeX 文件，使用相对路径
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        logger.info(f"latex generator initialized with output directory: '{self.output_dir}'")

    def _get_tex_header(self) -> str:
        """
        Returns:
            LaTeX 文档的固定头部
        """
        tex_header: str = dedent(r"""
            \documentclass[a4paper, oneside]{article}
            \usepackage[a4paper, margin=0.1cm]{geometry}
            \usepackage{graphicx}
            \pagestyle{empty}
            \begin{document}
        """)

        return tex_header

    def _get_tex_footer(self) -> str:
        """
        Returns:
            LaTeX 文档的固定尾部
        """
        tex_footer: str = dedent(r"""
            \end{document}
        """)

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
        return dedent(rf"""
            \begin{{center}}
                \includegraphics[width=\textwidth, height=0.49\textheight, keepaspectratio]{{{invoice_path}}}
            \end{{center}}
        """)

    def _get_tex_for_screenshot(self, invoice: Invoice) -> str:
        """
        为购物截图生成发票信息
        Args:
            invoice: 发票信息

        Returns:
            LaTeX 代码块
        """
        if not invoice.is_valid:
            logger.warning(f"skipping screenshot for invalid invoice: '{invoice.original_filename}'")
            return "\\newpage\n"

        width_fraction: float = 0.95 / invoice.screenshot_nums

        graphics_commands = []
        for filename in invoice.screenshot_filenames:
            screenshot_path: str = "./resources/" + filename
            command: str = (
                f"\\includegraphics[width={width_fraction:.2f}\\textwidth, "
                f"height=0.49\\textheight, keepaspectratio]{{{screenshot_path}}}"
            )
            graphics_commands.append(command)

        all_graphics: str = "\\quad".join(graphics_commands)

        return dedent(rf"""
            \begin{{center}}
                {all_graphics}
            \end{{center}}
            \newpage
        """)

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
        output_path: str = os.path.join(self.output_dir, "invoices.tex")
        logger.info(f"writing latex file: '{output_path}")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(tex_context)
            logger.info(f"successfully generated latex file at '{output_path}'")
        except IOError as e:
            logger.error(f"failed to write latex file to '{output_path}': {e}", exc_info=True)
