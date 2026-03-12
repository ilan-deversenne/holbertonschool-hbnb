#!/usr/bin/env python3
"""Script pour créer toutes les tables de la base de données."""

from app import create_app, db
from app.models.user import User
from app.models.place import Place

app = create_app()

with app.app_context():
    db.drop_all()
    print("Base nettoyée (toutes les tables supprimées).")
    db.create_all()
    print("Tables créées avec succès.")
