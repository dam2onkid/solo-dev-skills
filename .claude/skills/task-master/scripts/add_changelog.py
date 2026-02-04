#!/usr/bin/env python3
"""
Add changelog entries to feature documents or CHANGELOG.md.
Tracks changes to requirements, design, implementation, and testing.
"""

import sys
from pathlib import Path
from datetime import datetime

def add_changelog_entry(file_path: str, entry_type: str, description: str):
    """Add a changelog entry to a document."""

    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()
    today = datetime.now().strftime('%Y-%m-%d')

    # Find or create changelog section
    if "## Changelog" not in content:
        content += f"\n\n---\n\n## Changelog\n\n### {today}\n- {entry_type}: {description}\n"
    else:
        # Check if today's section exists
        if f"### {today}" in content:
            # Add to today's entries
            lines = content.split('\n')
            changelog_idx = None
            for i, line in enumerate(lines):
                if line.strip() == f"### {today}":
                    changelog_idx = i
                    break

            if changelog_idx is not None:
                # Find the next section or end of changelog
                insert_idx = changelog_idx + 1
                for i in range(changelog_idx + 1, len(lines)):
                    if lines[i].strip().startswith("###") or lines[i].strip().startswith("##"):
                        insert_idx = i
                        break
                    if lines[i].strip() and not lines[i].strip().startswith("-"):
                        insert_idx = i
                        break
                else:
                    insert_idx = len(lines)

                lines.insert(insert_idx, f"- {entry_type}: {description}")
                content = '\n'.join(lines)
        else:
            # Add new date section
            lines = content.split('\n')
            changelog_idx = None
            for i, line in enumerate(lines):
                if line.strip() == "## Changelog":
                    changelog_idx = i
                    break

            if changelog_idx is not None:
                lines.insert(changelog_idx + 1, "")
                lines.insert(changelog_idx + 2, f"### {today}")
                lines.insert(changelog_idx + 3, f"- {entry_type}: {description}")
                content = '\n'.join(lines)

    path.write_text(content)
    print(f"✅ Added changelog entry to {file_path}")
    print(f"   {entry_type}: {description}")

def add_to_feature_changelog(feature_dir: str, entry_type: str, description: str):
    """Add entry to feature's CHANGELOG.md."""

    feature_path = Path(feature_dir)
    if not feature_path.exists():
        print(f"❌ Feature directory not found: {feature_dir}")
        sys.exit(1)

    changelog_path = feature_path / "CHANGELOG.md"
    today = datetime.now().strftime('%Y-%m-%d')

    if not changelog_path.exists():
        # Create new changelog
        content = f"""# {feature_path.name} - Changelog

## {today}
### {entry_type}
- {description}

"""
        changelog_path.write_text(content)
        print(f"✅ Created CHANGELOG.md with entry")
    else:
        content = changelog_path.read_text()

        if f"## {today}" in content:
            # Add to today's section
            lines = content.split('\n')
            date_idx = None
            for i, line in enumerate(lines):
                if line.strip() == f"## {today}":
                    date_idx = i
                    break

            if date_idx is not None:
                # Check if entry type section exists
                type_idx = None
                for i in range(date_idx + 1, len(lines)):
                    if lines[i].strip() == f"### {entry_type}":
                        type_idx = i
                        break
                    if lines[i].strip().startswith("##"):
                        break

                if type_idx is not None:
                    # Add to existing type section
                    lines.insert(type_idx + 1, f"- {description}")
                else:
                    # Create new type section
                    insert_idx = date_idx + 1
                    lines.insert(insert_idx, f"### {entry_type}")
                    lines.insert(insert_idx + 1, f"- {description}")

                content = '\n'.join(lines)
        else:
            # Add new date section at top
            lines = content.split('\n')
            # Find first ## section
            first_section_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("##"):
                    first_section_idx = i
                    break

            if first_section_idx is not None:
                lines.insert(first_section_idx, "")
                lines.insert(first_section_idx, "")
                lines.insert(first_section_idx, f"- {description}")
                lines.insert(first_section_idx, f"### {entry_type}")
                lines.insert(first_section_idx, f"## {today}")
                content = '\n'.join(lines)

        changelog_path.write_text(content)
        print(f"✅ Updated CHANGELOG.md")

    print(f"   {entry_type}: {description}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Document:  python scripts/add_changelog.py doc <file-path> <type> <description>")
        print("  Feature:   python scripts/add_changelog.py feature <feature-dir> <type> <description>")
        print("\nTypes: Added, Changed, Fixed, Removed, Updated")
        print("\nExamples:")
        print("  python scripts/add_changelog.py doc docs/v1/auth/1_requirements.md Changed 'Updated success criteria'")
        print("  python scripts/add_changelog.py feature docs/v1/auth Added 'OAuth2 provider support'")
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]
    entry_type = sys.argv[3]
    description = ' '.join(sys.argv[4:])

    if command == "doc":
        add_changelog_entry(target, entry_type, description)
    elif command == "feature":
        add_to_feature_changelog(target, entry_type, description)
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'doc' or 'feature'")
        sys.exit(1)
