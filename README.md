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
