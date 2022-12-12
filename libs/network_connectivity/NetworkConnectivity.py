REMOTE_SERVER_IP = "3.130.51.163"
import subprocess
import time
import threading


class SshTunnel(threading.Thread):
    def __init__(self, localport, remoteport, remoteuser, remotehost):
        threading.Thread.__init__(self)
        self.localport = localport  # Local port to listen to
        self.remoteport = remoteport  # Remote port on remotehost
        self.remoteuser = remoteuser  # Remote user on remotehost
        self.remotehost = remotehost  # What host do we send traffic to
        self.daemon = True  # So that thread will exit when
        # main non-daemon thread finishes

    def run(self):
        a = subprocess.call([
            'ssh', '-C',
            '-L', str(self.localport) + ':' + "10.28.3.10" + ':' + str(self.remoteport),
            self.remoteuser + '@' + self.remotehost])



if __name__ == '__main__':
    tunnel = SshTunnel(8800, 8080, 'ubuntu', REMOTE_SERVER_IP)
    tunnel.start()
    tunnel.join()
    # subprocess.call(['curl', 'http://10.28.3.10:8800'])
