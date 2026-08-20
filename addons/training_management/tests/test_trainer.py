# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class  TestTrainingTrainer(TransactionCase):

    def setUp(self):
        super().setUp()
        self.trainer = self.env['training.trainer'].create({
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        })
    def test_trainer_creation(self):
        self.assertTrue(self.trainer.exists())
        self.assertEqual(self.trainer.name, 'John Doe')
        self.assertEqual(self.trainer.email, 'john.doe@example.com')

    def test_trainer_update(self):
        self.trainer.write({'name': 'Jane Doe'})
        self.assertEqual(self.trainer.name, 'Jane Doe')

    def test_trainer_deletion(self):
        trainer_id = self.trainer.id
        self.trainer.unlink()
        self.assertFalse(self.env['training.trainer'].browse(trainer_id).exists())