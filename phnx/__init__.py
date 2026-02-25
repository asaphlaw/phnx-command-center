"""
PHNX - Integrated AI Architecture

Usage:
    from phnx import PHNXCore
    
    phnx = PHNXCore()
    phnx.remember("Important information")
    result = phnx.browse("Task description")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.phnx_core import PHNXCore

__all__ = ['PHNXCore']
__version__ = '2.0.0'
