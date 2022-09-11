import re
import subprocess

coverage_report = subprocess.Popen(
    ["coverage", "report", "--skip-empty"], stdout=subprocess.PIPE)
summary: str = coverage_report.stdout.read().decode("utf-8")

last_line = summary.splitlines()[-1]
coverage = re.findall('\d+', last_line)[-1]

print(coverage)
