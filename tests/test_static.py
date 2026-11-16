import asyncio
import unittest
import app

class StaticStartupTests(unittest.TestCase):
    def test_frontend_modules_use_javascript_mime_and_no_store(self):
        static=app.FreshStaticFiles(directory=app.ROOT/'web',html=True)
        scope={'type':'http','method':'GET','path':'/app.js','headers':[]}
        for name in ('app.js','timeline.mjs','bootstrap.js'):
            response=asyncio.run(static.get_response(name,scope))
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.headers['cache-control'],'no-store')
            self.assertIn('text/javascript',response.headers['content-type'])
            cached={**scope,'headers':[(b'if-none-match',response.headers['etag'].encode())]}
            self.assertEqual(asyncio.run(static.get_response(name,cached)).status_code,200)
    def test_favicon_is_not_a_startup_error(self):
        self.assertEqual(app.favicon().status_code,204)
