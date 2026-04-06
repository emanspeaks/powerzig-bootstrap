Pre-built LLVM artifacts consumed by [emanspeaks/powerzig](https://github.com/emanspeaks/powerzig)'s Zig build workflow.

| Field | Value |
|---|---|
| Release tag | `$RELEASE_TAG` |
| zig-bootstrap commit | `$BOOTSTRAP_COMMIT` |
| Zig version in zig-bootstrap | `$ZIG_VERSION` |
| Target | `$ZIG_TARGET` |
| CPU | `$ZIG_CPU` |
| Host LLVM build type | MinSizeRel (build-time tool only) |
| Cross LLVM build type | Release (linked into the final Zig binary) |

**Files:**
- `llvm-host-zig.tar.xz` — host Zig compiler (`out/host/bin/zig`), used to compile the cross Zig
- `llvm-cross-powerpc32.tar.xz` — cross LLVM install prefix, statically linked into the final Zig binary
