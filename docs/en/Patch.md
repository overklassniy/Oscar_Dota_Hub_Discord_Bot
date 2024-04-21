# Patch Documentation

The **Patch** cog provides functionality for managing and requesting game patches within the Discord server. It allows administrators and users to
interact with and track the status of game updates and patches effectively.

## Overview

This cog includes commands to request new patches, set the status of patches, and create automated scripts for downloading patches. It's essential for
keeping the gaming community up-to-date with the latest game changes and developments.

## Commands

### Request

- **Description**: Initiates a request for a new game patch.
- **Usage**: `/patch request`
- **Details**: Opens a modal where users can enter the version of the game patch they wish to request. The command must be used in a designated
  verification channel.

### SetMaxPatch

- **Description**: Sets the latest patch version that can be requested.
- **Usage**: `/patch setmaxpatch <max_patch>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: Administrators can update the maximum patch version to control which patches are eligible for requests, preventing outdated or incorrect
  patch requests.

### SetDone

- **Description**: Marks a patch request as completed.
- **Usage**: `/patch setdone <request_id>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: Updates the status of a requested patch to 'done', indicating that the patch has been handled or implemented.

### SetAbandoned

- **Description**: Marks a patch request as abandoned.
- **Usage**: `/patch setabandoned <request_id>`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: Indicates that a patch request will no longer be pursued, updating its status accordingly.

### CreateScript

- **Description**: Generates a SteamCMD script for downloading a specific patch.
- **Usage**: `/patch create_script <date> [number]`
- **Permissions Required**: Administrator / Moderator roles
- **Details**: Creates a downloadable script based on Steam database information, facilitating the deployment or installation of game patches.

## Configuration

**File Location**: `bot/cogs/Patch.py`

The Patch cog is configured to interact with various data sources and APIs to retrieve and manage game patch information accurately. It is vital for
maintaining the relevance and functionality of game-related features within the community.

For detailed instructions on how to utilize and configure the Patch cog, refer to the source code available in the GitHub repository.

[Back to main documentation](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/blob/master/docs/en/Documentation.md)
