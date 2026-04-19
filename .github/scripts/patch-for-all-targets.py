#!/usr/bin/env python3
"""Patch the zig-bootstrap build script to build all LLVM targets instead of PowerPC only,
and optionally wire ccache into the cross LLVM cmake configure.

Usage:
  patch-for-all-targets.py [--ccache] <build-script>
"""
import sys
import pathlib

ALL_TARGETS = (
    'AArch64;AMDGPU;ARM;AVR;BPF;Hexagon;Lanai;LoongArch;Mips;MSP430;NVPTX;'
    'PowerPC;RISCV;Sparc;SPIRV;SystemZ;VE;WebAssembly;X86;XCore'
)

add_ccache = '--ccache' in sys.argv
script_file = next((a for a in sys.argv[1:] if not a.startswith('--')), 'build')

path = pathlib.Path(script_file)
text = path.read_text()

# Inject LLVM_TARGETS_TO_BUILD (all 20 targets) right after -DLLD_BUILD_TOOLS=OFF
ANCHOR = '-DLLD_BUILD_TOOLS=OFF'
if ANCHOR not in text:
    print(f'ERROR: anchor "{ANCHOR}" not found in {path}', file=sys.stderr)
    sys.exit(1)

targets_line = f'    -DLLVM_TARGETS_TO_BUILD={ALL_TARGETS}'
text = text.replace(ANCHOR, f'{ANCHOR} \\\n{targets_line}', 1)

if add_ccache:
    ccache_suffix = (
        ' \\\n    -DCMAKE_C_COMPILER_LAUNCHER=ccache'
        ' \\\n    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache'
        ' \\\n    -DCMAKE_ASM_COMPILER_LAUNCHER=ccache'
    )
    text = text.replace(targets_line, targets_line + ccache_suffix, 1)

path.write_text(text)
n = ALL_TARGETS.count(';') + 1
print(f'Patched: LLVM_TARGETS_TO_BUILD={n} targets' + (' + ccache' if add_ccache else ''))
