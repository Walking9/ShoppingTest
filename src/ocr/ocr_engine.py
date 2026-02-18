import os
import numpy as np
from paddleocr import PaddleOCR
from loguru import logger
from typing import List, Dict, Any, Optional

class OcrEngine:
    """封装 PaddleOCR 离线推理逻辑。"""

    def __init__(self, lang: str = 'ch', use_gpu: bool = False):
        """
        初始化 OCR 引擎。
        :param lang: 语言，'ch' 代表中文
        :param use_gpu: 是否使用 GPU 加速
        """
        # 模型存储路径定义（相对于项目根目录）
        self.model_dir = os.path.abspath("data/models")
        
        logger.info(f"正在初始化 PaddleOCR 引擎 (lang={lang}, use_gpu={use_gpu})...")
        
        try:
            # 初始化 PaddleOCR 实例
            # 这里的参数调优旨在降低移动端推理延迟
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=lang,
                use_gpu=use_gpu,
                show_log=False,
                # 强制指定本地模型路径，实现完全离线
                det_model_dir=os.path.join(self.model_dir, "det/ch_PP-OCRv3_det_infer"),
                rec_model_dir=os.path.join(self.model_dir, "rec/ch_PP-OCRv3_rec_infer"),
                cls_model_dir=os.path.join(self.model_dir, "cls/ch_ppocr_mobile_v2.0_cls_infer")
            )
            logger.success("OCR 引擎初始化成功。")
        except Exception as e:
            logger.warning(f"OCR 初始化异常 (可能是由于模型文件未找到): {e}")
            logger.info("系统将尝试使用默认模式运行（可能会触发自动下载）...")
            # 回退模式：仅用于首次运行或调试
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=use_gpu, show_log=False)

    def recognize(self, img: np.ndarray) -> List[Dict[str, Any]]:
        """
        执行文字识别推理。
        :param img: OpenCV 图像矩阵 (NumPy 数组)
        :return: 格式化的识别结果列表
        """
        if img is None:
            return []

        logger.debug("开始 OCR 推理...")
        try:
            # 执行识别，返回格式: [[[ [coords], (text, score) ], ...]]
            results = self.ocr.ocr(img, cls=True)
            
            parsed_results = []
            if not results or results[0] is None:
                return parsed_results

            for line in results[0]:
                coords = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text = line[1][0]
                confidence = line[1][1]
                
                # 计算中心点坐标
                center_x = int(sum(p[0] for p in coords) / 4)
                center_y = int(sum(p[1] for p in coords) / 4)
                
                parsed_results.append({
                    "text": text,
                    "confidence": round(float(confidence), 4),
                    "center": {"x": center_x, "y": center_y},
                    "box": coords
                })
            
            logger.debug(f"识别完成，发现 {len(parsed_results)} 行文本。")
            return parsed_results

        except Exception as e:
            logger.error(f"OCR 推理失败: {e}")
            return []
