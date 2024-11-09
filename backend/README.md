# PixelMotion Backend

## API Server 

### Running locally
```
cd api
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
python main.py
```

### Common Package

Install common package in api
```
cd api
pip install -e ../common
```

Uninstall common package in api
```
cd api
pip uninstall pm_common
```