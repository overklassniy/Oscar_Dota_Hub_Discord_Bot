# Cogs Documentation

The **Cogs** cog is responsible for managing the other cogs within the Oscar Dota Hub Discord Bot. This includes loading, unloading, and reloading cogs
dynamically, which allows for updates and maintenance without needing to restart the entire bot.

## Overview

The Cogs cog provides commands to manage the lifecycle of other cogs, which are components that handle specific functionalities within the bot. This
management is essential for maintaining an active and up-to-date bot environment.

## Commands

### Load

- **Description**: Loads a specified cog.
- **Usage**: `/cogs load <extension>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: The `load` command takes the name of a cog and loads it into the bot. This is useful for adding new functionalities on the fly.

### Unload

- **Description**: Unloads a specified cog.
- **Usage**: `/cogs unload <extension>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: The `unload` command disables a cog. This can be useful for temporarily removing a feature or for maintenance purposes.

### Reload

- **Description**: Reloads a specified cog.
- **Usage**: `/cogs reload <extension>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: The `reload` command unloads and then reloads a cog. This is used for applying updates or changes to the cog without disrupting the
  overall operation of the bot.

### Reload All

- **Description**: Reloads all cogs.
- **Usage**: `/cogs reload_all`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: This command will reload every cog currently loaded by the bot. It is particularly useful after a batch update of multiple cogs or
  system-wide changes.

## Configuration

**File Location**: `bot/cogs/Cogs.py`

The Cogs cog is a core part of the bot's operational management. It must be configured correctly to ensure that permissions and access are
appropriately set to prevent unauthorized use of these powerful commands.

For more detailed information on setting up and managing cogs, refer to the bot's main documentation or the source code located in the GitHub
repository.

[Back to main documentation](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/docs/en/Documentation.md)
