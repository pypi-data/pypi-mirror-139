"""Strangeworks Braket SDK"""
import importlib.metadata

__version__ = importlib.metadata.version("strangeworks-braket")

from strangeworks.braket.utils.serialize import braket_to_sw
