# Interface definitions for the clock application

from .theme_interface import ITheme
from .time_provider_interface import ITimeProvider
from .renderer_interface import IRenderer
from .window_manager_interface import IWindowManager

__all__ = ['ITheme', 'ITimeProvider', 'IRenderer', 'IWindowManager']