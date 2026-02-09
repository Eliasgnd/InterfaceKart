"""Repository for loading and saving application settings."""

from domain.settings_model import AppSettings


class SettingsRepository:
    """Persist and retrieve settings from a backing store."""

    def load_settings(self) -> AppSettings:
        """Load settings from disk; return defaults for now."""
        return AppSettings()

    def save_settings(self, settings: AppSettings) -> None:
        """Save settings to disk."""
        # TODO: write settings to a file or database.
        _ = settings
