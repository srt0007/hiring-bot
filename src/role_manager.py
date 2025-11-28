"""
Role Manager Module
Manages multiple job roles and their JDs
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class RoleManager:
    """Manages job roles and their job descriptions"""

    def __init__(self, config_file: str = 'roles_config.json'):
        """Initialize role manager"""
        self.config_file = config_file
        self.roles = self._load_roles()

    def _load_roles(self) -> List[Dict]:
        """Load roles from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('roles', [])
            except Exception as e:
                print(f"[ERROR] Failed to load roles: {e}")
                return []
        return []

    def _save_roles(self):
        """Save roles to config file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'roles': self.roles}, f, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save roles: {e}")
            return False

    def add_role(self, role_name: str, jd_file: str) -> Dict:
        """Add a new role"""
        # Generate role ID
        role_count = len(self.roles) + 1
        role_id = f"ROLE{role_count:03d}"

        new_role = {
            'role_id': role_id,
            'role_name': role_name,
            'jd_file': jd_file,
            'active': True,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }

        self.roles.append(new_role)
        self._save_roles()
        return new_role

    def get_active_roles(self) -> List[Dict]:
        """Get all active roles"""
        return [r for r in self.roles if r.get('active', True)]

    def get_role_by_id(self, role_id: str) -> Optional[Dict]:
        """Get role by ID"""
        for role in self.roles:
            if role['role_id'] == role_id:
                return role
        return None

    def get_role_by_name(self, role_name: str) -> Optional[Dict]:
        """Get role by name"""
        for role in self.roles:
            if role['role_name'].lower() == role_name.lower():
                return role
        return None

    def update_role(self, role_id: str, updates: Dict) -> bool:
        """Update a role"""
        for i, role in enumerate(self.roles):
            if role['role_id'] == role_id:
                self.roles[i].update(updates)
                return self._save_roles()
        return False

    def deactivate_role(self, role_id: str) -> bool:
        """Deactivate a role"""
        return self.update_role(role_id, {'active': False})

    def activate_role(self, role_id: str) -> bool:
        """Activate a role"""
        return self.update_role(role_id, {'active': True})

    def get_role_count(self) -> int:
        """Get total number of roles"""
        return len(self.roles)

    def get_active_role_count(self) -> int:
        """Get number of active roles"""
        return len(self.get_active_roles())
