import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import local_models

class LocalModelsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.folder=self.root/'Persian model'
        self.folder.mkdir()
        for name in ('model.bin','config.json','tokenizer.json'):
            (self.folder/name).write_text('{}')
        self.patcher=patch.object(local_models,'REGISTRY',self.root/'data'/'local-models.json')
        self.patcher.start()
    def tearDown(self):
        self.patcher.stop();self.tmp.cleanup()
    def test_persists_without_copy_and_deduplicates(self):
        key,entry=local_models.register(str(self.folder),'multilingual')
        self.assertEqual(local_models.catalog()[key]['path'],str(self.folder.resolve()))
        self.assertEqual(local_models.register(str(self.folder),'persian')[0],key)
        self.assertEqual(len(json.loads(local_models.REGISTRY.read_text())),1)
        self.assertEqual(len(list(self.folder.iterdir())),3)
    def test_rejects_incomplete_or_relative_folder(self):
        (self.folder/'tokenizer.json').unlink()
        with self.assertRaises(ValueError): local_models.register(str(self.folder),'multilingual')
        with self.assertRaises(ValueError): local_models.register('models','multilingual')
    def test_missing_folder_not_ready(self):
        key,_=local_models.register(str(self.folder),'multilingual')
        (self.folder/'model.bin').unlink()
        self.assertFalse(local_models.valid_folder(Path(local_models.catalog()[key]['path'])))
    def test_nava_is_rejected(self):
        folder=self.folder.rename(self.root/'Nava-ct2')
        with self.assertRaises(ValueError):local_models.register(str(folder),'multilingual')
    def test_legacy_unsupported_entry_hidden_without_deleting_files(self):
        local_models.REGISTRY.parent.mkdir()
        local_models.REGISTRY.write_text(json.dumps({'old':{'path':str(self.folder),'profile':'nava','name':'Old model'}}))
        self.assertNotIn('old',local_models.catalog())
        self.assertTrue((self.folder/'model.bin').exists())
