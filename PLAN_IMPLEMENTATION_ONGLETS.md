# Plan d'Implémentation des Onglets - HomeShow Desktop

## État Actuel

### ✅ Corrections Effectuées
1. **Erreur Tkinter Callback**: Corrigé `tk.Toplevel(self.main_window)` → `tk.Toplevel(self.main_window.root)`
2. **Navigation entre onglets**: Utilisation d'index au lieu de noms traduits dans `on_tab_changed()`
3. **Interfaces de base créées**: Les trois onglets ont leurs classes d'interface respectives

### 🏗️ Infrastructure Existante
- **PropertyManagerInterface**: Interface complète avec recherche, filtres, liste
- **ProjectsInterface**: Interface avec arbre de projets et gestion hiérarchique
- **TemplatesInterface**: Interface avec catégories (Website, Property, Email)

## 🎯 Priorités d'Implémentation

### Phase 1: Fonctionnalités Critiques (Semaine 1)

#### 🏠 Onglet Properties - Fonctionnalités Manquantes

**1. Édition de Propriétés**
```python
# À ajouter dans PropertyManagerInterface
def edit_property(self, property_id):
    # Ouvrir PropertyWizard en mode édition
    # Pré-remplir les champs avec les données existantes
    # Sauvegarder les modifications
```

**2. Suppression avec Confirmation**
```python
def delete_property(self, property_id):
    # Dialogue de confirmation
    # Suppression des médias associés
    # Suppression de la base de données
    # Rafraîchissement de la liste
```

**3. Actions en Lot**
```python
def bulk_actions(self, selected_ids, action):
    # Sélection multiple dans le Treeview
    # Actions: supprimer, exporter, changer statut
    # Barre de progression pour les opérations longues
```

#### 📁 Onglet Projects - Fonctionnalités Critiques

**1. Création de Projets**
```python
class ProjectCreationDialog:
    def __init__(self, parent):
        # Formulaire: nom, description, type, échéance
        # Sélection des propriétés à associer
        # Définition des phases du projet
```

**2. Association Propriétés ↔ Projets**
```python
def link_properties_to_project(self, project_id, property_ids):
    # Interface de sélection multiple
    # Glisser-déposer depuis l'onglet Properties
    # Visualisation des liens existants
```

#### 🎨 Onglet Templates - Fonctionnalités de Base

**1. Prévisualisation des Templates**
```python
def preview_template(self, template_id):
    # Fenêtre de prévisualisation HTML
    # Données d'exemple pour le rendu
    # Navigation entre les pages du template
```

**2. Sélection et Application**
```python
def apply_template_to_property(self, template_id, property_id):
    # Génération du site avec le template sélectionné
    # Personnalisation des couleurs et polices
    # Export vers dossier de destination
```

### Phase 2: Améliorations UX (Semaine 2)

#### Interface Utilisateur Avancée

**1. Recherche et Filtres Améliorés**
- Recherche en temps réel
- Filtres combinés (prix + type + localisation)
- Sauvegarde des recherches favorites
- Tri multi-colonnes

**2. Prévisualisation des Médias**
- Galerie d'images intégrée
- Zoom et rotation
- Métadonnées EXIF
- Édition basique (recadrage, luminosité)

**3. Drag & Drop**
- Glisser-déposer entre onglets
- Réorganisation des éléments
- Import de fichiers par glisser-déposer

### Phase 3: Fonctionnalités Avancées (Semaine 3-4)

#### Gestion de Projets Complète

**1. Phases et Tâches**
```python
class ProjectPhase:
    def __init__(self, name, start_date, end_date, tasks):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = tasks  # Liste de ProjectTask
        self.status = "pending"  # pending, in_progress, completed
```

**2. Calendrier Intégré**
- Vue calendrier des échéances
- Notifications de rappel
- Synchronisation avec calendriers externes

**3. Rapports de Projet**
- Génération PDF automatique
- Graphiques de progression
- Export Excel des données

#### Templates Avancés

**1. Éditeur Visuel**
- Interface WYSIWYG
- Glisser-déposer des composants
- Prévisualisation en temps réel
- Système de grille responsive

**2. Variables Dynamiques**
```python
template_variables = {
    '{{property.title}}': property.title,
    '{{property.price}}': format_price(property.price),
    '{{property.images}}': generate_gallery(property.images),
    '{{agent.contact}}': agent.contact_info
}
```

**3. Thèmes et Personnalisation**
- Palettes de couleurs prédéfinies
- Upload de logos personnalisés
- Polices Google Fonts
- CSS personnalisé avancé

## 🔧 Modifications Techniques Requises

### Base de Données

**Nouvelles Tables**
```sql
-- Table des projets
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT,
    status TEXT DEFAULT 'active',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Association propriétés-projets
CREATE TABLE project_properties (
    project_id INTEGER,
    property_id INTEGER,
    role TEXT,  -- 'primary', 'secondary', 'reference'
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

-- Templates personnalisés
CREATE TABLE custom_templates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,  -- 'website', 'property', 'email'
    template_data TEXT,  -- JSON avec structure du template
    preview_image BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Nouvelles Classes Core

**ProjectManager**
```python
class ProjectManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_project(self, project_data):
        # Création d'un nouveau projet
        pass
    
    def link_property(self, project_id, property_id, role='primary'):
        # Association propriété-projet
        pass
    
    def get_project_properties(self, project_id):
        # Récupération des propriétés d'un projet
        pass
```

**TemplateManager**
```python
class TemplateManager:
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
    
    def load_template(self, template_id):
        # Chargement d'un template
        pass
    
    def render_template(self, template_id, property_data):
        # Rendu avec données de propriété
        pass
    
    def save_custom_template(self, template_data):
        # Sauvegarde template personnalisé
        pass
```

## 📋 Checklist d'Implémentation

### Semaine 1: Fonctionnalités Critiques
- [ ] Édition de propriétés (modal dialog)
- [ ] Suppression avec confirmation
- [ ] Création de projets basique
- [ ] Prévisualisation des templates
- [ ] Navigation fonctionnelle entre tous les onglets

### Semaine 2: Améliorations UX
- [ ] Recherche en temps réel
- [ ] Filtres avancés
- [ ] Prévisualisation des médias
- [ ] Drag & drop basique
- [ ] Actions en lot

### Semaine 3: Fonctionnalités Avancées
- [ ] Gestion des phases de projet
- [ ] Calendrier intégré
- [ ] Éditeur de templates
- [ ] Variables dynamiques
- [ ] Rapports PDF

### Semaine 4: Finalisation
- [ ] Tests complets
- [ ] Documentation utilisateur
- [ ] Optimisation des performances
- [ ] Correction des bugs
- [ ] Préparation de la release

## 🚀 Prochaines Étapes Immédiates

1. **Corriger l'erreur "New Property"** - FAIT ✅
2. **Tester la navigation entre onglets** - EN COURS
3. **Implémenter l'édition de propriétés** - PRIORITÉ 1
4. **Ajouter la création de projets** - PRIORITÉ 2
5. **Améliorer la prévisualisation des templates** - PRIORITÉ 3

Ce plan fournit une roadmap claire pour transformer les interfaces de base existantes en fonctionnalités complètes et utilisables.