import click
import logging
from pathlib import PurePath
from os.path import  abspath
#from schema import SchemaError, Schema
from functools import partial
#from easysparkcli.subcommands.auxiliar.exceptions import ConfigfileValidationError, validationError
from easysparkcli.subcommands.auxiliar.conf import (
    validate_raw_config,
    read_config_file,
    validate_cluster_section,
    validate_submit_section,
    validate_k8s_section
)

switch_validations = {
    'k8s': partial(validate_k8s_section),
    'cluster': partial(validate_cluster_section),
    'submit': partial(validate_submit_section)
}

@click.option("--section",'-s',multiple=True,help="Specify a specific section to validate. If not provided, the entire configfile will be validated.")
@click.argument('configfile', nargs=1,type=click.Path(exists=True,resolve_path=True,readable=True))
@click.command()
def cli(**kwargs):
    """
    This option allow users to validate configuration file before using it.
    """
    try:
        cfgfilepath=PurePath(abspath(kwargs['configfile']))
        sections=kwargs.get("section")
        rawconfig= read_config_file(str(cfgfilepath)) #Lectura del archivo de configuración
        if len(sections) == 0:
            validate_raw_config(rawconfig) #Validacion de la configuracion completa usando el esquema
            print(f"\n* Specified configuration file \"{cfgfilepath}\" was successfully validated!\n")
        else:
            sectionsList=list(set(sections))
            for sectionName in sectionsList:
                if sectionName  in ["k8s","submit","cluster"]:
                    switch_validations.get(sectionName)(rawconfig)      
                else:
                    sectionsList.remove(sectionName)
                    print(f"* Specified section {sectionName} is not supported at the Scheme validation and is not used by the CLI,  skipping it ...\n")
            if len(sectionsList)==1:
                print(f"\n* Section {sectionsList} of the specified configuration file \"{cfgfilepath}\" was successfully validated!\n")
            elif len(sectionsList)>1:
                print(f"\n* Sections {sectionsList} of the specified configuration file \"{cfgfilepath}\" were successfully validated!\n")
    except KeyboardInterrupt:
        logging.error("""
WARNING: validation interrupted by the user!
""")                