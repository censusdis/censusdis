---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Code sample to reproduce the behavior. Please include a minimal standalone piece of 
code that reproduces the bug. Something like

```python
import censusdis.data as ced

result = ced.something(arg0, arg1, optional_arg=True)

# The result here is Null, when I expected a DataFrame.
print(result)
```

Or, even better, structure your code sample as a test that fails. Something like

```python
import unittest
import censusdis.data as ced

class TestMyBug(unittest.TestCase):
    def test_bug(self):
        result = ced.something(arg0, arg1, optional_arg=True)
        self.assertIsNotNone(result)
```
That way, when we fix the bug, we can add this unit test to make sure it does
not come back.

**Expected behavior**
A clear and concise description of what you expected to happen,
ideally as encoded in your test case.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment (please complete the following information):**
 - Hardware/Processor: [e.g. MacBook Pro M1]
 - Python Version and platform; output of:
```python
import sys
print(sys.version)
print(sys.platform)
```
 - Censusdis Version; output of:
```python
import censusdis
print(censusdis.version)
```

**Additional context**
Add any other context about the problem here.
