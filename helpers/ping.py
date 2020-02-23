import subprocess
import platform
import logging

LOG = logging.getLogger(__name__)


class Ping(object):

    LOG.debug('In ping class')

    @staticmethod
    def ping_host(host_ip):
        LOG.debug('In method ping_host')
        if platform.platform().split("-")[0] == "Linux":
            res = subprocess.Popen(['ping', '-c1', host_ip],
                                   stdout=subprocess.PIPE)
            LOG.debug('Result of ping = {0}'.format(res))
        else:
            res = subprocess.Popen(['ping', '-n', '1', host_ip],
                                   stdout=subprocess.PIPE)
            LOG.debug('Result of ping = {0}'.format(res))

        output = str(res.communicate()[0]).split(",")
        print("Ping Output == {0}".format(output))
        if " 0% packet loss" in output or ' Lost = 0 (0% loss)' in output:
            print("successfully send packets to remote PC")
            return True
        return False
