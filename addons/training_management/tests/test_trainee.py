# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class  TestTrainingTrainee(TransactionCase):

    def setUp(self):
        super().setUp()
        self.trainee = self.env['training.trainee'].create({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'organization': 'Example Organization',
        })
    def test_trainee_creation(self):
        self.assertTrue(self.trainee.exists())
        self.assertEqual(self.trainee.name, 'John Doe')
        self.assertEqual(self.trainee.email, 'john.doe@example.com')
        self.assertEqual(self.trainee.organization, 'Example Organization')
    
    def test_trainee_update(self):
        self.trainee.write({'name': 'Jane Doe'})
        self.assertEqual(self.trainee.name, 'Jane Doe')
        self.trainee.write({'organization': 'New Organization'})
        self.assertEqual(self.trainee.organization, 'New Organization')

    def test_trainee_deletion(self):
        trainee_id = self.trainee.id
        self.trainee.unlink()
        self.assertFalse(self.env['training.trainee'].browse(trainee_id).exists())