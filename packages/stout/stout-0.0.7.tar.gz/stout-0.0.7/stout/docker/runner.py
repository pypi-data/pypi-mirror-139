from os import getcwd
from os.path import realpath, dirname
from docker import from_env

def context():
    return from_env()

def build(ctx):
    return ctx.images.build(
        tag='stout-runner',

        rm=True,
        forcerm=True,

        path=getcwd(),
        dockerfile=f'{dirname(realpath(__file__))}/dockerfile',
    )

def run(ctx, script):
    return ctx.containers.run(
        image='stout-runner',
        environment=[f'SCRIPT={script}'],
        name='stout-runner',
        remove=True,
    )