# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AirDates'
        db.create_table(u'scrape_airdates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('airdate', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('game', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'scrape', ['AirDates'])

        # Adding M2M table for field contestants on 'AirDates'
        m2m_table_name = db.shorten_name(u'scrape_airdates_contestants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('airdates', models.ForeignKey(orm[u'scrape.airdates'], null=False)),
            ('contestants', models.ForeignKey(orm[u'scrape.contestants'], null=False))
        ))
        db.create_unique(m2m_table_name, ['airdates_id', 'contestants_id'])

        # Adding model 'Documents'
        db.create_table(u'scrape_documents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clue', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('right', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'scrape', ['Documents'])

        # Adding model 'Categories'
        db.create_table(u'scrape_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'scrape', ['Categories'])

        # Adding model 'Clues'
        db.create_table(u'scrape_clues', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('c_game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.AirDates'], null=True, blank=True)),
            ('c_document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.Documents'], null=True, blank=True)),
            ('c_round', self.gf('django.db.models.fields.IntegerField')()),
            ('c_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'scrape', ['Clues'])

        # Adding model 'Classifications'
        db.create_table(u'scrape_classifications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clue_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.Clues'], null=True, blank=True)),
            ('category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.Categories'], null=True, blank=True)),
        ))
        db.send_create_signal(u'scrape', ['Classifications'])

        # Adding model 'Contestants'
        db.create_table(u'scrape_contestants', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player_id', self.gf('django.db.models.fields.IntegerField')()),
            ('player_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('player_nickname', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'scrape', ['Contestants'])

        # Adding model 'Earnings'
        db.create_table(u'scrape_earnings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round1', self.gf('django.db.models.fields.IntegerField')()),
            ('round2', self.gf('django.db.models.fields.IntegerField')()),
            ('round3', self.gf('django.db.models.fields.IntegerField')()),
            ('final', self.gf('django.db.models.fields.IntegerField')()),
            ('e_game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.AirDates'], null=True, blank=True)),
            ('e_player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrape.Contestants'], null=True, blank=True)),
        ))
        db.send_create_signal(u'scrape', ['Earnings'])


    def backwards(self, orm):
        # Deleting model 'AirDates'
        db.delete_table(u'scrape_airdates')

        # Removing M2M table for field contestants on 'AirDates'
        db.delete_table(db.shorten_name(u'scrape_airdates_contestants'))

        # Deleting model 'Documents'
        db.delete_table(u'scrape_documents')

        # Deleting model 'Categories'
        db.delete_table(u'scrape_categories')

        # Deleting model 'Clues'
        db.delete_table(u'scrape_clues')

        # Deleting model 'Classifications'
        db.delete_table(u'scrape_classifications')

        # Deleting model 'Contestants'
        db.delete_table(u'scrape_contestants')

        # Deleting model 'Earnings'
        db.delete_table(u'scrape_earnings')


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
            'final': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round1': ('django.db.models.fields.IntegerField', [], {}),
            'round2': ('django.db.models.fields.IntegerField', [], {}),
            'round3': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['scrape']