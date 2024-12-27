import os
import glob
import shutil
import subprocess
import time
import logging
import click
import configparser

class Config(object):

    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(no_args_is_help=True)
@pass_config
def cli(config):
    """PeopleSoft Cache Tool"""
    pass    

@cli.group()
def tuxedo():
    """Working with Tuxedo cache"""
    pass

@tuxedo.command("loadcache", context_settings={'show_default': True})
@click.option('-db','--database',
              required=True,
              help="Database")
@click.option('-o','--options-file',
              default=f"{os.getenv('HOME')}/psae.options",
              help="Location to store temporary options file for AE")
@click.option('-sd', '--ps-servdir',
              required=True,
              help="Directory used to store generated cache")
@click.option('-r', '--rebase', 
              is_flag=True,
              help="Delete current generated cache to rebase")
def loadcache(options_file, rebase, ps_servdir, database):
    """Run the LOADCACHE program to generate cache"""

    # Validate ps_servdir
    os.environ["PS_SERVDIR"] = ps_servdir
    if not os.path.isdir(ps_servdir):
        print(f"Error: The PS_SERVDIR directory '{ps_servdir}' does not exist.")
        exit(1) 

    # Validate credentials set as environment variables
    username = os.getenv('PSC_USER')
    if username is None:
        print(f"Error: Environment variable 'PSC_USER' is not set.")
        exit(1)

    userpass = os.getenv('PSC_PASS')
    if userpass is None:
        print(f"Error: Environment variable 'PSC_PASS' is not set.")
        exit(1)

    connect_id = os.getenv('PSC_CONN_ID')
    if connect_id is None:
        print(f"Error: Environment variable 'PSC_CONN_ID' is not set.")
        exit(1)

    connect_pw = os.getenv('PSC_CONN_PW')
    if connect_pw is None:
        print(f"Error: Environment variable 'PSC_CON_PW' is not set.")
        exit(1)

    # Rebase cache
    if rebase:
        print("INFO: Rebase by removing previous cache")
        patterns = [
            f"{ps_servdir}/CACHE/1/*.DAT",
            f"{ps_servdir}/CACHE/1/*.KEY",
            f"{ps_servdir}/CACHE/STAGE/stage/*.DAT",
            f"{ps_servdir}/CACHE/STAGE/stage/*.KEY"
        ]

        for p in patterns:
            for f in glob.glob(p):
                os.remove(f)

    # Prepare options file
    print(f"INFO: Generating options file '{options_file}'. This will be deleted after succesful AE run.")
    with open(options_file, 'w+') as file:
        file.write(f"-CT ORACLE\n")
        file.write(f"-CD {database.upper()}\n")
        file.write(f"-R LOADCACHE\n")
        file.write(f"-AI LOADCACHE\n")
        file.write(f"-DR Y\n") # disable restart
        file.write(f"-CO {username}\n")
        file.write(f"-CP {userpass}\n")
        file.write(f"-CI {connect_id}\n")
        file.write(f"-CW {connect_pw}\n")

    # Run LOADCACHE
    command = [
        "psae",
        options_file
    ]

    try:
        print(f"INFO: Running LOADCACHE and generating to {ps_servdir}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return e.returncode

@tuxedo.command("copycache", context_settings={'show_default': True})
@click.option('-d','--domain',
              required=True,
              help="App server domain name")
@click.option('-sd','--ps-servdir',
              required=True,
              help="Directory used to store generated cache")
@click.option('-r','--rebase',
              is_flag=True,
              help="Rebase cache")
def copycache(domain, ps_servdir, ps_cfg_home, rebase):
    """Copy generated cache to PSAPPSRVs"""

    # Validate ps_servdir
    os.environ["PS_SERVDIR"] = ps_servdir
    if not os.path.isdir(ps_servdir):
        print(f"Error: The PS_SERVDIR directory '{ps_servdir}' does not exist.")
        exit(1) 
    ps_servdir = os.getenv('PS_SERVDIR')

    # Validate ps_cfg_home
    ps_cfg_home = os.getenv('PS_CFG_HOME')
    if ps_cfg_home is None:
        print(f"Error: Environment variable 'PS_CFG_HOME' is not set.")
        sys.exit(1)

    # Check if cfg file exists
    psappsrv_cfg = f"{ps_cfg_home}/appserv/{domain}/psappsrv.cfg"
    if not os.path.exists(psappsrv_cfg):
        print(f"Error: The file '{psappsrv_cfg}' does not exist.")
        sys.exit(1)

    # Get Min Instances setting
    config = configparser.ConfigParser()
    config.read(psappsrv_cfg)
    if config.has_section('PSAPPSRV'):
        minsetting = config.get('PSAPPSRV','Min Instances')
        print(f"INFO: PSAPPSRV Min {minsetting}")

    # Rebase cache
    if rebase:
        print("INFO: Rebase by removing previous cache")
        for i in range(1, int(minsetting) + 1):
            for f in glob.glob(f"{ps_cfg_home}/appserv/{domain}/CACHE/PSAPPSRV_{i}/*"):
                os.remove(f)

    # Copy generated cache
    for i in range(1, int(minsetting) + 1):
        target_dir = os.path.join(ps_cfg_home, 'appserv', domain, 'CACHE', f'PSAPPSRV_{i}')
        os.makedirs(target_dir, exist_ok=True)
        shutil.copytree(os.path.join(ps_servdir, 'CACHE', 'STAGE', 'stage'), target_dir, dirs_exist_ok = True)
        print(f"INFO: Copied to {target_dir}")
