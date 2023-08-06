"""Strangeworks Rigetti SDK"""
import importlib.metadata

__version__ = importlib.metadata.version("strangeworks-rigetti")

from strangeworks.rigetti.utils.serialize import rigetti_to_sw
