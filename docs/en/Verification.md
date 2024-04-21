# Verification Documentation

The **Verification** cog provides tools and commands necessary for verifying the identities of users by linking their Discord accounts with external
profiles, such as Steam. This ensures that users meet certain community standards or requirements.

## Overview

This cog facilitates a secure and efficient verification process, which is crucial for communities that require proof of identity or association, such
as gaming servers where users need to link their game profiles.

## Commands

### Verify

- **Description**: Initiates the user verification process.
- **Usage**: `/verify <steam_url>`
- **Permissions Required**: Unverified role
- **Details**:
    - `steam_url`: The URL to the user's Steam profile.
    - This command starts the verification process, where users are prompted to provide their Steam profile URL. The bot then checks the validity of
      the URL and provides further instructions for completing the verification.
    - It must be used in a designated verification channel to maintain order and ensure privacy during the process.

## Configuration

**File Location**: `bot/cogs/Verification.py`

The Verification cog is configured to handle user data sensitively and securely, ensuring that personal information is not misused or exposed. It
integrates with external APIs to verify the authenticity of provided links and profiles.

## Security Measures

- **Data Handling**: All data collected during the verification process is handled securely, with measures in place to protect user privacy.
- **Role Management**: After successful verification, users are automatically assigned roles that grant them access to community features, enhancing
  both security and user experience.

For detailed instructions on setting up and managing the verification process, including troubleshooting common issues, refer to the bot's source code
in the GitHub repository.

[Back to main documentation](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/blob/master/docs/en/Documentation.md)
