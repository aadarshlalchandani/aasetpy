<!-- Modify **`README.md`** as per your project -->
<!-- credits: aadarshlalchandani/aasetpy -->

# your_project_name

## Setup the Virtual Environment

Open terminal in an empty folder

You can run this command by following instructions [here](https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68?permalink_comment_id=5315260#gistcomment-5315260).

```bash
aasetpy
```

## Run your python scripts

```bash
./run.sh python_filename
```
The File Logs will be stored in `logs/<python_filename>_logs.log`.

<details>

<summary>
<h2 style="display: inline;">
Containerization of the your_project_name
</h2>
</summary>

### Containerize and Start the Project inside container

```bash
sudo docker-compose up --build -d
```

### Access the real time project logs

```bash
sudo docker exec -it DOCKER_IMAGE_NAME tail -f logs/main_logs.log
```

### Access all logs in the docker container with filename

```bash
sudo docker exec -it DOCKER_IMAGE_NAME sh -c 'for file in logs/*.log; do echo "File: $file"; cat "$file"; echo -en "\n\n"; done'
```

### Access Docker Container

```bash
sudo docker ps --filter name=DOCKER_IMAGE_NAME
```

### Stop the API Docker Container

```bash
sudo docker stop $(sudo docker ps -aq --filter name=DOCKER_IMAGE_NAME)
```

</details>
