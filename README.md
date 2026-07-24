# Dragonfly Loader

An automated job to load new releases from the PyPI RSS feed into the [Dragonfly Mainframe](https://github.com/vipyrsec/dragonfly-mainframe).

## Configuration

The loader authenticates to a Cloudflare Access protected Dragonfly endpoint by
default in all environments.

Required runtime settings:

- `BASE_URL`
- `CF_ACCESS_CLIENT_ID`
- `CF_ACCESS_CLIENT_SECRET`

For staging, `BASE_URL` should be the public protected hostname rather than an
in-cluster origin, for example `https://dragonfly-staging.vipyrsec.com`.

## Development

Run the complete local validation suite with:

```console
prek run --all-files
```

The container-definition hook uses native
[Hadolint 2.13.1](https://github.com/hadolint/hadolint/releases/tag/v2.13.1)
and requires `hadolint` on `PATH`. This avoids requiring a local container
runtime. The official Linux x86-64 release binary has SHA-256:

```text
f8b05e4c724cdeb84c0dca07e40936c3d875c0af5d120a27c94026a0f370b2cf
```

Download the binary from the linked upstream release, verify the checksum, make
it executable, and place it in a persistent tools directory included in
`PATH`.
