from convisoappsec.flow.source_code_scanner import SCC
from convisoappsec.logger import LOGGER
import docker

def project_metrics(source_code_dir, ci_provider_name):
    try:
        scanner = SCC(source_code_dir, ci_provider_name)
        scanner.scan()
        return {
            'total_lines': scanner.total_source_code_lines
        }
    except docker.errors.APIError as e:
        LOGGER.error('Error on fetch project metrics')
        LOGGER.exception(e)
        return None

