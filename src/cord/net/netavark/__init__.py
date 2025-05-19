from datetime import timedelta
from io import BytesIO
from pathlib import Path
from subprocess import Popen

from msgspec import json

from cord.utils.clwrap import CLIWrapperBase

from .spec import NetworkOptions

# TODO: error handling


class Netavark(CLIWrapperBase):
    def __init__(
        self,
        path: str | Path = "netavark",
        firewall_driver: str | None = None,
        rootless: bool | None = None,
        aardvark_path: str | None = None,
        aardvark_config: str | None = None,
        plugin_directories: list[str] | None = None,
    ):
        global_args = []

        if firewall_driver:
            global_args.append(f"--firewall-driver={firewall_driver}")
        if rootless:
            global_args.append(str(rootless).lower())
        if aardvark_path:
            global_args.append(f"--aardvark-binary={aardvark_path}")
        if aardvark_config:
            # Note: this is correct, this config is for aardvark, not for netavark
            global_args.append(f"--config={aardvark_config}")
        if plugin_directories:
            for directory in plugin_directories:
                global_args.append(f"--plugin-directory={directory}")

        super().__init__(path, global_args)

    def setup(self, ns_path: str, config: NetworkOptions):
        data = BytesIO(json.encode(config))
        self._run("setup", ns_path, stdin=data)

    def update_dns(self, ns_path: str, dns: str):
        self._run("update", f"--network-dns-servers={dns}", ns_path)

    def run_firewalld_reloader(self) -> Popen:
        # TODO: do not wait here
        return self._run_raw("firewalld-reload")

    def run_dhcp_proxy(
        self, backup_dir: str, uds: str, timeout: timedelta, activity_timeout: timedelta
    ):
        args = []
        if backup_dir:
            args.append(f"--dir={backup_dir}")
        if uds:
            args.append(f"--uds={uds}")
        if timeout:
            args.append(f"--timeout={timeout.total_seconds()}")
        if activity_timeout:
            args.append(f"--activity-timeout={activity_timeout.total_seconds()}")

        # TODO: do not wait here
        return self._run_raw("dhcp-proxy", *args)

    def teardown(self, ns_path: str):
        self._run("teardown", ns_path)
