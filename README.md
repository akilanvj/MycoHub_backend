# MyCO Backend services


### To create virtual environment and activate 

```
python3 -m venv venv
```

```
source venv/bin/activate
```

To deactivate the python virtualenv
```
deactivate
```

### To install the requirement packages
```
 pip3 install -r requirements.txt
```


Start the Redis docker container
```
docker-compose up -d
```

To run the server

```
uvicorn main:app --host 0.0.0.0 --port 8000
```