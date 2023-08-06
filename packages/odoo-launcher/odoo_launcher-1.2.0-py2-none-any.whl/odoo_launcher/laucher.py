from __future__ import unicode_literals

import argparse
import configparser
import logging
import os
import subprocess
import sys
import uuid
from typing import Dict, List, Optional

from .odoo_config_maker import OdooConfig

_logger = logging.getLogger("launch")
_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
_logger.addHandler(handler)


class Launcher(object):
    def __init__(self, args, odoo_path=None, odoo_rc=None, server_path=None):
        # type: (List[str], Optional[str], Optional[str], Optional[str]) -> Launcher
        parser = self.get_parser()
        ns, other = parser.parse_known_args(args=args)
        odoo_path = ns.odoo_path or odoo_path
        assert odoo_path, "No Odoo path is provided"
        self.odoo_path = os.path.abspath(os.path.expanduser(odoo_path))

        odoo_rc = ns.odoo_rc or odoo_rc
        assert "No Odoo config file path is provided"
        self.odoo_rc = os.path.abspath(odoo_rc)
        ndp_server_path = ns.server_path or server_path
        assert "Server path is provided"
        self.ndp_server_path = os.path.abspath(os.path.expanduser(ndp_server_path))

    def get_parser(self):
        # type: () -> argparse.ArgumentParser
        parser = argparse.ArgumentParser()
        parser.add_argument("--odoo-path", dest="odoo_path", help="Path of odoo-bin")
        parser.add_argument("--odoo-rc", "-c", dest="odoo_rc", help="Path of the base config file")
        parser.add_argument("--ndp-server-path", dest="server_path", help="Server Path")
        return parser

    def create_config_file_args(self, env_vars):
        # type: (Dict[str, str]) -> OdooConfig
        config = OdooConfig(env_vars, self.odoo_rc)
        config.http_config.enable = False

        config.update_install.enable = False
        config.update_install.save_config_file = True
        config.update_install.force_stop_after_init = True
        config.update_install.force_save_config_file = True
        return config

    def _get_default_config_file(self, env_vars):
        if os.path.exists(self.odoo_rc):
            _logger.info("Remove file %s", self.odoo_rc)
            os.remove(self.odoo_rc)
        default_config = self.get_config_parser(env_vars)
        with open(self.odoo_rc, "w") as fp:
            default_config.write(fp)

    def get_config_parser(self, env_vars):
        default_config = configparser.ConfigParser()
        section = "options"
        default_config.add_section(section)
        default_config.set(section, "admin_passwd", env_vars.get("ADMIN_PASSWD", str(uuid.uuid4())))
        default_config.set(section, "csv_internal_sep", env_vars.get("CSV_INTERNAL_SEP", ","))
        default_config.set(
            section, "publisher_warranty_url", env_vars.get("PUBLISHER_WARRANTY_URL", "https://ndp-systemes.fr")
        )
        default_config.set(section, "reportgz", str(False))
        default_config.set(section, "root_path", str(False))
        return default_config

    def launch_config_file(self, env_vars):
        self._get_default_config_file(env_vars)
        config = self.create_config_file_args(env_vars)
        return self._launch_odoo("ndpserver", config)

    def launch_update(self, env_vars):
        # type: (Dict[str, str]) -> subprocess.Popen
        config = self.config_launch_update(env_vars)
        return self._launch_odoo("ndpserver", config)

    def launch(self, env_vars):
        # type: (Dict[str, str]) -> subprocess.Popen
        return self._launch_odoo("ndpserver", None)

    def config_launch_update(self, env_vars):
        # type: (Dict[str, str]) -> OdooConfig
        config = OdooConfig(env_vars, self.odoo_rc)
        config.http_config.enable = False
        config.workers_config.enable = False
        config.db_config.enable = False
        config.addons_config.enable = False
        config.workers_config.enable = False
        config.update_install.enable = True

        config.wide_module.remove_queue_job()
        config.update_install.stop_after_init = True

        return config

    def launch_maintenance_server(self):
        # type: () -> subprocess.Popen
        return self._execute_popen([sys.executable, "-m", "maintenance_server"])

    def normalize_args(self, srv, config):
        # type: (str, Optional[OdooConfig]) -> List[str]
        cmd_args = [sys.executable, os.path.join(self.odoo_path, "odoo-bin")]
        if srv:
            cmd_args.append("--addons-path=%s" % self.ndp_server_path)
            cmd_args.append(srv)
        return cmd_args + (config and config.to_odoo_args() or [])

    def _launch_odoo(self, srv, config):
        # type: (str, Optional[OdooConfig]) -> subprocess.Popen
        return self._execute_popen(self.normalize_args(srv, config))

    def _execute_popen(self, cmd):
        # type: (List[str]) -> subprocess.Popen
        _logger.info("Run -> %s", " ".join([str(s) for s in cmd]))
        return subprocess.Popen(cmd)


if __name__ == "__main__":
    _logger.info("create config")
    launcher = Launcher(sys.argv[1:])
    if os.getenv("UPDATE") or os.getenv("INSTALL"):
        return_code = launcher.create_config_file(update_mode=True).wait()
        if return_code:
            sys.exit(return_code)
        _logger.info("Update or init detected")
        with launcher.launch_maintenance_server() as maintenance_server_proc:
            return_code = launcher.launch_update().wait()
            maintenance_server_proc.kill()
        if return_code:
            sys.exit(return_code)
    _logger.info("#############################################")
    _logger.info("Run Odoo")
    sys.exit(launcher.launch().wait())
