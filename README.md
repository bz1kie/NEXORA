# NEXORA

**NEXORA** is an experimental PlayStation 5 emulator for Windows x64.
The Windows build produces a graphical `NEXORA.exe` launcher. Game
compatibility and real-world performance are **not yet verified**.

## Windows portable build

1. Open [NEXORA Windows builds](https://github.com/bz1kie/NEXORA/actions/workflows/nexora-windows.yml).
2. Open the latest successful workflow run on the development branch.
3. Download the `NEXORA-windows-x64-portable` artifact (GitHub sign-in may be required).
4. Extract the ZIP to a folder. Keep `NEXORA.exe`, `game-run.exe`, and all
   companion files in the same directory.
5. Run `NEXORA.exe`.

This is a development build, not a signed installer. Windows may show a
SmartScreen warning for an unsigned experimental executable. Do not download
builds from untrusted mirrors.

## Development

The source is built with Zig 0.16.0. Windows CI runs
`zig build -Doptimize=ReleaseSafe` and checks that both required executables
are present. The portable ZIP is produced from `zig-out/bin`.

The frame profiling module records guest flip intervals. Its CSV export API
is integrated in the renderer, but no user-facing CSV export button is
available yet. See [frame timing notes](docs/FRAME_TIMING.md).

## License and acknowledgments

NEXORA is a modified version of the open-source PS5PCEM project by its
respective contributors, distributed under **GPL-3.0-or-later**.
Original copyright notices and required attribution are retained.
The original upstream project is available at
https://github.com/iStark/PS5PCEM.

The NEXORA-specific modifications are also distributed under
**GPL-3.0-or-later**. See [LICENSE](LICENSE).
