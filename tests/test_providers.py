#!/usr/bin/python
# -*- coding: utf-8 -*-

from skosprovider_heritagedata.providers import (
    HeritagedataProvider
)
import unittest

class HeritagedataProviderTests(unittest.TestCase):

    def test_default_language_error(self):
        self.assertRaises(ValueError, HeritagedataProvider, {'id': 'Heritagedata', 'default_language': 'nl'}, vocab_id='eh_period')

    def test_vocab_id_error(self):
        self.assertRaises(ValueError, HeritagedataProvider, {'id': 'Heritagedata', 'default_language': 'en'})

    def test_get_by_id_concept(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_by_id('PM')
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'en': 'POST MEDIEVAL'}]
        preflabels_conc = [{label['language']: label['label']} for label in concept['labels']
                           if label['type'] == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)

        self.assertGreater(len(concept['notes']), 0)

        self.assertEqual(concept['id'], 'PM')
        self.assertEqual(len(concept['broader']), 0)
        self.assertEqual(len(concept['related']), 0)
        self.assertIn('STU', concept['narrower'])

    def test_get_by_id_nonexistant_id(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_by_id('123')
        self.assertIsNone(concept)

    def test_get_by_uri(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_by_uri('http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['id'], 'PM')

    def test_get_all(self):
        self.assertFalse(HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_all())

    def test_get_top_display(self):
        top_heritagedata_display = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_top_display()
        self.assertIsInstance(top_heritagedata_display, list)
        self.assertGreater(len(top_heritagedata_display), 0)
        keys_first_display = top_heritagedata_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn('POST MEDIEVAL', [label['label'] for label in top_heritagedata_display])

    def test_get_top_concepts(self):
        top_heritagedata_concepts = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_top_concepts()
        self.assertIsInstance(top_heritagedata_concepts, list)
        self.assertGreater(len(top_heritagedata_concepts), 0)

    def test_get_childeren_display(self):
        childeren_Heritagedata_pm = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').get_children_display('PM')
        self.assertIsInstance(childeren_Heritagedata_pm, list)
        self.assertGreater(len(childeren_Heritagedata_pm), 0)
        keys_first_display = childeren_Heritagedata_pm[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("VICTORIAN", [label['label'] for label in childeren_Heritagedata_pm])

    def test_expand(self):
        all_childeren_pm = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').expand('PM')
        self.assertIsInstance(all_childeren_pm, list)
        self.assertGreater(len(all_childeren_pm), 0)
        self.assertIn('PM', all_childeren_pm)

    def test_expand_invalid(self):
        all_childeren_invalid = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').expand('invalid')
        self.assertFalse(all_childeren_invalid)

    def test_find_with_collection(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find, {'type': 'concept', 'collection': {'id': '300007466', 'depth': 'all'}})

    def test_find_collections(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find, {'type': 'collection'})

    def test_find_wrong_type(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find, {'type': 'collectie'})

    def test_find_multiple_keywords(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find({'label': 'iron Age', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_one_keywords(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}, vocab_id='eh_period').find({'label': 'VICTORIAN', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')