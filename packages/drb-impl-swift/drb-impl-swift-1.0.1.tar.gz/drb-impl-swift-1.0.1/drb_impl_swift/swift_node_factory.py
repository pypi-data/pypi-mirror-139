from drb import DrbNode
from drb.factory.factory import DrbFactory
from drb_impl_http import DrbHttpNode
from requests.auth import HTTPBasicAuth

from drb_impl_swift import SwiftService, SwiftAuth


class SwiftNodeFactory(DrbFactory):
    """ authurl=None, user=None,
                 key=None, preauthurl=None,
                 preauthtoken=None,
                 os_options: Dict = None,
                 auth_version="1",
                 """

    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, SwiftService):
            return node
        if isinstance(node, DrbHttpNode):
            if isinstance(node.auth, HTTPBasicAuth):
                auth = SwiftAuth(authurl=node.path.path,
                                 user=node.auth.username,
                                 key=node.auth.password
                                 )
            else:
                auth = SwiftAuth(authurl=node.path.path)
            return SwiftService(auth=auth)
        raise NotImplementedError("Call impl method")
