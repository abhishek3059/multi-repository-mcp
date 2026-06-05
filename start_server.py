#!/usr/bin/env python
"""Wrapper script to start the multi-repo MCP server."""
import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Import and run the server
from multi_repo_mcp.server import main

if __name__ == "__main__":
    main()
