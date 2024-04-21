# Tools Documentation

The **Tools** cog comprises utility commands that assist in managing server interactions and content. These tools are designed to streamline server
management tasks, making them easier and more efficient for administrators and moderators.

## Overview

This cog includes commands that help in moving messages between channels, managing user permissions, and performing other administrative tasks that
enhance the bot's functionality and server management.

## Commands

### Move

- **Description**: Moves a specified message to another channel.
- **Usage**: `!move #<channel>`
- **Permissions Required**: Administrator / Moderator / Helper roles
- **Details**:
    - `channel`: The target channel where the message will be moved.
    - This command requires that the user invoke the command in response to the message they wish to move. The message content will be re-posted in the
      designated channel as an embed and then deleted from the original channel.
    - Permissions: This command is restricted to users with administrative privileges or specific roles designated in the bot's configuration.

## Configuration

**File Location**: `bot/cogs/Tools.py`

The Tools cog is critical for efficient server management, allowing for quick modifications to message placement and visibility, which can help
maintain order and organization within the server's communication channels.

For more detailed instructions on how to utilize and configure the Tools cog, refer to the source code available in the GitHub repository.

[Back to main documentation](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/blob/master/docs/en/Documentation.md)
