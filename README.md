# churn-cml-dvc — DVC + S3 + GitHub Actions + CML

Ce projet est un squelette prêt pour le TP **MLOps de bout en bout** :
- versioning des data & modèles avec **DVC**
- stockage des artefacts dans **S3**
- CI/CD avec **GitHub Actions**
- rapport automatique avec **CML** (métriques + matrice de confusion)

## 1) Prérequis
- Python 3.11
- Git
- Un bucket S3 + un utilisateur IAM (Access key / Secret key)
- DVC avec support S3

## 2) Installation locale
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "dvc[s3]==3.63.0"
```

## 3) Configurer le remote S3
Édite `.dvc/config` et remplace `REPLACE_ME_BUCKET` par ton bucket.

Puis initialise DVC et fais le premier push :
```bash
git init
dvc init

# (optionnel) si tu préfères créer le remote via commande:
# dvc remote add -d myremote s3://<bucket>/dvc-storage
# dvc remote modify myremote region eu-west-3

python script.py
dvc add data models
git add .dvc .github script.py requirements.txt README.md .gitignore data.dvc models.dvc
git commit -m "Init project with DVC tracking"

# Configure AWS credentials (recommandé via env vars)
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=eu-west-3

dvc push
```

## 4) GitHub Actions + Secrets
Dans GitHub → **Settings → Secrets and variables → Actions** ajoute :
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION` (ex: `eu-west-3`)

Ensuite, chaque `git push` déclenche :
- `dvc pull`
- training `script.py`
- `dvc add` + `dvc push`
- commentaire CML avec `models/metrics.txt` et `models/conf_matrix.png`

## 5) Structure
```
.
├── .github/workflows/ci.yml
├── .dvc/config                # remote S3 (sans secrets)
├── script.py                  # train + outputs
├── requirements.txt
└── README.md
```

> ⚠️ Ne jamais committer `.dvc/config.local` (secrets).
