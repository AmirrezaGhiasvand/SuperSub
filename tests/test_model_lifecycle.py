import unittest
from pathlib import Path
from unittest.mock import patch
from fastapi import HTTPException
import app

class ModelLifecycleTests(unittest.TestCase):
    def test_load_validates_profile_and_uses_resident_process(self):
        entry=dict(path=str(Path('models/model').resolve()),profile='multilingual')
        with patch.object(app.local_models,'catalog',return_value={'test':entry}),patch.object(app.local_models,'valid_folder',return_value=True),patch.object(app.inference.resident,'load',return_value={'status':'loading'}) as loader:
            self.assertEqual(app.load_model({'model':'test'})['status'],'loading')
            loader.assert_called_once_with(entry['path'],app.DATA/'model-runtime')
        self.assertFalse(app.lock.locked())
    def test_loading_and_unloading_blocked_during_generation(self):
        app.lock.acquire()
        try:
            for call in (lambda:app.load_model({'model':'test'}),app.unload_model):
                with self.assertRaises(HTTPException) as error:call()
                self.assertEqual(error.exception.status_code,409)
        finally:app.lock.release()
    def test_unload_releases_worker(self):
        with patch.object(app.inference.resident,'unload',return_value={'status':'unloaded'}) as unload:
            self.assertEqual(app.unload_model()['status'],'unloaded');unload.assert_called_once()
    def test_rejects_unsupported_model(self):
        with patch.object(app.local_models,'catalog',return_value={'nava':{'profile':'nava','path':'unused'}}):
            with self.assertRaises(HTTPException) as error:app.load_model({'model':'nava'})
        self.assertEqual(error.exception.status_code,400)
        self.assertFalse(app.lock.locked())
