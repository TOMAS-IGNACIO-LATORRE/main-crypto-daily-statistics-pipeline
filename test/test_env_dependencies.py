import subprocess
import unittest

class DependencyCheckTests(unittest.TestCase):
    """
    Test suite to ensure all installed Python packages are compatible and conflict-free.
    """

    def test_no_dependency_conflicts(self) -> None:
        """
        Verifies there are no package dependency issues by running the 'pip check' command.
        If any issues are found, the test fails and provides the output for debugging.
        """
        try:
            process_result = subprocess.run(
                ['pip', 'check'], capture_output=True, text=True
            )
        except subprocess.SubprocessError as e:
            self.fail(f"Failed to run pip check: {e}")

        if process_result.returncode != 0:
            error_output = process_result.stdout.strip()
            self.fail(f"Dependency issues detected:\n{error_output}")
        else:
            print("All dependencies are compatible and conflict-free.")

if __name__ == "__main__":
    unittest.main()
