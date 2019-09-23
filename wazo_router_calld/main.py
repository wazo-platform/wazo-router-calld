import click
import uvicorn

from .app import get_app


@click.command()
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
@click.option(
    "--consul-uri",
    type=str,
    default=None,
    help="Consul agent URI, used to obtain environment configurations and perform service discovery",
    show_default=True,
)
@click.option(
    "--database-uri",
    type=str,
    default="postgresql://wazo:wazo@localhost/wazo",
    help="SQLAlchemy database URI, overwrites the configuration obtained from the Consul agent",
    show_default=True,
)
@click.option(
    "--debug", is_flag=True, default=False, help="Enable debug mode.", hidden=True
)
def main(
    host: str = None,
    port: int = None,
    consul_uri: str = None,
    database_uri: str = None,
    debug: bool = False,
):
    config = dict(
        host=host,
        port=port,
        consul_uri=consul_uri,
        database_uri=database_uri,
        debug=debug,
    )
    app = get_app(config)
    log_level = "info" if not config['debug'] else "debug"
    uvicorn.run(
        app,
        host=config['host'],
        port=config['port'],
        log_level=log_level,
        reload=config['debug'],
    )


def main_with_env():
    main(auto_envvar_prefix="WAZO_ROUTER_CALLD")
