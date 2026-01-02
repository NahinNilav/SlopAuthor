#!/usr/bin/env python3
"""
SlopAuthor - Entry point for the autonomous writing agent.

Usage:
    python main.py "Your writing prompt"
    python main.py --template novel "Write a mystery novel"
    python main.py --list-templates
"""

from src.writer import main

if __name__ == "__main__":
    main()
