# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Earnings.final'
        db.delete_column(u'scrape_earnings', 'final')


    def backwards(self, orm):
        # Adding field 'Earnings.final'
        db.add_column(u'scrape_earnings', 'final',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        u'scrape.airdates': {
            'Meta': {'object_name': 'AirDates'},
            'airdate': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'contestants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['scrape.Contestants']", 'symmetrical': 'False'}),
            'game': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scrape.categories': {
            'Meta': {'object_name': 'Categories'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scrape.classifications': {
            'Meta': {'object_name': 'Classifications'},
            'category_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.Categories']", 'null': 'True', 'blank': 'True'}),
            'clue_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.Clues']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scrape.clues': {
            'Meta': {'object_name': 'Clues'},
            'c_document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.Documents']", 'null': 'True', 'blank': 'True'}),
            'c_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.AirDates']", 'null': 'True', 'blank': 'True'}),
            'c_round': ('django.db.models.fields.IntegerField', [], {}),
            'c_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scrape.contestants': {
            'Meta': {'object_name': 'Contestants'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_id': ('django.db.models.fields.IntegerField', [], {}),
            'player_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'player_nickname': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'scrape.documents': {
            'Meta': {'object_name': 'Documents'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'clue': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'right': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'scrape.earnings': {
            'Meta': {'object_name': 'Earnings'},
            'e_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.AirDates']", 'null': 'True', 'blank': 'True'}),
            'e_player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrape.Contestants']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round1': ('django.db.models.fields.IntegerField', [], {}),
            'round2': ('django.db.models.fields.IntegerField', [], {}),
            'round3': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['scrape']