from loglib import loglib


class Test_loglib:
    def test_get_file_name(self):
        prefix = 'abc'
        postfix = 'xyz'
        ext = 'test'

        file_name = loglib.get_file_name(prefix=prefix, postfix=postfix, ext=ext)
        assert len(file_name) == 28
        assert file_name[:3] == prefix
        assert file_name[20:23] == postfix
        assert file_name[24:] == ext

        file_name = loglib.get_file_name(prefix=prefix, postfix=postfix, ext=ext, with_ms=True)
        assert len(file_name) == 32
        assert file_name[:3] == prefix
        assert file_name[24:27] == postfix
        assert file_name[28:] == ext

        file_name = loglib.get_file_name(postfix=postfix, ext=ext)
        assert len(file_name) == 24
        assert file_name[:3] != prefix
        assert file_name[16:19] == postfix
        assert file_name[20:] == ext

        file_name = loglib.get_file_name(prefix=prefix, ext=ext)
        assert len(file_name) == 24
        assert file_name[:3] == prefix
        assert file_name[16:19] != postfix
        assert file_name[20:] == ext

        file_name = loglib.get_file_name(prefix=prefix, postfix=postfix)
        assert len(file_name) == 23
        assert file_name[:3] == prefix
        assert file_name[20:23] == postfix
        assert file_name[24:] != ext

    def test_loglib(self):
        test_file = 'test_loglib.zzz'
        debug = 'debug'
        info = 'info'
        warning = 'warning'
        error = 'error'
        critical = 'critical'

        logger = loglib('test_loglib')
        logger.start_log(test_file)
        logger.debug(debug)
        logger.info(info)
        logger.warning(warning)
        logger.error(error)
        logger.critical(critical)
        logger.d(debug)
        logger.i(info)
        logger.w(warning)
        logger.e(error)
        logger.c(critical)
        logger.close_log()

        with open('test_loglib.zzz') as f:
            lines = f.readlines()
            assert len(lines) == 10
            assert lines[0][-(len(debug) + 1):-1] == debug
            assert lines[1][-(len(info) + 1):-1] == info
            assert lines[2][-(len(warning) + 1):-1] == warning
            assert lines[3][-(len(error) + 1):-1] == error
            assert lines[4][-(len(critical) + 1):-1] == critical
            assert lines[5][:-1] == debug
            assert lines[6][:-1] == info
            assert lines[7][:-1] == warning
            assert lines[8][:-1] == error
            assert lines[9][:-1] == critical

        import os
        if os.path.exists(test_file):
            os.remove(test_file)
