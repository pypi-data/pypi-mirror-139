from schema import Schema,SchemaError,Or,Optional
from configparser import ConfigParser
from os.path import expandvars

from easysparkcli.subcommands.auxiliar.exceptions import ConfigfileValidationError, validationError

from easysparkcli.subcommands.auxiliar.validations import (
    existing_file,
    nonempty_str,
    url,
    positive_int,
    memory_units,
    master_url,
    check_advanced,
    app_jar,
    booleanCheck,
    nodes_memory_units,
    existing_dir,
    existing_files
)

#TODO: Meter comprobaciones bien en cada tipo: tipos,regex...
SCHEMA= {
    'submit' : {
        Optional(str): str
    },
    'k8s': {
        Optional('ssl_ca_cert') : existing_file,
        Optional('api_key') : nonempty_str,
        Optional('api_key_prefix') : nonempty_str,
        Optional('host') : url,
        Optional('username'): nonempty_str,
        Optional('password'): nonempty_str,
        Optional('verify_ssl'): booleanCheck,
        Optional('cert_file'): existing_file,
        Optional('key_file'): existing_file,
        Optional('retries'): positive_int
    },
    'cluster': {
        'deploy_type': Or("k8s","standalone"),
        Optional(str): str
    }
}

SUBMIT_APP_SCHEMAS = {
    'k8s': {
        'master': master_url,
        'class': nonempty_str,
        'app_jar': app_jar,
        Optional('container_image'):nonempty_str,
        Optional('app_args'): nonempty_str,
        Optional('name'): nonempty_str,     
        Optional('jarsdir'):existing_dir,
        Optional('jars'):existing_files,
        Optional('libsdir'):existing_dir,
        Optional('driver_memory'):memory_units,
        Optional('driver_cores'):positive_int,
        Optional('executor_memory'):memory_units,
        Optional('executor_cores'):positive_int,
        Optional('executor_instances'): positive_int,
        Optional('historylogs_dir'):existing_dir,
        Optional('advanced'):check_advanced,
        Optional('driverlogs_file'):  nonempty_str,
    },
    'standalone': {
        'master': master_url,
        'class': nonempty_str,
        'app_jar': app_jar,
        Optional('app_args'): nonempty_str,
        Optional('name'): nonempty_str,      
        Optional('jarsdir'):existing_dir,
        Optional('jars'):existing_files,
        Optional('libsdir'):existing_dir,
        Optional('driver_memory'):memory_units,
        Optional('driver_cores'):positive_int,
        Optional('executor_memory'):memory_units,
        Optional('executor_cores'):positive_int,
        Optional('executor_instances'): positive_int,
        Optional('historylogs_dir'):existing_dir,
        Optional('advanced'):check_advanced,
        Optional('supervise'): booleanCheck,    
        Optional('driverlogs_file')   : nonempty_str 
    }
}

CLUSTER_TYPE_SCHEMAS = {
    'k8s': {
        "deploy_type": "k8s",
        Optional('node_cpus'): positive_int,
        Optional('node_memory'): nodes_memory_units,
        Optional('nodes'): positive_int,
    },
    'standalone': {
        "deploy_type": "standalone",
        Optional('workers'): positive_int,
        Optional('node_memory'): nodes_memory_units,
        Optional('node_cpus'): positive_int
    }
}

def validate_submit_section(configcontent):
    submit_section=configcontent.get("submit")
    aux={}
    if submit_section is not None:
        model_submit_section=SCHEMA["submit"]
        aux["submit"] = Schema(model_submit_section).validate(submit_section)
        type=configcontent.get("cluster")["deploy_type"].lower()
        if type is None:
            raise validationError("* In order to validate the submit option, there must be a well-formed \"cluster\" section in the specified file to know the type of cluster with which you want to work.")
        if type in ["k8s","standalone"]:
            return Schema(SUBMIT_APP_SCHEMAS[type]).validate(aux["submit"])
        else:
            raise validationError(f"* At \"cluster\" section, \"deploy_type\" key with value \"{type}\" is not valid. In order to validate the submit option, there must be a well-formed \"cluster\" section in the specified file to know the type of cluster with which you want to work.")
    else:
        raise ConfigfileValidationError(f'* Section \"submit\" was not found in the current configuration file. Please, check it')

def validate_cluster_section(configcontent):
    cluster_section= configcontent.get("cluster")
    aux={}
    if cluster_section is not None:
        model_cluster_section = SCHEMA['cluster']
        aux["cluster"] = Schema(model_cluster_section).validate(cluster_section)
        type = aux["cluster"]["deploy_type"]
        return Schema(CLUSTER_TYPE_SCHEMAS[type]).validate(aux["cluster"])
    else:
        raise ConfigfileValidationError(f'* Section \"cluster\" was not found in the current configuration file. Please, check it.')

def validate_k8s_section(configcontent):
    k8s_section=configcontent.get("k8s")
    if k8s_section is not None:
        model_k8s_schema=SCHEMA["k8s"]
        return Schema(model_k8s_schema).validate(k8s_section)
    else:
        raise ConfigfileValidationError(f'* Section \"k8s\" was not found in the current configuration file. Please, check it')

def read_config_file(filepath):
    '''
    Leer las opciones de ejecución del fichero de configuración especificado en la opción --config
    '''
    cfg= ConfigParser()
    cfg.read(filepath)
    config={}
    for section in cfg.sections():
        config[section] = {}
        for key in cfg.options(section):
            value = cfg.get(section, key)
            config[section][key] = expandvars(value)
    return config

def validate_specific_cluster_section(newconfig):
    """
    Ejecutar validación con schema correspondiente según tipo cluster solicitado
    """
    type = newconfig["deploy_type"]
    return Schema(CLUSTER_TYPE_SCHEMAS[type]).validate(newconfig)

def validate_specific_submit_section(newconfig):
    """
    Ejecutar validación con schema correspondiente según tipo de cluster contra el que se realiza el submit
    """
    type = newconfig["cluster"]["deploy_type"]
    return Schema(SUBMIT_APP_SCHEMAS[type]).validate(newconfig["submit"])

def validate_raw_config(rawconfig):
    """
    Función para validar el fichero de configuración en su totalidad usando el schema.
    """
    
    newconfig = {}
    #Validamos primero siempre sección cluster, ya que de esta sección depende el modelo de submit a aplicar
    data = rawconfig.get("cluster")
    try:

        if data is not None:
                modelClusterSection = SCHEMA['cluster']
                newconfig["cluster"] = Schema(modelClusterSection).validate(data)
                newconfig["cluster"] = validate_specific_cluster_section(newconfig['cluster'])
        else:
            raise ConfigfileValidationError('Section \'cluster\' must exist in the configuration file. Please, rewrite it') from None

        for section,model in SCHEMA.items():
            if section not in rawconfig or section == 'cluster':
                continue
            data = rawconfig[section]
            newconfig[section] = Schema(model).validate(data)

            if section == 'submit':
                newconfig[section] = validate_specific_submit_section(newconfig)
    except (SchemaError, ValueError) as error:
                raise ConfigfileValidationError(f'\n{error}'.format(error)) from None

    return newconfig
    