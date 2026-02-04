#!/usr/bin/env python3
"""
Mark tasks as complete in implementation or testing documents.
Finds unchecked tasks and marks them as done.
"""

import sys
import re
from pathlib import Path

def mark_task_complete(file_path: str, task_pattern: str, mark_all: bool = False):
    """Mark tasks matching pattern as complete."""

    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()
    lines = content.split('\n')

    updated_lines = []
    marked_count = 0

    for line in lines:
        # Check if line is an unchecked task
        if re.match(r'^(\s*)- \[ \](.*)$', line):
            # Check if it matches the pattern
            if not task_pattern or task_pattern.lower() in line.lower():
                # Mark as complete
                line = re.sub(r'^(\s*)- \[ \]', r'\1- [x]', line)
                marked_count += 1
                print(f"✅ Marked: {line.strip()}")

                if not mark_all:
                    updated_lines.append(line)
                    updated_lines.extend(lines[len(updated_lines):])
                    break

        updated_lines.append(line)

    if marked_count > 0:
        path.write_text('\n'.join(updated_lines))
        print(f"\n✨ Marked {marked_count} task(s) as complete in {file_path}")
    else:
        print(f"⚠️  No matching unchecked tasks found in {file_path}")

def list_tasks(file_path: str, show_completed: bool = False):
    """List all tasks in a file."""

    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()
    lines = content.split('\n')

    incomplete = []
    complete = []

    for line in lines:
        if re.match(r'^(\s*)- \[ \](.*)$', line):
            incomplete.append(line.strip())
        elif re.match(r'^(\s*)- \[x\](.*)$', line):
            complete.append(line.strip())

    if incomplete:
        print(f"\n📋 Incomplete tasks in {file_path}:")
        for task in incomplete:
            print(f"  {task}")

    if show_completed and complete:
        print(f"\n✅ Completed tasks:")
        for task in complete:
            print(f"  {task}")

    if not incomplete and not complete:
        print(f"⚠️  No tasks found in {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  List tasks:      python scripts/mark_task.py list <file-path> [--all]")
        print("  Mark complete:   python scripts/mark_task.py mark <file-path> [task-pattern] [--all]")
        print("\nExamples:")
        print("  python scripts/mark_task.py list docs/v1/auth/3_implementation.md")
        print("  python scripts/mark_task.py mark docs/v1/auth/3_implementation.md 'Task 1.1'")
        print("  python scripts/mark_task.py mark docs/v1/auth/3_implementation.md --all")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        file_path = sys.argv[2]
        show_all = "--all" in sys.argv
        list_tasks(file_path, show_all)

    elif command == "mark":
        file_path = sys.argv[2]
        task_pattern = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else ""
        mark_all = "--all" in sys.argv
        mark_task_complete(file_path, task_pattern, mark_all)

    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'list' or 'mark'")
        sys.exit(1)
