# coding=utf-8
import logging
import time
import threading


class MasterThread:
    def __init__(self):
        self.log = logging.getLogger(MasterThread.__name__)

    def main(self):
        while True:
            for i in range(10):
                self._per_second()

    # 判断io压力是否小 上一秒io小于5%io吞吐量
    def _is_io_low_pressure(self):
        self.log.debug('io压力小')
        return True

    # 当前缓冲池中脏页比例超过设置最大脏页阈值
    def _can_refresh_dirty_pages_to_disk(self):
        self.log.debug('可以刷新脏页')
        return True

    def _enable_adaptive_plush(self):
        self.log.debug('开启自适应刷新')
        return True

    def _not_user_activity(self):
        self.log.debug('没有用户活动')
        return True

    # 是否不在空闲
    def _not_idle(self):
        self.log.debug('不空闲')
        return True

    # 每秒运行
    def _per_second(self):
        time.sleep(1)
        self.log.debug('日志缓冲刷新到磁盘')
        if self._is_io_low_pressure():
            self.log.debug('合并5%io吞吐量条插入缓冲')
        if self._can_refresh_dirty_pages_to_disk():
            self.log.debug('刷新100%脏页')
        elif self._enable_adaptive_plush():
            self.log.debug('根据重做日志速度刷新脏页')
        if self._not_user_activity():
            self._background()

    # 后台刷新
    def _background(self):
        self.log.debug('刷新所有脏页')
        self.log.debug('合并100%插入缓冲')
        if self._not_idle():
            self.main()
        else:
            self._flush()

    # 刷新循环
    def _flush(self):
        self.log.debug('日志缓冲刷新到磁盘')
        if self._can_refresh_dirty_pages_to_disk():
            self._flush()

    # 暂停循环
    def _suspend(self):
        e = threading.Event()
        self.log.debug('等待事件激活')
        e.wait()
        self.main()


if __name__ == "__main__":
    MasterThread().main()
    pass
