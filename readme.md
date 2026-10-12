# powerzig-bootstrap

Publishes the cross-compiled LLVM that [emanspeaks/powerzig](https://github.com/emanspeaks/powerzig) links into Zig for PowerPC 32-bit (`powerpc-linux-musleabihf`, `baseline` CPU).

The build itself is defined in [zig-build](https://codeberg.org/emanspeaks/zig-build); this repo's workflow only runs those scripts on GitHub's runners and publishes the result:

1. Build a stage3 Zig for the runner from the upstream devkit (`build-stage3.sh`), cached between runs.
2. Cross-compile LLVM, Clang, LLD, zlib and zstd with that Zig (`build-llvm-cross.sh`). This is the long step, so it is split across two jobs that share a ccache.
3. Publish the install prefix and a `manifest.json` as release `vN`.

## Releases

Each release contains:

| File | Contents |
|---|---|
| `llvm-powerpc-linux-musleabihf-baseline.tar.xz` | Static LLVM/Clang/LLD install prefix, all 20 default targets, plus zlib and zstd |
| `manifest.json` | Every input: zig-build commit, LLVM sources (zig-bootstrap commit), devkit version, and the `llvm_key` that identifies them |

A run only builds when no existing release has the same `llvm_key`, so unchanged inputs never produce duplicate releases. To rebuild anyway, run the workflow manually with **force**.

## Running it locally

On a Linux, macOS or BSD machine with a checkout of zig-build:

```sh
./build-stage3.sh
./build-llvm-cross.sh powerpc-linux-musleabihf baseline
```
