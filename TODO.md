# Liste des tâches à réaliser

Cette liste reprend les actions nécessaires pour rendre l'application pleinement opérationnelle.

- [ ] **Persistance des données** *(en cours - SQLite ajouté)* : remplacer l'actuelle base en mémoire par une véritable base (ex. Postgres via Prisma). Adapter `packages/api` et prévoir les migrations.
- [ ] **Gestion complète des cycles d'entraînement** *(en cours - progression automatisée)* : structurer macrocycles, mésocycles et microcycles et automatiser la montée de charge (4 semaines + 1 semaine allégée).
- [ ] **Ajustement dynamique selon l'ACWR** *(en cours)* : adapter automatiquement la durée ou l'intensité des séances lorsque le ratio dépasse les seuils.
- [ ] **Module nutrition avancé** *(en cours)* : calculer les apports en glucides, protéines, lipides et suivre l'hydratation.
- [ ] **Prise en charge des blessures** *(en cours)* : enregistrer les blessures, appliquer la méthode RICE puis programmer la reprise progressive.
- [ ] **Synchronisation front‑end / back‑end** *(en cours)* : connecter l'application mobile et le tableau de bord web à l'API.
- [ ] **Interface utilisateur enrichie** : écrans de saisie des séances, de la nutrition et des blessures. Suivi visuel de la progression.
- [ ] **Gestion des compétitions** : planifier les compétitions et ajuster automatiquement les séances autour des dates clés.
- [ ] **Couverture de tests et CI/CD** : étendre les tests unitaires et mettre en place une intégration continue.
- [ ] **Documentation et aide utilisateur** : documenter toutes les API et fournir un guide rapide.
