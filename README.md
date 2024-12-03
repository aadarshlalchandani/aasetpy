Modify **`README.md`** as per your project

# python-project

## Setup the Virtual Environment

```bash
rm -rf ~/.wget-hsts && wget -q -O - https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68/raw | bash
```

You can follow instructions in the last comment [here](https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68/raw)

## Run your python scripts

```bash
./run.sh python_file_name
```

<details>

<summary>
<h2 style="display: inline;">
Containerization of the Python Project
</h2>
</summary>

### Containerize and Start the Project inside container

```bash
sudo docker-compose up --build -d
```

### Access the real time project logs

```bash
sudo docker exec -it docker_image_name tail -f logs/main_logs.log
```

### Access all logs in the docker container with filename

```bash
sudo docker exec -it docker_image_name sh -c 'for file in logs/*.log; do echo "File: $file"; cat "$file"; echo -en "\n\n"; done'
```

### Access Docker Container

```bash
sudo docker ps --filter name=docker_image_name
```

### Stop the API Docker Container

```bash
sudo docker stop $(sudo docker ps -aq --filter name=docker_image_name)
```

</details>
