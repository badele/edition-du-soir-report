# Summary

## Init env

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
# Get last datas
rm -rf /tmp/opencovid19
git clone git@github.com:opencovid19-fr/data.git /tmp/opencovid19

# Convert datas
source .venv/bin/activate
python convert_to_csv.py -p /tmp/opencovid19/ministere-sante > index.html

# Serve data (development server)
python convert_to_csv.py -p /tmp/opencovid19/ministere-sante -s  # saved in templates/index.html
export FLASK_APP=app.py && flask run
```

