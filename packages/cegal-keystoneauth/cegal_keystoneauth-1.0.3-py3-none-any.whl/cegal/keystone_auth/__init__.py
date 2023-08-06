# Copyright 2021 Cegal AS
# All rights reserved

__version__ = "1.0.3"
__git_hash__ = "e13aaf50"

import logging
from os import getenv


logger = logging.getLogger(__name__)
verify_tls = True
if getenv("PYVAR_ALLOW_NON_HTTPS") == "true":
    verify_tls = False


from .client import OidcClient
from .options import OidcOptions, OidcFlow
