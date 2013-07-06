import config.test as test_conf
import config.production as prod_conf
import config.main as maincfg
import os


def set_env(f):
    def tmp(*args, **kwargs):
        if Config.test_suite:
            Config.cfg = test_conf
        else:
            Config.cfg = prod_conf
        res = f(*args, **kwargs)
        return res
    return tmp


class Config(object):

    test_suite = None
    cfg = prod_conf

    @staticmethod
    @set_env
    def getImageDir():
        return Config.cfg.image_dir

    @staticmethod
    @set_env
    def getDbFile():
        return os.path.join(maincfg.app_dir, Config.cfg.sqlite_file)

    @staticmethod
    @set_env
    def getVocFile():
        return os.path.join(maincfg.app_dir, Config.cfg.voc_file)

    @staticmethod
    @set_env
    def getVocName():
        return Config.cfg.voc_name