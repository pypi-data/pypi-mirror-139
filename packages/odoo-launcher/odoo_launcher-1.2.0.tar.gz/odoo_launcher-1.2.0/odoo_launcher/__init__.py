from __future__ import unicode_literals

import logging
import os
import sys

from . import laucher  # noqa
from . import api, config_section, mapper  # noqa
from .odoo_config_maker import OdooConfig, OdooEnvConverter  # noqa

_logger = logging.getLogger(__name__)


def main():
    env_vars = dict(os.environ)
    launcher = laucher.Launcher(
        args=sys.argv[:1],
        odoo_path=env_vars.get("ODOO_PATH"),
        odoo_rc=env_vars.get("ODOO_RC"),
        server_path=env_vars.get("ODOO_SERVER_PATH"),
    )
    _logger.info("create config")
    if env_vars.get("UPDATE") or env_vars.get("INSTALL"):
        return_code = launcher.launch_config_file(env_vars).wait()
        if return_code:
            sys.exit(return_code)
        _logger.info("Update or init detected")
        with launcher.launch_maintenance_server() as maintenance_server_proc:
            return_code = launcher.launch_update(env_vars).wait()
            maintenance_server_proc.kill()
        if return_code:
            sys.exit(return_code)
    _logger.info("#############################################")
    _logger.info("Run Odoo")
    sys.exit(launcher.launch(env_vars).wait())
