# selinon-demo

Demo for Selinon implementation. Please visit [Selinon](https://github.com/selinon/selinon) for more info.

Is this project helpful? [Send me a simple warm message](https://saythanks.io/to/fridex)!

## Running

Just clone the repo and run prepared docker-compose:

```bash
$ git clone https://github.com/selinon/demo.git
$ cd demo/
$ docker-compose up
```

Building and bringing up demo for the first time may take a while. Once finished, there are available services and DB frontends to easily demo the system. If you wish to visualize available available flows, just run `hack/visualize_flows.sh`.


To run a flow access API server and run flow by entering `flow_name` and `node_args` to POST request `/api/v1/ui/run-flow`.

## Simulating a flow run

If you wish to simulate a flow run without bringing the whole system up, enter `hack` directory and run:

```bash
$ cd hack/
$ ./simulate_run.sh
```

It will run prepared flow `flow1`.

*Note* that flow `flow1` does not use any storage/database so results get discarded.
*Note* that you need to have `selinon` and `selinonlib` installed. Use prepared script `install_selinon.sh` so you have recent version of Selinon.

## Generating flow graphs

To plot flow graphs, enter `hack` directory and run:

```bash
$ cd hack/
$ ./visualize_flows.sh
```

Selinonlib will generate SVG images for you in the current directory.

*Note* that you need to have `selinon` and `selinonlib` installed. Use prepared script `install_selinon.sh` so you have recent version of Selinon.

## Experimenting with flows

If you would like to change/introduce your own flows, just modify `worker/myapp/config/nodes.yaml`, if needed, and introduce changes to `worker/myapp/config/flows/`. Once done, just run `docker-compose up` again (there is no need to build worker and server again as these configs are mounted as volumes).

If you want to scale workers, just run (to scale to 10 workers):
```bash
$ docker-compose scale worker=10
```

Note that queues on message broker has to be clean, otherwise [already known Celery bug](https://github.com/celery/celery/issues/3539) can occur.

## Available services

The following listing states available services that are brought by `docker-compose`.

### API server

API server running as a thin client to message broker

 * url: [http://localhost:34000](http://localhost:34000)
 
### RabbitMQ Management

Message broker management

 * url: [http://localhost:35000](http://localhost:35000)
 * user: guest
 * password: guest
 
### Celery Flower

Real-time monitor and web admin interface for Celery.

 * [http://localhost:36000](http://localhost:36000)
 
### PGweb

A web frontend for PostgreSQL.

 * url: [http://localhost:8081](http://localhost:8081)
 
*Note:* PGweb does not retry on failure when connecting to PostgreSQL. If PostgreSQL is not ready, the PGweb container will fail. If it occurs, run `docker-compose run pgweb` to ensure that the PGweb is up.
 
### Redis Commander

A web frontend for Redis.

 * url: [http://localhost:8082](http://localhost:8082)
 
### Mongo Express

A web frontend for MongoDB.

 * url: [http://localhost:8083](http://localhost:8083)

### Minio S3

Amazon AWS S3 alternative with UI.

 * url: [http://localhost:8084](http://localhost:8084)
 * access key: E5UENY2EOTV2U7DP0ODQ
 * secret key: tfIv8oNKIpfwGYlUe8ZErnMXZzOxPhVagKBiE6qV
