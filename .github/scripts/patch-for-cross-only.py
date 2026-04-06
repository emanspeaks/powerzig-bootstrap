#!/usr/bin/env python3
"""Patch zig-bootstrap build script to skip host build stages if out/host/bin/zig exists."""
import sys, pathlib

script_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'build')
lines = script_path.read_text().splitlines(keepends=True)

first_cmake = next((i for i, l in enumerate(lines) if l.lstrip().startswith('cmake ')), None)
cross_marker = next((i for i, l in enumerate(lines) if '# Now we have Zig as a cross compiler' in l), None)

if first_cmake is None or cross_marker is None:
    print(f"ERROR: Could not find patch markers (first_cmake={first_cmake}, cross_marker={cross_marker})", file=sys.stderr)
    sys.exit(1)

lines.insert(first_cmake, 'if [[ ! -f "$ROOTDIR/out/host/bin/zig" ]]; then\n')
lines.insert(cross_marker + 1, 'fi\n')

script_path.write_text(''.join(lines))
print(f"Patched: stages 1+2 (lines {first_cmake+1}-{cross_marker+1}) wrapped in if-guard")
