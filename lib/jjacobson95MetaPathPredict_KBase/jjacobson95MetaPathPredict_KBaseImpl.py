# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import logging
import os
from pprint import pformat
import subprocess 
from Bio import SeqIO
import sys
import zipfile
import uuid
from datetime import datetime
import csv
import gzip
import shutil

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as workspaceService
# from installed_clients.cb_annotation_ontology_apiClient import cb_annotation_ontology_api

#END_HEADER


class MetaPathPredict:
    '''
    Module Name:
    SnekmerLearnApply

    Module Description:
    A KBase module: SnekmerLearnApply
This sample module contains one small method that filters contigs.
This will have to be changed soon.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/jjacobson95/KbaseSnekmerLA.git"
    GIT_COMMIT_HASH = "1421a376a1e6a3f23c863257f976721e20b6acce"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        
        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.workspaceURL = config['workspace-url']
        self.wsClient = workspaceService(self.workspaceURL)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_MetaPathPredict(self, ctx, params):
        """
        Executes the Snekmer Apply function, which is designed to annotate biological sequences with ontology terms (TIGRFams, Pfam, PANTHER)
        based on their k-mer profiles. The method supports processing both protein and genome inputs. It performs several key operations:
        
        1. Validates input parameters to ensure the presence of either protein or genome inputs.
        2. Dynamically constructs object references based on the input type and fetches corresponding sequence data from a workspace.
        3. Writes the fetched sequences to FASTA files, which are then used as input for the Snekmer application.
        4. Decompresses necessary reference files for Snekmer analysis based on the specified family (TIGRFams, Pfam, PANTHER).
        5. Executes the Snekmer application to generate k-mer based annotations for the input sequences.
        6. Parses the Snekmer output to annotate the original sequence objects with the new ontology terms.
        7. Packages the Snekmer output files into a ZIP archive for easy download.
        8. Generates a detailed report through the KBaseReport service, summarizing the annotation results and providing links to the output files.
        
        Parameters:
            ctx (dict): A context object containing information about the runtime environment, including user authentication.
            params (dict): A dictionary containing method input parameters. Expected keys include:
                - workspace_name: Name of the workspace where the output will be saved.
                - protein_input or genome_input: Lists of object references to protein or genome data.
                - input_type: A string indicating the type of input ('protein' or 'genome').
                - family: The ontology family to use for annotation (e.g., 'TIGRFams', 'Pfam', 'PANTHER').
        
        Returns:
            dict: A dictionary with keys 'report_name' and 'report_ref', referring to the name and reference of the generated report.
        
        Raises:
            ValueError: If neither protein_input nor genome_input are provided in the params, or if other expected parameters are missing.
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_MetaPathPredict

        logging.info('Starting MetaPathPredict. Params=' + pformat(params))
        logging.info('Validating parameters.')

        # cmd_string = "MetaPathPredict --input data/blastKoala_annotations.tsv.gz --annotation-format koala --output MetaPath_test_output_file"
        cmd_string = "MetaPathPredict --help"
        cmd_process = subprocess.Popen(cmd_string, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, cwd=os.getcwd(),
                                    shell=True)
        
        output, errors = cmd_process.communicate()
        logging.info('return code: ' + str(cmd_process.returncode))
        logging.info("="*80)
        logging.info("output: " + str(output) + '\n')
        logging.info("errors: " + str(errors) + '\n')
        
        
        # check inputs
        workspace_name = params['workspace_name']
        run_type = []
        text_message = "Test 1"

        # Prepare the Report Parameters
        report_params = {
            'message': text_message,
            'workspace_name': workspace_name
        }
        logging.info(report_params)

        # Create the report
        report_client = KBaseReport(self.callback_url)
        report_info = report_client.create_extended_report(report_params)

        # Prepare output
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }


        #END run_MetaPathPredict

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_MetaPathPredict return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
            

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]