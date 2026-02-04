#!/usr/bin/env python3
"""
Initialize a new feature with all development phase templates.
Creates a structured directory with requirements, design, implementation, and testing docs.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def create_feature_docs(feature_name: str, output_dir: str = "docs/v1"):
    """Create feature documentation structure from templates."""

    # Find templates directory
    templates_dir = Path("docs/templates")
    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        sys.exit(1)

    # Create output directory
    feature_dir = Path(output_dir) / feature_name
    feature_dir.mkdir(parents=True, exist_ok=True)

    # Copy and customize templates
    templates = {
        "requirements.md": "1_requirements.md",
        "design.md": "2_design.md",
        "implementation.md": "3_implementation.md",
        "testing.md": "4_testing.md"
    }

    for src_name, dest_name in templates.items():
        src_path = templates_dir / src_name
        dest_path = feature_dir / dest_name

        if src_path.exists():
            content = src_path.read_text()

            # Add changelog section
            content += f"\n\n---\n\n## Changelog\n\n### {datetime.now().strftime('%Y-%m-%d')}\n- Initial version\n"

            dest_path.write_text(content)
            print(f"✅ Created {dest_path}")
        else:
            print(f"⚠️  Template not found: {src_path}")

    # Create CHANGELOG.md
    changelog_path = feature_dir / "CHANGELOG.md"
    changelog_content = f"""# {feature_name} - Changelog

## {datetime.now().strftime('%Y-%m-%d')}
### Added
- Initialized feature documentation structure

"""
    changelog_path.write_text(changelog_content)
    print(f"✅ Created {changelog_path}")

    print(f"\n✨ Feature '{feature_name}' initialized at {feature_dir}")
    print("\nNext steps:")
    print(f"1. Fill out {feature_dir}/1_requirements.md")
    print(f"2. Design the solution in {feature_dir}/2_design.md")
    print(f"3. Plan implementation in {feature_dir}/3_implementation.md")
    print(f"4. Define tests in {feature_dir}/4_testing.md")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_feature.py <feature-name> [output-dir]")
        print("Example: python scripts/init_feature.py user-authentication docs/v1")
        sys.exit(1)

    feature_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs/v1"

    create_feature_docs(feature_name, output_dir)
