import time
import logging
from collections import defaultdict

class PerformanceMetrics:
    _start_times = {}
    _total_times = defaultdict(lambda: 0)
    _call_stack = []

    @staticmethod
    def start(name):
        """Start timing for a given process name."""
        now = time.perf_counter()
        PerformanceMetrics._start_times[name] = now
        PerformanceMetrics._call_stack.append(name)
        logging.info(f"Performance start: {name}")

    @staticmethod
    def stop(name):
        """Stop timing for a given process name and log elapsed time."""
        now = time.perf_counter()
        start_time = PerformanceMetrics._start_times.get(name)
        if start_time is None:
            logging.warning(f"Performance stop called without matching start: {name}")
            return
        elapsed = now - start_time
        PerformanceMetrics._total_times[name] += elapsed
        # Remove from start_times
        del PerformanceMetrics._start_times[name]
        # Remove from call stack
        if PerformanceMetrics._call_stack and PerformanceMetrics._call_stack[-1] == name:
            PerformanceMetrics._call_stack.pop()
        else:
            logging.warning(f"Call stack mismatch on stop: {name}")
        # Convert elapsed seconds to D:H:M:S:MS
        days, rem = divmod(elapsed, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, rem = divmod(rem, 60)
        seconds, milliseconds = divmod(rem * 1000, 1000)
        message = (f"{name} executed in "
                   f"{int(days)}d:{int(hours)}h:{int(minutes)}m:{int(seconds)}s:{int(milliseconds)}ms")
        logging.info(message)

    @staticmethod
    def report():
        """Report total elapsed times for all measured processes."""
        report_lines = ["Performance Metrics Summary:"]
        for name, total_time in PerformanceMetrics._total_times.items():
            days, rem = divmod(total_time, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, rem = divmod(rem, 60)
            seconds, milliseconds = divmod(rem * 1000, 1000)
            line = (f"{name}: {int(days)}d:{int(hours)}h:{int(minutes)}m:"
                    f"{int(seconds)}s:{int(milliseconds)}ms")
            report_lines.append(line)
        report = "\n".join(report_lines)
        logging.info(report)
        return report
