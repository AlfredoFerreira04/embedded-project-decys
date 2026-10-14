#!/bin/bash

for f in ../target-2/memory_dumps/memory_0.bin ../target-2/memory_dumps/memory_1.bin ../target-2/memory_dumps/memory_2.bin; do
  echo "=== $f ===" >> full_strings_output.txt
  strings -a -n 4 "$f" >> full_strings_output.txt
  echo "" >> full_strings_output.txt
done