import cv2
import numpy as np
from loguru import logger
from typing import Optional

class ImageProcessor:
    """图像预处理流水线，用于提升 OCR 识别率。"""

    @staticmethod
    def to_gray(img: np.ndarray) -> np.ndarray:
        """转换为灰度图。"""
        if len(img.shape) == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    @staticmethod
    def denoise(img: np.ndarray) -> np.ndarray:
        """应用中值滤波降噪。"""
        # 使用 3x3 核进行中值模糊，去除孤立噪点
        return cv2.medianBlur(img, 3)

    @staticmethod
    def apply_threshold(img: np.ndarray) -> np.ndarray:
        """使用自适应阈值处理 (Adaptive Thresholding)。"""
        # 首先确保是灰度图
        gray = ImageProcessor.to_gray(img)
        # 使用自适应高斯阈值，能更好地处理局部光照和背景复杂的 UI
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        return binary

    def process_for_ocr(self, img: np.ndarray, use_binary: bool = False) -> np.ndarray:
        """
        核心流水线接口。
        :param img: 原始 BGR 图像
        :param use_binary: 是否执行二值化（针对极简背景推荐开启，复杂背景可仅用灰度）
        """
        logger.debug("开始执行图像预处理流水线...")
        
        # 1. 基础转换
        processed = self.to_gray(img)
        
        # 2. 降噪
        processed = self.denoise(processed)
        
        # 3. 可选二值化
        if use_binary:
            processed = self.apply_threshold(processed)
            
        return processed

    def save_debug_img(self, img: np.ndarray, name: str = "processed"):
        """保存中间图像用于可视化调试。"""
        path = f"logs/debug_{name}.png"
        cv2.imwrite(path, img)
        logger.info(f"调试图像已保存: {path}")
