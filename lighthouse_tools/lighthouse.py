import subprocess
from lighthouse_tools.throttling_profiles import NETWORK_PROFILES


class LightHouse:

    @staticmethod
    def lighthouse_report_throttling(url, port, throttling_profile, report_file_name="lighthouse_report.html"):
        throttling_profile = NETWORK_PROFILES[throttling_profile]
        process_exit_code = subprocess.check_call(
            f"lighthouse {url} --port {port} "
            '--chrome-flags="--headless" '
            "--throttling-method=devtools "
            "--emulated-form-factor=none "
            "--disable-cpu-throttling=true "
            "--disable-network-throttling "
            f"--throttling.requestLatencyMs={throttling_profile['latency']} "
            f"--throttling.downloadThroughputKbps={throttling_profile['downloadThroughput']} "
            f"--throttling.uploadThroughputKbps={throttling_profile['uploadThroughput']} "
            "--no-enable-error-reporting "
            "--disable-storage-reset "
            f"--output-path=./{report_file_name}".split(" "), shell=LightHouse.check_os_for_shell())

        assert process_exit_code == 0, "lighthouse finish with error"

    @staticmethod
    def lighthouse_report_without_throttling(url, port, report_file_name="lighthouse_report.html"):
        process_exit_code = subprocess.check_call(
            f"lighthouse {url} --port {port} "
            "--no-enable-error-reporting "
            f"--output-path=./{report_file_name}".split(" "), shell=LightHouse.check_os_for_shell())

        assert process_exit_code == 0, "lighthouse finish with error"

    @staticmethod
    def check_os_for_shell():
        import platform
        if platform.system() != "Windows":
            return False
        return True
