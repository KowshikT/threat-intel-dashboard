#!/usr/bin/env python3
"""Test single fetcher in isolation"""
import sys
sys.path.insert(0, '/home/albatross/threat-intel-dashboard')

print("=" * 60)
print("TEST: Running URLhaus fetcher with single connection pattern")
print("=" * 60)

from fetcher.abusech import fetch_abusech_data
fetch_abusech_data()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
