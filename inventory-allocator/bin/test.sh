#!/bin/bash
if [[ ! "$(command -v mypy)" ]]; then
  echo "mypy is not installed. Run \"pip3 install mypy\""
fi

mypy src && python3 src/test_inventory_allocator.py
