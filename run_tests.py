import unittest
import sys

log_file = "test_results.log"


with open(log_file, "w", encoding="utf-8") as f:

    runner = unittest.TextTestRunner(stream=f, verbosity=2)
    loader = unittest.TestLoader()
    

    tests = loader.discover('tests')

    result = runner.run(tests)

print(f"\n✅ Testing complete. Results saved to: {log_file}")
