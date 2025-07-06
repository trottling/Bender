def run(params: dict, log_func=None):
    result = {}
    if log_func:
        log_func('Starting hardware scan...', '🔍')
    if params.get('cpuCheckBox'):
        log_func('Collecting CPU info...', '🖥️')
        result['cpu'] = 'Intel Core i7 (example)'
    if params.get('gpuCheckBox'):
        log_func('Collecting GPU info...', '🖥️')
        result['gpu'] = 'NVIDIA RTX 3080 (example)'
    if params.get('ramCheckBox'):
        log_func('Collecting RAM info...', '💾')
        result['ram'] = '16GB (example)'
    if params.get('romCheckBox'):
        log_func('Collecting ROM info...', '💽')
        result['rom'] = '512GB SSD (example)'
    if params.get('macCheckBox'):
        log_func('Collecting MAC address...', '🌐')
        result['mac'] = '00:11:22:33:44:55 (example)'
    if params.get('bitnessCheckBox'):
        log_func('Collecting system bitness...', '🔢')
        result['bitness'] = '64-bit (example)'
    log_func('Hardware scan finished.', '✅')
    return result 