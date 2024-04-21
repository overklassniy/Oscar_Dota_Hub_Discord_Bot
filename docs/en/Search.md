# Search Documentation

The **Search** cog facilitates content searching and interactions within the Discord server, using specific commands to manage and respond to search
queries with images and text.

## Overview

This cog provides tools for posting and managing search-related messages, which can include images selected based on pre-defined rules or user inputs.
It's designed to support moderators and users in creating engaging and dynamic content.

## Commands

### Search

- **Description**: Sends a search-related message with an optional image attachment.
- **Usage**: `/search [image]`
- **Permissions Required**: Administrator / Moderator / Helper roles
- **Details**:
    - `image`: An optional parameter specifying the number of an image to attach to the message. If omitted, a random image from the configured list
      may be used.
    - This command ensures interactions remain relevant and engaging by allowing the inclusion of visual content.
    - It must be used in specified channels designated for search-related activities.

### Gather

- **Description**: Gathers users for an event based on their reactions to a message.
- **Usage**: `!gather <ip>`
- **Permissions Required**: Administrator / Moderator / Helper roles
- **Details**:
    - `ip`: Required parameter specifying the IP address of an event server, which is useful for gaming communities.
    - This command collects users who reacted with a specific emoji and prepares a list or message indicating their readiness or interest.
    - Provides a method for organizers to quickly assemble participants and disseminate event details effectively.

## Configuration

**File Location**: `bot/cogs/Search.py`

The Search cog is crucial for managing interactive content within the server, particularly for communities centered around real-time interaction and
responsiveness. It supports a wide range of activities from simple searches to organizing large community events.

For more detailed information on configuring and extending the capabilities of the Search cog, refer to the bot's source code in the GitHub repository.

[Back to main documentation](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/blob/master/docs/en/Documentation.md)
