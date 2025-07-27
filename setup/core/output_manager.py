"""
Output filename management for SuperClaude commands
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class OutputManager:
    """Manages standardized output filenames and conventions"""
    
    def __init__(self, config_dir: Path):
        """
        Initialize output manager
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.conventions_file = config_dir / "output_conventions.json"
        self._conventions_cache = None
    
    def load_conventions(self) -> Dict[str, Any]:
        """Load output conventions from config file"""
        if self._conventions_cache is not None:
            return self._conventions_cache
            
        if not self.conventions_file.exists():
            # Return sensible defaults if config doesn't exist
            return self._get_default_conventions()
        
        try:
            with open(self.conventions_file, 'r') as f:
                conventions = json.load(f)
            self._conventions_cache = conventions
            return conventions
        except (json.JSONDecodeError, FileNotFoundError):
            return self._get_default_conventions()
    
    def _get_default_conventions(self) -> Dict[str, Any]:
        """Get default conventions if config file doesn't exist"""
        return {
            "filename_conventions": {
                "include_timestamps": True,
                "timestamp_format": "YYYYMMDD_HHMM",
                "separator": "_",
                "patterns": {
                    "default": "{prefix}_{timestamp}.md"
                }
            },
            "output_locations": {
                "reports": "./reports/",
                "analysis": "./",
                "documentation": "./"
            }
        }
    
    def generate_filename(self, 
                         prefix: str, 
                         file_type: str = "default",
                         identifier: Optional[str] = None,
                         extension: str = "md") -> str:
        """
        Generate standardized filename based on conventions
        
        Args:
            prefix: Base name for the file (e.g., "LLMS-SITEMAP", "CONTENT_AUDIT")
            file_type: Type of file for pattern lookup (default: "default")
            identifier: Optional identifier (e.g., directory name, case ID)
            extension: File extension (default: "md")
            
        Returns:
            Standardized filename with timestamp
        """
        conventions = self.load_conventions()
        filename_config = conventions.get("filename_conventions", {})
        
        if not filename_config.get("include_timestamps", True):
            # If timestamps disabled, return simple format
            if identifier:
                return f"{prefix}_{identifier}.{extension}"
            return f"{prefix}.{extension}"
        
        # Generate timestamp
        timestamp_format = filename_config.get("timestamp_format", "YYYYMMDD_HHMM")
        timestamp = self._generate_timestamp(timestamp_format)
        
        # Get pattern for file type
        patterns = filename_config.get("patterns", {})
        pattern = patterns.get(file_type, patterns.get("default", "{prefix}_{timestamp}.md"))
        
        # Replace placeholders
        filename = pattern.format(
            prefix=prefix,
            timestamp=timestamp,
            identifier=identifier or "",
            extension=extension
        )
        
        # Clean up any double separators from empty identifier
        separator = filename_config.get("separator", "_")
        while f"{separator}{separator}" in filename:
            filename = filename.replace(f"{separator}{separator}", separator)
        
        return filename
    
    def _generate_timestamp(self, format_str: str) -> str:
        """Generate timestamp string in specified format"""
        now = datetime.now()
        
        # Convert format string to strftime format
        format_mapping = {
            "YYYY": "%Y",
            "MM": "%m", 
            "DD": "%d",
            "HH": "%H",
            "mm": "%M",
            "ss": "%S"
        }
        
        strftime_format = format_str
        for placeholder, strftime_code in format_mapping.items():
            strftime_format = strftime_format.replace(placeholder, strftime_code)
        
        return now.strftime(strftime_format)
    
    def get_output_directory(self, output_type: str = "analysis") -> str:
        """Get standardized output directory path"""
        conventions = self.load_conventions()
        locations = conventions.get("output_locations", {})
        return locations.get(output_type, "./")
    
    def generate_full_path(self, 
                          prefix: str,
                          output_type: str = "analysis", 
                          file_type: str = "default",
                          identifier: Optional[str] = None) -> str:
        """
        Generate full file path including directory
        
        Args:
            prefix: Base name for the file
            output_type: Type for directory lookup ("reports", "analysis", "documentation")
            file_type: Type for filename pattern lookup
            identifier: Optional identifier
            
        Returns:
            Full file path
        """
        directory = self.get_output_directory(output_type)
        filename = self.generate_filename(prefix, file_type, identifier)
        return f"{directory.rstrip('/')}/{filename}"


# Convenience function for commands to use
def get_timestamped_filename(prefix: str, 
                            identifier: Optional[str] = None,
                            file_type: str = "default") -> str:
    """
    Quick function for commands to get timestamped filename
    
    Args:
        prefix: Base name (e.g., "LLMS-SITEMAP")
        identifier: Optional identifier
        file_type: File type for pattern matching
        
    Returns:
        Timestamped filename
    """
    # Try to find config directory
    possible_config_dirs = [
        Path("../../../config"),
        Path("../../config"), 
        Path("../config"),
        Path("config"),
        Path(".")
    ]
    
    config_dir = None
    for dir_path in possible_config_dirs:
        if (dir_path / "output_conventions.json").exists():
            config_dir = dir_path
            break
    
    if config_dir is None:
        # Fallback to simple timestamp format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        if identifier:
            return f"{prefix}_{identifier}_{timestamp}.md"
        return f"{prefix}_{timestamp}.md"
    
    manager = OutputManager(config_dir)
    return manager.generate_filename(prefix, file_type, identifier)