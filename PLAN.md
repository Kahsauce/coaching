# Plan de développement

Cette application doit évoluer vers une plateforme complète de suivi sportif
(web et mobile). Les grandes étapes sont inspirées du cahier des charges.

1. **Analyse du PDF** : extraire les modèles de périodisation, les règles ACWR,
   nutrition et blessures.
2. **Atelier UX & personas** : définir les parcours utilisateurs, wireframes
   mobile first.
3. **Mise en place du monorepo (Turborepo)** : structure `apps/web`,
   `apps/mobile` et `packages/api`.
4. **Conception de la base de données avec Prisma**.
5. **Implémentation d'un moteur de règles pour planifier et adapter les séances**.
6. **API workouts (tRPC/GraphQL)** avec drag-and-drop et replanification.
7. **Module nutrition et hydratation**.
8. **Gestion des blessures et adaptations automatiques**.
9. **Dashboard Aujourd'hui** (web & mobile).
10. **Calendrier hebdomadaire interactif**.
11. **Statistiques ACWR, charge, progression**.
12. **Plan nutrition détaillé**.
13. **Gestion des compétitions et recalcul du plan**.
14. **Tests unitaires et e2e (couverture >80%)**.
15. **Déploiement Docker + CI/CD et documentation complète**.

Chaque étape fera l'objet de branches et de revues de code dédiées.
