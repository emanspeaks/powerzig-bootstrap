# powerzig-bootstrap

Builds the pre-compiled LLVM toolchain artifacts consumed by
[emanspeaks/powerzig](https://github.com/emanspeaks/powerzig) to cross-compile
Zig for PowerPC 32-bit (`powerpc-linux-musleabihf`).

## What this repo does

The [zig-bootstrap](https://codeberg.org/ziglang/zig-bootstrap) build process
requires two LLVM installations:

| Artifact | Purpose |
|---|---|
| **Host LLVM + Zig** (`llvm-host-zig.tar.xz`) | Runs on the build machine (x86-64); used as the C/C++ cross-compiler to build the cross LLVM and the final Zig binary. |
| **Cross LLVM** (`llvm-cross-powerpc32.tar.xz`) | Compiled _for_ `powerpc-linux-musleabihf`; statically linked into the final Zig binary so it can generate code for all supported targets. |

Building these artifacts takes 5–10 hours on a 2-core GitHub Actions runner.
Separating them here means **powerzig** can skip the multi-hour LLVM build and
go straight to compiling Zig itself.

## What this repo does NOT do

This repo does **not** build the Zig compiler binary. That is done in
[emanspeaks/powerzig](https://github.com/emanspeaks/powerzig), which downloads
the artifacts produced here and runs `zig build -Dstatic-llvm`.

## LLVM target backends

The cross LLVM is built with **all 20 target backends** that Zig supports,
so the resulting Zig binary can generate code for any of them:

AArch64, AMDGPU, ARM, AVR, BPF, Hexagon, Lanai, LoongArch, Mips, MSP430,
NVPTX, **PowerPC**, RISCV, Sparc, SPIRV, SystemZ, VE, WebAssembly, X86, XCore

> PowerPC is included because it is one of Zig's standard 20 targets, not
> because this build is limited to PowerPC code generation.  The cross
> artifact is named `llvm-cross-powerpc32` because the LLVM libraries
> themselves are cross-compiled to _run on_ a PowerPC 32-bit machine.

## Releases

Releases are tagged `v1`, `v2`, … and contain two tarballs:

```
llvm-host-zig.tar.xz        # bin/zig  +  lib/zig/ stdlib
llvm-cross-powerpc32.tar.xz # powerpc-linux-musleabihf LLVM install prefix
```

Releases are created automatically when `zig-bootstrap`'s HEAD commit changes
(weekly scheduled check) or on a manual `workflow_dispatch` run.

## Workflow overview

```
prepare          — resolve zig-bootstrap commit, decide build/release
    │
build-host       — host LLVM + host Zig  (cached by bootstrap commit)
    │
build-cross-llvm — cross LLVM compile-only, save ccache  (≤6h)
    │
build-cross-clang-lld — resume from ccache, cmake install, publish  (≤6h)
```

The two-job split for the cross build keeps each step within GitHub Actions'
6-hour per-job limit. `ccache` carries compiled objects across the job boundary
so the second job only needs to link and install.
