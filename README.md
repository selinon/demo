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

### Sentry

To demo Selinon's support for [Sentry monitoring](https://sentry.io), you need to configure Sentry monitoring explicitly. Don't worry - it just takes few seconds.

First, you need to run Sentry for the first time to create expected tables and relations in the database. To do so, first run system with Sentry instance:

```
$ docker-compose -f docker-compose.yaml -f docker-compose.sentry.yaml up
```

This will run system with Sentry that will be available at [http://localhost:9000](http://localhost:9000). You will not be able to log in as you need to create a user first. To create a user, run in another shell (while the system is up):

```
$ docker-compose -f docker-compose.yaml -f docker-compose.sentry.yaml run sentry sentry upgrade
```

This will run database migrations and prepare Sentry for the initial run. Once database tables are created, the upgrade command will prompt you to create a new user:

```
...
 > sentry:0357_auto__add_projectteam__add_unique_projectteam_project_team
Created internal Sentry project (slug=internal, id=1)

Would you like to create a user account now? [Y/n]: y
Email: fridex@example.com
Password: ****
Repeat for confirmation: ****
Should this user be a superuser? [y/N]: y
User created: fridex@example.com
Added to organization: sentry
 - Loading initial data for sentry.
...
```

After that your Sentry instance is configured. Open [http://localhost:9000](http://localhost:9000), log in with e-mail and password and proceed with Welcome screen (default values are just fine). Once you confirm the Welcome screen, click on the "New Project" button in the top right corner, select "Python", optionally adjust project name and click on "Create Project".

A new screen will appear with initial instructions on how to set up Python based application monitoring. In the example, copy [Sentry's DSN](https://docs.sentry.io/quickstart/#configure-the-dsn), it should look similarly to the following example:

```
http://5305e373726b40ca894d8cfd121dea34:78c848fac46040d1a3218cc0bf8ef6a7@localhost:9000/2
```

Copy the whole link and place this DSN to worker's [nodes.yaml](https://github.com/selinon/demo/blob/master/worker/myapp/config/nodes.yaml) configuration file so worker is able to report errors to Sentry instance.

Uncomment configuration entry in the `trace` configuration in `global` configuration section and substitute DSN with the copied one.

The last important step is to substitute `localhost` with `sentry` so worker can reach to Sentry in the docker-compose setup. Once you are done with editing `nodes.yaml`, restart the whole system and worker should be able to report any task failures to Sentry monitoring service.

The DSN listed above would be amended as follows (just replace `localhost` with `sentry`):

```
http://5305e373726b40ca894d8cfd121dea34:78c848fac46040d1a3218cc0bf8ef6a7@sentry:9000/2
```

And the appropriate configuration entry would be:

```yaml
    trace:
      - sentry:
          dsn: 'http://5305e373726b40ca894d8cfd121dea34:78c848fac46040d1a3218cc0bf8ef6a7@sentry:9000/2'
      # You can keep logging to stdout/stderr as well so you still see what is going on in the system:
      - logging: true
```

 * url: [http://localhost:9000](http://localhost:9000)
 * login: based on your initial setup
 * password: based on your initial setup

Note that Selinon reports only task failures (event `TASK_FAILURE`). Any other failures are ignored by default. See [Selinon docs](http://selinon.readthedocs.io/en/latest/trace.html) for more info.
