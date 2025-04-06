import os
import shutil
import tempfile
import unittest
from sync_tool import sync_dirs

class TestFolderSyncIntegration(unittest.TestCase):
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()

        self.test_file = os.path.join(self.source_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("Hello Integration Test")

    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)

    def test_sync_creates_file(self):
        sync_dirs(self.source_dir, self.replica_dir)

        replica_file = os.path.join(self.replica_dir, "test.txt")
        self.assertTrue(os.path.exists(replica_file))

        with open(replica_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello Integration Test")

if __name__ == '__main__':
    unittest.main()
