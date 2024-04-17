# modules/user_accounts/user_data_manager.py

import os
import json
import re
import subprocess
import re
from modules.logging.logger import setup_logger

logger = setup_logger('user_data_manager.py')

class SystemInfo:
    @staticmethod
    def run_command(command):
        """Runs a system command and returns the output."""
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            return result.stdout
        except Exception as e:
            logger.error(f"Error running command '{command}': {e}")
            return ""

    @staticmethod
    def get_basic_info():
        """Gets basic system information using the 'systeminfo' command."""
        output = SystemInfo.run_command("systeminfo")
        return output

    @staticmethod
    def get_cpu_info():
        """Gets CPU information using the 'wmic cpu get' command."""
        output = SystemInfo.run_command("wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors /format:list")
        return output

    @staticmethod
    def get_memory_info():
        """Gets memory information using the 'wmic MemoryChip' command."""
        output = SystemInfo.run_command("wmic MemoryChip get Capacity /format:list")
        total_memory = sum([int(re.search(r'Capacity=(\d+)', line).group(1)) for line in output.splitlines() if "Capacity" in line])
        return f"Total Physical Memory: {total_memory / (1024**3):.2f} GB"

    @staticmethod
    def get_disk_info():
        """Gets disk information using the 'wmic diskdrive' command."""
        output = SystemInfo.run_command("wmic diskdrive get model,size /format:list")
        return output

    @staticmethod
    def get_network_info():
        """Gets network configuration using the 'ipconfig /all' command."""
        output = SystemInfo.run_command("ipconfig /all")
        return output

    @staticmethod
    def get_detailed_system_info():
        """Compiles detailed system information from various sources."""
        info = {
            "Basic Info": SystemInfo.get_basic_info(),
            "CPU Info": SystemInfo.get_cpu_info(),
            "Memory Info": SystemInfo.get_memory_info(),
            "Disk Info": SystemInfo.get_disk_info(),
            "Network Info": SystemInfo.get_network_info(),
        }
        return info

class UserDataManager:
    def __init__(self, user):
        self.user = user
        self.profile = self.get_profile_text
        self.emr = self.get_emr
        self.system_info = self.get_system_info
        logger.info(f"UDM instantiated with user: {self.user}, {self.profile}")

    def get_profile(self):
        logger.info("Entering get_profile() method")
        try:
            profile_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', 'modules', 'user_accounts', 'user_profiles',
                f"{self.user}.json"
            ))

            if not os.path.exists(profile_path):
                logger.error(f"Profile file does not exist: {profile_path}")
                return {}

            with open(profile_path, 'r', encoding='utf-8') as file:
                profile = json.load(file)
                logger.info("Profile found")
                return profile

        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            return {}
        
    def format_profile_as_text(self, profile_json):
        logger.info("Formatting profile.")
        profile_lines = []
        for key, value in profile_json.items():
            line = f"{key}: {value}"
            profile_lines.append(line)
        return '\n'.join(profile_lines)
    
    def get_profile_text(self):
        logger.info("Entering get_profile_text() method")
        profile_json = self.get_profile()
        return self.format_profile_as_text(profile_json)
    
    def get_emr(self):
        logger.info("Getting EMR.")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        EMR_filename = f"{self.user}_emr.txt"
        relative_EMR_path = os.path.join(script_dir, '..', '..', 'modules', 'user_accounts', 'user_profiles', EMR_filename)
        
        EMR_path = os.path.abspath(relative_EMR_path)

        logger.info(f"EMR path: {EMR_path}")

        if not os.path.exists(EMR_path):
            logger.error(f"EMR file does not exist: {EMR_path}")
            return ""
        
        try:
            with open(EMR_path, 'r', encoding='utf-8') as file:
                EMR = file.read()
                EMR = EMR.replace("\n", " ")
                EMR = re.sub(r'\s+', ' ', EMR)
                return EMR.strip()
        except Exception as e:
            logger.error(f"Error loading EMR: {e}")
            return ""

    def get_system_info(self):
        """Retrieves and formats detailed system information for persona personalization."""
        try:
            detailed_info = SystemInfo.get_detailed_system_info()
            formatted_info = ""
            for category, info in detailed_info.items():
                logger.info(f"Retrieving {category} information:")
                logger.info(info)
                formatted_info += f"--- {category} ---\n{info}\n"
            logger.info("System information retrieved successfully.")
            return formatted_info
        except Exception as e:
            logger.error(f"Error retrieving system information: {e}")
            return "System information not available"