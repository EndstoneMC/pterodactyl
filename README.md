# Endstone Pterodactyl Egg

A [Pterodactyl](https://pterodactyl.io/) / [Pelican](https://pelican.dev/) egg for running
[Endstone](https://github.com/EndstoneMC/endstone) servers. Endstone is a plugin framework
for Minecraft Bedrock Dedicated Server, similar to Bukkit/Spigot/Paper for Java Edition.

## Quick Start

1. Download [`egg-endstone.json`](egg-endstone.json) from this repo
2. In your panel, go to **Admin > Nests > Import Egg** and upload the file
3. Create a new server using the **Endstone** egg
4. Start the server

The egg automatically installs the latest version of Endstone on first start.

## Configuration

### Endstone Version

The `ENDSTONE_VERSION` variable controls which version to install. By default it's set to
`endstone` which always installs the latest release.

Examples:

| Value | Effect |
|-------|--------|
| `endstone` | Always install the latest release (default) |
| `endstone==0.11.2` | Pin a specific version |
| `https://example.com/endstone-0.12.0-py3-none-any.whl` | Install from a direct URL |
| `endstone-0.12.0-py3-none-any.whl` | Install a `.whl` file uploaded to the server |

Available versions are listed on [PyPI](https://pypi.org/project/endstone/#history).

### Docker Image

The egg supports Python 3.10 through 3.14. Python 3.12 is recommended for most users.
Choose a different image only if a plugin requires a specific Python version.

### Server Properties

A default `server.properties` is created on first install. You can edit it through the
panel's file manager or via SFTP. Common settings:

| Property | Default | Description |
|----------|---------|-------------|
| `server-port` | `19132` | IPv4 port (managed by the panel) |
| `server-name` | `Endstone Server` | Server name shown in the server list |
| `gamemode` | `survival` | Default game mode: survival, creative, adventure |
| `max-players` | `10` | Maximum player count |
| `difficulty` | `easy` | World difficulty |
| `online-mode` | `true` | Require Xbox Live authentication |

## Installing Plugins

1. Build or download a plugin `.whl` file
2. Upload it to the `plugins/` folder via the panel's file manager or SFTP
3. Restart the server

Find plugins on [PyPI](https://pypi.org/search/?q=endstone) or build your own using the
[Python](https://github.com/EndstoneMC/python-example-plugin) or
[C++](https://github.com/EndstoneMC/cpp-example-plugin) plugin templates.

## Updating Endstone

If `ENDSTONE_VERSION` is set to `endstone` (the default), simply restarting the server will
install the latest version. If you've pinned a version, update the variable and restart.

## Documentation

- [Endstone Documentation](https://endstone.dev/latest/)
- [Endstone GitHub](https://github.com/EndstoneMC/endstone)

## License

[MIT License](LICENSE)