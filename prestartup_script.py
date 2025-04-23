from collections import namedtuple
from unittest.mock import patch
import psutil
import os


def get_cgroup_version():
    """Check cgroup version by testing the existence of memory control files.
    Returns:
        str: "v2" if cgroup v2 is found, "v1" if cgroup v1 is found, None if neither.
    """
    # Check for cgroup v2 (unified hierarchy)
    if os.path.exists("/sys/fs/cgroup/memory.max"):
        return "v2"
    # Check for cgroup v1 (legacy hierarchy)
    elif os.path.exists("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        return "v1"
    # Neither found (possibly not in a cgroup environment)
    return None

def read_int(path):
    try:
        with open(path) as f:
            value = f.read().strip()
            if value == "max":
                return None
            return int(value)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def container_virtual_memory(original, cgroup_version):
    svmem = namedtuple("svmem", original._fields)

    override = {}
    
    if cgroup_version == "v1":
         # cgroup v1
        total = read_int("/sys/fs/cgroup/memory/memory.limit_in_bytes")
        used = read_int("/sys/fs/cgroup/memory/memory.usage_in_bytes")
    elif cgroup_version == "v2":
        # cgroup v2
        total = read_int("/sys/fs/cgroup/memory.max")
        used = read_int("/sys/fs/cgroup/memory.current")
    else:
        # Neither cgroup v1 nor v2 found
        print("Neither cgroup v1 nor cgroup v2 found. Using original values.")
        return original

    # If values are read, update the override dictionary
    if total is not None:
        override["total"] = total
    if used is not None:
        override["used"] = used

    # Calculate available and percent
    if total is not None and used is not None:
        override["available"] = total - used
        override["percent"] = round((used / total) * 100, 2) if total > 0 else 0

    # Construct new svmem object, using values from override if available
    new_values = [override.get(field, getattr(original, field)) for field in original._fields]
    return svmem(*new_values)

def apply_memory_patch():
    """Apply the memory patch if running in a container environment"""
    cgroup_version = get_cgroup_version()
    if cgroup_version is None:
        print("Not in a container environment - using original psutil values")
        return
    
    original_memory = psutil.virtual_memory()
    patched_memory = lambda: container_virtual_memory(original_memory, cgroup_version)
    patch("psutil.virtual_memory", patched_memory).start()
    print(f"psutil.virtual_memory has been patched for cgroup {cgroup_version} environment")

# Apply the patch when this module is imported
apply_memory_patch()