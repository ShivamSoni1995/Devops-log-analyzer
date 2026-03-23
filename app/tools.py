def detect_error_type(log: str) -> str:
    log = log.lower()

    if "oomkilled" in log:
        return "memory_error"
    elif "crashloopbackoff" in log:
        return "crash_loop"
    elif "imagepullbackoff" in log:
        return "image_error"
    elif "connection refused" in log:
        return "network_error"
    else:
        return "unknown"
