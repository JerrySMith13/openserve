import os
import yaml
from enum import Enum

class UserPermissions(Enum):
    NotUser = 0,
    User = 1,
    Admin = 2,
    SuperAdmin = 3

class Config:
    #For oauth purposes + general web app
    app_url: str
    redir_path: str
    
    hour_db_path: str
    pending_db_path: str
    
    #approved organization email url, for rockhurst would be 'amdg.rockhursths.edu'
    approved_org: str
    blacklist_emails: set[str]
    
    #approved admins, for rockhurst would be 'rockhursths.edu'
    admin_org: str
    admin_list: str
    #specifies if admin list is whitelist or blacklist
    _is_whitelist: bool
    
    super_admins: set[str]
    
    google_client_info_path: str 
    
    #initializes config object from a config.toml file
    def __init__(self, path: str):
        pass
    
    #checks for admin permissions compared against whitelist + filters
    def _is_admin(self, email: str):
        pass
    
    #checks for user permissions compared against whitelist + filters. NOT guaranteed that said user is admin or not
    def _is_user(self, email: str):
        pass
    def user_type(self, email: str) -> UserPermissions:
        return UserPermissions.NotUser
        
    

#This code runs to set up a server in the directory specified by args
if __name__ == "__main__":