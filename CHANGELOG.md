# Changelog

## [0.1] - 2025-01-29

### Added
- **Core bot functionality**: A Discord bot was created that integrates with AI models.
- **`!switch` command**: Added the ability to change the AI model using the following commands:
  - `!switch low` — switches to the `deepseek-r1:1.5b` model.
  - `!switch high` — switches to the `deepseek-r1:8b` model.
- **Message processing**: The bot processes user messages, queries the selected model for a response, and sends it back to the channel.
- **`!systemstatus` command**: Added a command to check the current system load:
  - Displays the CPU usage percentage.
  - Displays the memory usage percentage.
  - Displays the disk usage percentage.
- **Logging**: Basic logging has been added for monitoring the bot's operation.

### Changed
- **Model request module**: Requests to the model are handled through a separate `api_handler.py` module.
- **Response processing**: Added logic to clean up responses by removing unnecessary `<think>` and `</think>` tags.

### Fixed
- Fixed command handling issues that allow the bot to correctly respond to user input.
