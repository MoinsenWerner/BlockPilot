from collections import defaultdict
from typing import Dict, List


class VersionService:
    """Static service that would normally pull versions from Mojang APIs."""

    def __init__(self):
        self._versions: Dict[str, List[str]] = defaultdict(
            list,
            {
                "vanilla": ["1.20.4", "1.20.3", "1.19.4"],
                "paper": ["1.20.4", "1.19.4"],
                "fabric": ["1.20.2", "1.20.1"],
                "folia": ["1.20.2"],
                "forge-installer": ["1.20.1", "1.19.2"],
                "neoforge-installer": ["1.20.2"],
                "purpur": ["1.20.4"],
                "velocity": ["3.2.0"],
                "bungee-cord": ["1.20"],
            },
        )

    def get_versions(self, software_type: str) -> List[str]:
        return self._versions.get(software_type.lower(), [])
