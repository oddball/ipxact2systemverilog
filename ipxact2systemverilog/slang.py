#!/usr/bin/env python3

import sys
import os
import pyslang


def check_file(file_path):
    if not (file_path.endswith(".sv") or file_path.endswith(".svh")):
        print(f"⏭️  Skipping {file_path}: not an .sv or .svh file")
        return False

    if not os.path.isfile(file_path):
        print(f"❌ Error: File '{file_path}' does not exist.")
        return False

    print(f"\n🔍 Checking {file_path}...")

    tree = pyslang.SyntaxTree.fromFile(file_path)
    diagnostics = tree.diagnostics

    if diagnostics:
        print(f"❌ Syntax errors in {file_path}:")
        for diag in diagnostics:
            print(f"  - {diag}")
        return False

    print(f"✅ {file_path} is syntactically valid.")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: check_sv_syntax.py <file1.sv> [file2.svh ...]")
        sys.exit(1)

    files = sys.argv[1:]
    all_passed = True

    for file_path in files:
        if not check_file(file_path):
            all_passed = False

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
