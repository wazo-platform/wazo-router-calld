from multiprocessing import Process
from typing import Optional

import click
import signal

from .consul import setup_consul


@click.command()
@click.option(
    "--consul-uri",
    type=str,
    default=None,
    help="Consul agent URI, used to obtain environment configurations and perform service discovery",
    show_default=True,
)
@click.option(
    "--api-uri", type=click.STRING, default="http://localhost:8000/", show_default=True
)
@click.option(
    "--messagebus-uri",
    type=click.STRING,
    default="pyamqp://wazo:wazo@localhost:5672//",
    show_default=True,
)
@click.option("-w", "--workers", type=click.INT, default=1, show_default=True)
@click.option(
    "-d", "--debug", is_flag=True, default=False, help="Enable debug mode.", hidden=True
)
def main(
    consul_uri: Optional[str] = None,
    api_uri: Optional[str] = None,
    messagebus_uri: Optional[str] = None,
    workers: int = 1,
    debug: bool = False,
):
    config = dict(
        consul_uri=consul_uri,
        api_uri=api_uri,
        messagebus_uri=messagebus_uri,
        debug=debug,
    )
    if consul_uri is not None:
        setup_consul(config)

    # worker constructor
    def _worker():
        from .worker import WazoRouterCalld

        worker = WazoRouterCalld(config)
        worker.run()

    # start the workers as processes
    processes = []
    for n in range(workers):
        process = Process(target=_worker)
        process.start()
        processes.append(process)
    # ignore SIGINT & SIGTERM signals in the main process
    signal.signal(signal.SIGINT, lambda signum, frame: None)
    signal.signal(signal.SIGTERM, lambda signum, frame: None)
    # wait the subprocesses to terminate
    for process in processes:
        process.join()


def main_with_env():
    main(auto_envvar_prefix="WAZO_ROUTER_CALLD")
