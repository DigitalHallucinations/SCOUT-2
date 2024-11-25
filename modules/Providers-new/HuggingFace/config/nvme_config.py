# modules/Providers/HuggingFace/config/nvme_config.py

import os

class NVMeConfig:
    def __init__(self):
        self.offload_nvme = False
        self.nvme_path = "/local_nvme"  # Default NVMe path
        self.nvme_buffer_count_param = 5
        self.nvme_buffer_count_optimizer = 4
        self.nvme_block_size = 1048576  # 1MB
        self.nvme_queue_depth = 8

    def enable_nvme_offloading(self, enable: bool):
        self.offload_nvme = enable

    def set_nvme_path(self, path: str):
        if not os.path.isabs(path):
            raise ValueError("NVMe path must be an absolute path.")
        self.nvme_path = path

    def set_nvme_buffer_count_param(self, count: int):
        if count <= 0:
            raise ValueError("NVMe buffer count for parameters must be positive.")
        self.nvme_buffer_count_param = count

    def set_nvme_buffer_count_optimizer(self, count: int):
        if count <= 0:
            raise ValueError("NVMe buffer count for optimizer must be positive.")
        self.nvme_buffer_count_optimizer = count

    def set_nvme_block_size(self, size: int):
        if size <= 0:
            raise ValueError("NVMe block size must be positive.")
        self.nvme_block_size = size

    def set_nvme_queue_depth(self, depth: int):
        if depth <= 0:
            raise ValueError("NVMe queue depth must be positive.")
        self.nvme_queue_depth = depth
