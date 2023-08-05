import os
import sys
import boto3
import botocore
import sagemaker
import json
import yaml
import time
import shutil
import zipfile
import pandas as pd
from typing import Union, List
from tqdm.notebook import tqdm
from time import sleep
from io import BytesIO
from yaspin import yaspin
from yaspin.spinners import Spinners
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor, as_completed

session = boto3.Session()

sm_client = session.client('sagemaker')

class Settings:
    spinner_type = Spinners.clock
    spinner_color = 'blue'
    spinner_ok = '✅'
    spinner_fail = '💥'

def create_or_update_iam_role(role_name: str, role_desc: str, asume_role_policy_document: dict, policy_name: str, policy_document: dict) -> str:
    '''
    Given a role name, roles description, a policy document and asume role policy document, creates or updates an IAM role
    
    Args:
        role_name (str): IAM role name
        role_desc (str): role description
        asume_role_policy_document (dict): policy document that grants an IAM entity permission to assume the role
        policy_name (str): name of the policy document
        policy_document (dict): the policy document
        
    Returns:
        role_arn (str): arn of the role created or updated
    '''
    
    iam = session.client('iam')
    
    response = None
    try:
        role_response = iam.get_role(RoleName=role_name)                 
        
        print('INFO: Role already exists, updating it...')
        role_arn = role_response['Role']['Arn']
        
        iam.update_role(RoleName=role_name, Description=role_desc)
                        
        iam.update_assume_role_policy(RoleName=role_name, PolicyDocument=json.dumps(asume_role_policy_document))
                        
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document))
        
        print('INFO: Role updated: {}'.format(role_name))
        
        response = role_arn
        
    except iam.exceptions.NoSuchEntityException as e:
        print('INFO: Role does not exist, creating it...')
        try:
            create_role_response = iam.create_role(           
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(asume_role_policy_document),
                Description=role_desc)                     
            
            role_arn = create_role_response['Role']['Arn']

            iam.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document))
            
            print('INFO: Role created: {}'.format(role_arn))
            
            response = role_arn
            
        except Exception as e:
            print('ERROR: Failed to create role: {}'.format(role_name))
            print(e)
            
    except Exception as e:
        print('ERROR: Failed to update role: {}'.format(role_name))
        print(e)
        
    return response

def create_codebuild_execution_role(role_name: str, policy_document: dict) -> str:
    '''
    Given a role name, and a policy document creates or updates an IAM role for CodeBuild jobs
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        role_arn (str): arn of the role created or updated
    '''
    
    
    
    assume_role_document={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "codebuild.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for CodeBuild', 
                                         asume_role_policy_document = assume_role_document,
                                         policy_name = 'CodeBuildExecutionPolicy',
                                         policy_document = policy_document)
    
    # Wait for role to propagate
    sleep(60)
    
    return response

def create_lambda_execution_role(role_name: str, policy_document: dict) -> str:    
    '''
    Given a role name, and a policy document creates or updates an IAM role for Lambda functions
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        role_arn (str): arn of the role created or updated
    '''
    lambda_asume_role_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for Lambda functions', 
                                         asume_role_policy_document = lambda_asume_role_document,
                                         policy_name = 'LambdaExecutionPolicy',
                                         policy_document = policy_document)
    
    # Wait for role to propagate
    sleep(60)
    
    return response
    

def create_pipeline_execution_role(role_name: str, policy_document: dict) -> str:    
    '''
    Given a role name, and a policy document creates or updates an IAM role for SageMaker Pipelines
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        role_arn (str): arn of the role created or updated
    '''
    assume_role_document={
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": "events.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }]
        }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for EventBridge', 
                                         asume_role_policy_document = assume_role_document,
                                         policy_name = 'CodeBuildExecutionPolicy',
                                         policy_document = policy_document)

    # Wait for role to propagate
    sleep(60)
    
    return response
    


def create_secret(secret_name: str, username: str, password: str) -> None:
    '''
    Given a secret name, user name and a password creates or updates Secret on Secrets Manager
    
    Args:
        secret_name (str): Secret name to create or update
        username (str): User name to store on the secret
        password (str): Password to store on the secret
        
    '''
    secretsmanager = session.client('secretsmanager')
    secret_string = f'{{"username":"{username}","password":"{password}"}}'
    description = 'Docker hub credentials'

    try:
        secretsmanager.create_secret(Name=secret_name,
                                     Description=description,
                                     SecretString=secret_string)
        print('INFO: Secret created')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            print('INFO: Secret already exists, updating it...')
            try:
                secretsmanager.update_secret(SecretId=secret_name,
                                             Description=description,
                                             SecretString=secret_string)
                print(f'INFO: Secret {secret_name} updated')
            except Exception as e:
                print(f'ERROR: Failed to create secret: {secret_name}')
                print(e)
        else:        
            print('ERROR: Failed to create secret')
            print(e) 

def create_image_repository(repository_name: str) -> None:
    '''
    Given a repository name creates a repository on ECR if it doesn't exist
    
    Args:
        repository_name (str): Repository name to be created
        
    '''
    ecr = session.client('ecr')
    try:
        repositories = ecr.describe_repositories(repositoryNames=[repository_name])['repositories']
        if len(repositories) > 0:
            print(f'INFO: Repository {repository_name} already exists')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'RepositoryNotFoundException':
            ecr.create_repository(repositoryName=repository_name)
        else:
            print('ERROR: Failed to describe repository: {}'.format(repository_name))
            print(e)

def _remove_path_prefix(path: str) -> str:
    prefixes = './,../,/'.split(',')
    to_remove = list(filter(path.startswith, prefixes))
    return path if len(to_remove)==0 else path.replace(to_remove[0],'',1)  

def _add_path_sufix(path: str) -> str:
    if os.path.isdir(path) and path[-1]!='/':
        path += '/'
    return path
        
def _fix_path(path: str) -> str:
    return _add_path_sufix(_remove_path_prefix(path))
    
def build_and_publish_docker_image(image_name: str, working_directory: str, docker_file: str, s3_path: str, role: str, **kwargs) -> str: 
    #Create build spec
    build = {'version':0.2,
             'phases':{'pre_build':{'commands':[
                 'echo Logging in to Amazon ECR...',
                 'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com',
                 'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 763104351884.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com']},
                       'build':{'commands':[
                 'echo Build started on `date`',
                 'echo Building the Docker image...',
                 'docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .',
                 'docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG']},
                       'post_build':{'commands':[
                 'echo Build completed on `date`',
                 'echo Pushing the Docker image...',
                 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG',                 
                 'echo Pushing completed on `date`',]}
                      }
            }
    
    if 'secret' in kwargs:
        build['phases']['pre_build']['commands'].append('docker login -u $dockerhub_username -p $dockerhub_password')
    
    with open(os.path.join(working_directory,'buildspec.yml'), 'w') as f:
        yaml.dump(build, f)
        
    
    zip_file_name = os.path.join(working_directory, f'{image_name}.zip')
    
    #Remove file if already exists
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
    
    #Create source package
    def zipdir(path, ziph):
        #base=path.split('/')[0]
        base='/'.join(path.split('/')[:-1])
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),os.path.join(root, file).replace(f'{base}/',''))
                replace = os.path.join(root, file).replace(f'{base}/','')
        
    with zipfile.ZipFile(zip_file_name, mode='w') as zf:
        zf.write(os.path.join(working_directory,'Dockerfile'),'Dockerfile')
        zf.write(os.path.join(working_directory,'buildspec.yml'),'buildspec.yml')
    
        #Copy dependencies
        for dependency, _ in kwargs.get('dependencies',[]):
            if os.path.isdir(dependency):
                shutil.copytree(dependency, os.path.join(working_directory, _remove_path_prefix(dependency)))                
                zipdir(os.path.join(working_directory, dependency.split('/')[-1]), zf)
                
            elif os.path.isfile(dependency):
                dest = os.path.join(working_directory,_remove_path_prefix(dependency))
                dest_folder = os.path.dirname(dest)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                shutil.copy(dependency, dest)
                zf.write(dest,_remove_path_prefix(dependency))
                
            else:
                print(f'ERROR: unable to copy dependency: {dependency}')
                

    #Upload to S3
    source_location = upload(zip_file_name,s3_path,show_progress=False).replace('s3://','')

    codebuild = session.client('codebuild')
                         
    region = sagemaker.Session().boto_region_name
    account_id = sagemaker.Session().account_id()
    project_name = f'{image_name}-build-image'
    parameters = {'name': project_name,
                  'description':'Builds a docker image to be used with SageMaker',
                  'source':{'type':'s3', 'location':source_location},
                  'artifacts':{'type':'NO_ARTIFACTS'},
                  'environment':{'type':'LINUX_CONTAINER',
                                 'image':'aws/codebuild/standard:4.0',
                                 'computeType':'BUILD_GENERAL1_SMALL',
                                 'environmentVariables':[{'name':'AWS_DEFAULT_REGION',
                                                          'value':region},
                                                         {'name':'AWS_ACCOUNT_ID',
                                                          'value':account_id},
                                                         {'name':'IMAGE_REPO_NAME',
                                                          'value':image_name},
                                                         {'name':'IMAGE_TAG',
                                                          'value':'latest'}],
                                 'privilegedMode':True},
                  'serviceRole':role}
    
    if 'secret' in kwargs:
        secret_name = kwargs['secret']
        parameters['environment']['environmentVariables'].append({'name':'dockerhub_username',
                                                                  'value':f'{secret_name}:username',
                                                                  'type':'SECRETS_MANAGER'})
        parameters['environment']['environmentVariables'].append({'name':'dockerhub_password',
                                                                  'value':f'{secret_name}:password',
                                                                  'type':'SECRETS_MANAGER'})
    try:
        codebuild.create_project(**parameters)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            codebuild.update_project(**parameters)
        else:
            print('ERROR: Failed to create codebuild project')
            print(e)                  
                         
    try:
        build_id = codebuild.start_build(projectName=project_name)['build']['id']   
        
        if kwargs.get('wait',True):                         
            with yaspin(Settings.spinner_type , text='Building docker image', color=Settings.spinner_color) as sp:         
                while True:            
                    build_response = codebuild.batch_get_builds(ids=[build_id])
                    status = build_response['builds'][0]['buildStatus']            
                    if status != 'IN_PROGRESS':
                        sp.write(f'{image_name.ljust(48,".")}{status}')
                        if status == 'SUCCEEDED':
                            sp.ok(Settings.spinner_ok)                                                                                    
                            return f'{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest'
                        else:                            
                            sp.fail(Settings.spinner_fail)
                            raise Exception(f'{image_name} {status} ')                        
                    else:                        
                        time.sleep(10)
        else:
            return build_id

    except botocore.exceptions.ClientError as e:
        print('ERROR: Failed to start codebuild project')
        print(e) 

def wait_for_build(codebuild_ids: list) -> None:
    '''
    Given a code build ids list creates waits for those builds on Code Build to finish
    
    Args:
        codebuild_ids (str): Code build ids
        
    '''
    codebuild = session.client('codebuild')

    region = sagemaker.Session().boto_region_name
    account_id = sagemaker.Session().account_id()
                         
    finished = True
    latest_status = {}          

    with yaspin(Settings.spinner_type , text="Building docker images", color=Settings.spinner_color) as sp:
        while True:
            build_response = codebuild.batch_get_builds(ids=codebuild_ids)
            for response in build_response['builds']:  
                if response['buildStatus'] != 'IN_PROGRESS':                    
                    if response['id'] not in latest_status:
                        sp.write(f'{response["id"].split(":")[0].ljust(48,".")}{response["buildStatus"]}!')
                        latest_status[response['id']] = response['buildStatus']
                else:
                    finished = False
                
                            
            if finished:                  
                if len([latest_status[status] for status in latest_status if latest_status[status] == 'SUCCEEDED']) == len(latest_status):
                    sp.ok(Settings.spinner_ok)
                    break
                else:
                    sp.fail(Settings.spinner_fail)
                    raise Exception('Building some images failed!')                
            else:
                finished = True
                time.sleep(10)
    
    image_uris = {}
    for codebuild_id in codebuild_ids:
        image_name = codebuild_id.split(":")[0].replace("-build-image","")
        image_uris[codebuild_id] = f'{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest'
                      
    return image_uris                   
       
def create_docker_file(file_name, base_image, libraries, **kwargs):
    with open(file_name,'w') as f:
        f.write(f'FROM {base_image}')
        f.write('\n\n')
        f.write('RUN rm -rf /usr/share/man/man1/; mkdir /usr/share/man/man1/ \n')
        f.write('\n')
        f.write('RUN apt-get update -y && apt-get -y install python3-dev gcc --no-install-recommends default-jdk \n')
        f.write('\n')
        
        f.write('RUN pip3 install --no-cache-dir --upgrade pip \n')
        f.write('\n') 
        
        f.write('RUN pip3 install retrying')
        for library in libraries:
            f.write(f' \\\n    {library}=={libraries[library]}')
        f.write('\n\n')            
        
        for dependency in kwargs.get('dependencies',[]):
            f.write(f'COPY {_fix_path(dependency[0])} {dependency[1]}\n')
        f.write('\n')        
        
        for cmd in kwargs.get('others',[]):
            f.write(f'{cmd} \n')
            f.write('\n')
        
        f.write('ENV PYTHONDONTWRITEBYTECODE=1 \\\n')
        f.write('    PYTHONUNBUFFERED=1 \\\n')
        f.write('    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib" \\\n')
        f.write('    PYTHONIOENCODING=UTF-8 \\\n')
        f.write('    LANG=C.UTF-8 \\\n')
        f.write('    LC_ALL=C.UTF-8')
        for variable in kwargs.get('env',{}):
            f.write(f' \\\n    {variable}={env[variable]}')
            
        if 'entrypoint' in kwargs:
            f.write('\n\n')
            f.write(f'ENTRYPOINT {json.dumps(kwargs["entrypoint"])}')
            
        if 'cmd' in kwargs:
            f.write('\n\n')
            f.write(f'CMD {json.dumps(kwargs["cmd"])}')
            
def create_docker_image(image_name: str, base_image: str, libraries: dict, s3_path: str, role: str, **kwargs)->str:
    '''
    Creates a custom Docker image to be used with SageMaker using Code Build 
    
    Args:
        image_name (str): Docker image name
        base_image (str): base image to be used to build the new Docker image
        libraries (dict): set of libraries to install on the Docker image
        s3_path (str): S3 path where the Docker image files are going to be stored
        role (str): 
        **kwargs: other parameters
            wait (bool): whether to wait for the build process to finish or not
            secret (str): secret name to be used to pull the base image
        
    Returns:
        role_arn (str): arn of the role created or updated
    '''
     #Create working directory
    working_directory = os.path.join('docker_images', image_name)
    if os.path.exists(working_directory):
        shutil.rmtree(working_directory)
    os.makedirs(working_directory)
    
    docker_file = os.path.join(working_directory,'Dockerfile')
    create_docker_file(docker_file, base_image, libraries, **kwargs)
    create_image_repository(image_name)
    return build_and_publish_docker_image(image_name, working_directory, docker_file, s3_path, role, **kwargs)  
            
def wait_for_training_jobs(estimators):
    statuses = ['Completed','Failed','Stopped']
    while True:
        finished = True        
        
        latest_status = {}
        for estimator in estimators:     
            latest_training_job = estimators[estimator].latest_training_job.describe()
            status = latest_training_job['TrainingJobStatus']
            job_name = latest_training_job['TrainingJobName']
            latest_status[job_name]=status
            finished *= status in statuses
            sys.stdout.write('.')
            
        if finished:
            sys.stdout.write('\n')
            for job_name in latest_status:
                print(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')            
            break
        else:
            time.sleep(10)
        
def wait_for_optmimization_jobs(tuners):
    statuses = ['Completed','Failed','Stopped']
    while True:
        finished = True        
        
        latest_status = {}
        for tuner in tuners:
            optimization_job = tuners[tuner].describe()
            status = optimization_job['HyperParameterTuningJobStatus']
            job_name = optimization_job['HyperParameterTuningJobName']
            latest_status[tuner]=status
            finished *= status in statuses
            sys.stdout.write('.')
            
        if finished:
            sys.stdout.write('\n')
            for job_name in latest_status:
                print(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')    
            break
        else:
            time.sleep(10)

def wait_for_transform_jobs(transformers):
    statuses = ['Completed','Failed','Stopped']
    while True:
        finished = True        
        
        latest_status = {}
        for transform in transformers:
            job_name = transformers[transform].latest_transform_job.job_name
            status = sm_client.describe_transform_job(TransformJobName=job_name)['TransformJobStatus']
            latest_status[job_name]=status
            finished *= status in statuses
            sys.stdout.write('.')
            
        if finished:
            sys.stdout.write('\n')
            for job_name in latest_status:
                print(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')    
            break
        else:
            time.sleep(10)


def create_lambda_function(**kwargs): 
    lambda_client = session.client('lambda')
    
    response = {None}
    try:
        function_name = kwargs['FunctionName']
        response = lambda_client.get_function(FunctionName=function_name)  
                    
        #Update function, because it was found. So, it does already exist
        code = None
        if 'Code' in kwargs:
            code = kwargs.pop('Code')
            
        kwargs.pop('PackageType')

        response = lambda_client.update_function_configuration(**kwargs)        
              

        if code != None:
    
            update_parameters = {
                'FunctionName':function_name,
                'Publish':True}

            update_parameters.update(code)
            response = lambda_client.update_function_code(**update_parameters)
        
        
    except lambda_client.exceptions.ResourceNotFoundException as e:
        try:
            #Create function, because it doesn't exist
            response = lambda_client.create_function(**kwargs)
          
        except botocore.exceptions.ClientError as e:
            print('Failed to create function: {}'.format(kwargs['FunctionName']))
            print(e)            
    except botocore.exceptions.ClientError as e:
        print('Failed to update function: {}'.format(kwargs['FunctionName']))
        print(e)   
        
    return response

def list_model_packages(model_package_group_name):
    model_packages_paginator = sm_client.get_paginator('list_model_packages')
    model_packages_iterator = model_packages_paginator.paginate(ModelPackageGroupName=model_package_group_name)
    return [model_package for model_packages_page in model_packages_iterator for model_package in model_packages_page['ModelPackageSummaryList']]


def delete_model_package(mdel_package_name):
    sm_client.delete_model_package(ModelPackageName=mdel_package_name)
    

def delete_model_packages(model_package_group_name):
    model_packages = list_model_packages(model_package_group_name)
    for model_package in model_packages:
        delete_model_package(model_package['ModelPackageArn'])
        
def delete_project(project_name):
    sm_client.delete_project(ProjectName=project_name)

def get_processor_output_path(processor, output_name):
    return next((output.destination 
               for output in processor.latest_job.outputs 
                   if output.output_name == output_name),
           None) 

def upload(files: Union[str, List[str]], s3_path: str, show_progress=True) -> Union[str, None]:
    '''
    Upload files or directories to S3
    
    Args:
        files (list|str): file|dir name or list of files or directories to upload to S3
        s3_path (str): S3 path where the files are going to be uploaded
        show_progress (bool): whether to show the progress of the upload
        
    Returns:
        s3_path: s3 path where the file was uploaded, if was a list of files, it doesn't return anything
    '''
    GB = 1024 ** 3
    MULTIPART_THRESHOLD = GB/200
    MAX_CONCURRENCY = 10
    NUM_DOWNLOAD_ATTEMPTS = 10
    USE_THREADS = True

    s3 = session.client('s3')

    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    prefix = '/'.join(path_parts)    

    files = [files] if isinstance(files,str) else files if isinstance(files, list) else None

    if files == None:
        raise Exception(f"You have to specify the file or files you want to upload to S3.")

    def get_total_size(files):
        total_size = 0
        for path in files:                
            if os.path.isfile(path):                                                        
                total_size += os.stat(path).st_size
            elif os.path.isdir(path):        
                for (root,dirs,files) in os.walk(path, topdown=True):
                    for file in files:    
                        file_path = os.path.join(root,file)                                                                            
                        total_size += os.stat(file_path).st_size
        return total_size 

    def upload_file(bucket, prefix, file_name, callback):
        try: 
            params = {
                    'Filename': file_name,
                    'Bucket': bucket, 
                    'Key': f'{prefix}/{file_name}',                                     
                    'Config': TransferConfig(multipart_threshold = MULTIPART_THRESHOLD, 
                                        max_concurrency = MAX_CONCURRENCY,
                                        use_threads = USE_THREADS,
                                        num_download_attempts = NUM_DOWNLOAD_ATTEMPTS)}

            if callable(callback):
                params['Callback'] = callback

            s3.upload_file(**params)

        except botocore.exceptions.ClientError as error:            
            raise Exception(f"Unable to upload file: {file_name}")    
    
    def upload_files(files, pbar):        
        update = getattr(pbar, 'update', None)
        update = update if callable(update) else lambda x: None

        futures = {}            
        with ThreadPoolExecutor() as executor: 
            for path in files:                
                if os.path.isfile(path):                             
                    futures[executor.submit(upload_file, bucket, prefix, path, update)] = path                                                                      
                        
                elif os.path.isdir(path):        
                    for (root,dirs,files) in os.walk(path, topdown=True):
                        for file in files:                                                    
                            file_path = os.path.join(root,file)                                                    
                            futures[executor.submit(upload_file, bucket, prefix, file_path, update)] = file_path                            
                else:
                    raise Exception('File not found or not supported')
            
            pending_files = []
            files_sent = []
            for future in as_completed(futures):
                path = futures[future]
                try: 
                    result = future.result()                    
                except Exception as error:                                
                    pending_files.append(path) 
                    print(error)                   
                else:      
                    files_sent.append(path)   
        
        return pending_files, files_sent     

    if show_progress:
        pbar = tqdm(total=get_total_size(files), unit='B', unit_scale=True, desc='Uploading')
    else:
        pbar = None

    pending_files, all_files_sent = upload_files(files, pbar)

    while len(pending_files)>0:            
        pending_files, files_sent = upload_files(pending_files, pbar)
        all_files_sent.extend(files_sent)

    if callable(getattr(pbar,'close',None)):
        pbar.close()

    return f's3://{bucket}/{prefix}/{all_files_sent[0]}' if len(all_files_sent) == 1 else None

def read_csv(s3_path, compression=None)->pd.core.frame.DataFrame:  
    '''
    Reads a CSV file from a S3 path
    
    Args:
        s3_path (str): S3 path of the file to read
        
    Returns:
        df (pandas.core.frame.DataFrame): pandas dataframe
    '''      
    s3 = session.resource('s3')    
    
    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    obj = s3.Object(bucket, key)
    f = BytesIO(obj.get()['Body'].read())

    pd.read_csv(f, compression='gzip')

    