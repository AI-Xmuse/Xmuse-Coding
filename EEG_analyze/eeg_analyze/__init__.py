"""
EEG-Analyze: 一个用于脑电信号分析的Python工具包
"""

from .analyzer import EEGAnalyzer
from .visualizer import EEGVisualizer
from .preprocessor import preprocess_eeg, augment_eeg
from .feature_extractor import extract_features, spectral_analysis
from .data_loader import loadEEGData

__version__ = '0.1.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

__all__ = [
    'EEGAnalyzer',
    'EEGVisualizer',
    'preprocess_eeg',
    'augment_eeg',
    'extract_features',
    'spectral_analysis',
    'loadEEGData'
] 