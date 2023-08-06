from click import command, argument, option, echo
from stout.docker import context as docker_context, build as docker_build, run as docker_run

from json import loads as json_loads

@command()
@argument('script')
@option('-v', '--verbose', is_flag=True)
def run_script(script, verbose):
    ctx = docker_context()
    
    _, builder = docker_build(ctx)
    if verbose:
        for chunk in builder:
            if 'stream' in chunk:
                    echo(chunk['stream'].strip('\n'))

    output = docker_run(ctx, script)

    print(output)

def main():
    run_script()