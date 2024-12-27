import os
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

# TODO - improve psae config/credential options

@cli.group()
def tuxedo():
    """Working with Tuxedo cache"""
    pass

@tuxedo.command("loadcache")
@click.option('-db','--database',
              required=True,
              help="Database")
@click.option('-un','--username',
              required=True,
              help="Username")
@click.option('-up','--userpass',
              required=True,
              help="Userpass")
@click.option('-ci','--connect-id',
              required=True,
              help="Connect ID")
@click.option('-cp','--connect-pw',
              required=True,
              help="Connect Password")
@click.option('-d', '--ps-servdir',
              required=True,
              help="Directory used to store generated cache")
@click.option('-r', '--rebase', 
              default="false",
              show_default=True,
              help="Delete current generated cache to rebase")
def loadcache(rebase, ps_servdir, ps_home, database, username, userpass, connect_id, connect_pw):
    """Run the LOADCACHE program to generate cache"""
 
    #TODO logger.setLevel(logging.DEBUG if debug else logging.INFO)
    debug = True

    # validate ps_servdir
    if not os.path.isdir(ps_servdir):
        print(f"Error: The PS_SERVDIR directory '{ps_servdir}' does not exist.")
        exit(1) 

    # validate ps_home - TODO
    #ps_home_env = os.getenv('PS_HOME')
    #if ps_home_env is None:
    #    print(f"Error: Environment variable 'PS_HOME' is not set.")
    #    exit(1)

    # validate psae - TODO


    # rebase - TODO
#        if reset:
#            logger.info("Removing previous cache")
#            for path in [
#                f"{ps_servdir}/CACHE/1/*.DAT",
#                f"{ps_servdir}/CACHE/1/*.KEY",
#                f"{ps_servdir}/CACHE/STAGE/stage/*.DAT",
#                f"{ps_servdir}/CACHE/STAGE/stage/*.KEY",
#            ]:
#                subprocess.run(["rm", "-rf", path], check=False)
#
#        logger.info("Run LOADCACHE [ Task ]")
#        logger.info("Environment: %s", os.environ)
#        logger.info("-------------------")
#

    # run LOADCACHE
    command = [
        "psae",
        "-CT", "ORACLE",
        "-CD", database.upper(),
        "-CO", username,
        "-CP", userpass,
        "-R", "LOADCACHE",
        "-AI", "LOADCACHE",
        "-CI", connect_id,
        "-CW", connect_pw
    ]

    try:
        if debug:
            subprocess.run(command, check=True)
        else:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # TODO logger.info("Run LOADCACHE [ Done ]")
    except subprocess.CalledProcessError as e:
        # TODO logger.error("Run LOADCACHE [ Error ]")
        # TODO logger.error("  Result Code: %s", e.returncode)
        return e.returncode

    return 0

@tuxedo.command("copycache")
@click.option('-d','--domain',
              required=True,
              help="App server domain name")
@click.option('-pd', '--ps-servdir',
              help="Directory used to store generated cache")
@click.option('-pc','--ps-cfg-home',
              help="PS_CFG_HOME")
@click.option('-r','--rebase',
              help="Rebase cache")
def copycache(domain, ps_servdir, ps_cfg_home, rebase):
    """Copy generated cache to PSAPPSRVs"""
    #debug = True
    #TODO logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # validate ps_servdir
    ps_servdir = os.getenv('PS_SERVDIR')
    if ps_servdir is None:
        print(f"Error: Environment variable 'PS_SERVDIR' is not set.")
        sys.exit(1)  # Exit the program with a non-zero status to indicate failure

    # validate ps_cfg_home
    ps_cfg_home = os.getenv('PS_CFG_HOME')
    if ps_cfg_home is None:
        print(f"Error: Environment variable 'PS_CFG_HOME' is not set.")
        sys.exit(1)  # Exit the program with a non-zero status to indicate failure

    # check if file exists
    psappsrv_cfg = f"{ps_cfg_home}/appserv/{domain}/psappsrv.cfg"
    if not os.path.exists(psappsrv_cfg):
        print(f"Error: The file '{psappsrv_cfg}' does not exist.")
        sys.exit(1)  # Exit the program with a non-zero status to indicate failure

    # find MIN appsrv setting
    config = configparser.ConfigParser()
    config.read(psappsrv_cfg)
    if config.has_section('PSAPPSRV'):
        minsetting = config.get('PSAPPSRV','Min Instances')
        print(f"PSAPPSRV Min: {minsetting}")

    # rebase TODO
#    if [[ ${RESET} == "true" ]]; then
#      echoinfo "Remove Existing CACHE Files [ Task ]"
#      for ((i=1; i<=minsetting; i++))
#      do
#        rm -rf $PS_CFG_HOME/appserv/${ENVIRONMENT}/CACHE/PSAPPSRV_${i}/*
#      done
#      echoinfo "Remove Existing CACHE Files [ Done ]"
#    fi

    # copy generated cache
    for i in range(1, int(minsetting) + 1):
        target_dir = os.path.join(ps_cfg_home, 'appserv', domain, 'CACHE', f'PSAPPSRV_{i}')
        os.makedirs(target_dir, exist_ok=True)
        shutil.copytree(os.path.join(ps_servdir, 'CACHE', 'STAGE', 'stage'), target_dir, dirs_exist_ok = True)
        print(f"Created and copied to {target_dir}")

    return 0

