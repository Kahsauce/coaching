# Plan de développement

Cette application doit évoluer vers une plateforme complète de suivi sportif (web et mobile). Les grandes étapes sont inspirées du cahier des charges.

- [x] **Analyse du PDF** : extraire les modèles de périodisation, les règles ACWR, nutrition et blessures.
- [x] **Atelier UX & personas** : définir les parcours utilisateurs, wireframes mobile first.
- [x] **Mise en place du monorepo (Turborepo)** : structure `apps/web`, `apps/mobile` et `packages/api`.
- [x] **Conception de la base de données avec Prisma**.
- [x] **Implémentation d'un moteur de règles pour planifier et adapter les séances**.
- [x] **API workouts (tRPC/GraphQL)** avec drag-and-drop et replanification.
- [x] **Module nutrition et hydratation**.
- [x] **Gestion des blessures et adaptations automatiques**.
- [ ] **Dashboard Aujourd'hui** (web & mobile).
- [ ] **Calendrier hebdomadaire interactif**.
- [ ] **Statistiques ACWR, charge, progression**.
- [ ] **Plan nutrition détaillé**.
- [ ] **Gestion des compétitions et recalcul du plan**.
- [ ] **Tests unitaires et e2e (couverture >80%)**.
- [ ] **Déploiement Docker + CI/CD et documentation complète**.

Chaque étape fera l'objet de branches et de revues de code dédiées.
