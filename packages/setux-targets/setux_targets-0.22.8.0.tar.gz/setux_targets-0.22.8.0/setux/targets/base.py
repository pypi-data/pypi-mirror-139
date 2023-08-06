from setux.core.target import CoreTarget
from setux.deployers.transfer import Sender, Syncer
from . import logger, info, error


class BaseTarget(CoreTarget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.context = dict()

    def __call__(self, command, **kw):
        ret, out, err = self.run(command, **kw)
        info('\n\t'.join(out))
        return ret

    def send(self, src, dst=None):
        try:
            Sender(self, src=src, dst=dst or src)()
        except Exception as x:
            error(f'send {src} -> {dst} ! {x}')
            return False
        return True

    def sync(self, src, dst=None):
        try:
            Syncer(self, src=src, dst=dst or src)()
        except Exception as x:
            error(f'sync {src} -> {dst} ! {x}')
            return False
        return True

