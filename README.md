# Dragonfly Loader

An automated job to load new releases from the PyPI RSS feed into the [Dragonfly Mainframe](https://github.com/vipyrsec/dragonfly-mainframe).

## Configuration

The loader authenticates to Auth0 by default in all environments.

Set `DISABLE_AUTH=true` only for local or test scenarios where the mainframe is
also configured to bypass authentication.
