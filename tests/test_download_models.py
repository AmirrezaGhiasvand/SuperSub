import unittest
from unittest.mock import patch
import install_models

class ModelDownloadTests(unittest.TestCase):
    def test_only_supported_runtime_files_downloaded(self):
        self.assertEqual(set(install_models.MODELS),{'small','medium','turbo','large-v3'})
        for choice,(repo,folder,files) in install_models.MODELS.items():
            with patch('sys.argv',['install_models.py',choice]),patch.object(install_models,'snapshot_download') as download:
                install_models.main()
            self.assertEqual(download.call_args.args,(repo,))
            self.assertEqual(download.call_args.kwargs['allow_patterns'],files)
            self.assertIn('model.bin',files)
            self.assertNotIn('model.safetensors',files)
