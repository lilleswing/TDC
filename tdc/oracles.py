import pandas as pd
import numpy as np
import os, sys, json 
import warnings
warnings.filterwarnings("ignore")

# from. evaluator import Evaluator
from .utils import * 
from .metadata import download_oracle_names, oracle_names, molecule_evaluator_name

class Oracle:
	def __init__(self, name):

		name = fuzzy_search(name, oracle_names)
		if name in download_oracle_names:
			self.name = oracle_load(name)
		else:
			self.name = name
		self.evaluator_func = None
		self.assign_evaluator() 

	def assign_evaluator(self):
		'''
		from .chem_utils import eval(self.name)
		self.evaluator_func = eval(self.name)
		'''
		if self.name == 'novelty':
			from .chem_utils import novelty
			self.evaluator_func = novelty  
		elif self.name == 'diversity':
			from .chem_utils import diversity
			self.evaluator_func = diversity 
		elif self.name == 'validity':
			from .chem_utils import validity
			self.evaluator_func = validity 
		elif self.name == 'uniqueness':
			from .chem_utils import uniqueness
			self.evaluator_func = uniqueness 
		elif self.name == 'kl_divergence':
			from .chem_utils import kl_divergence
			self.evaluator_func = kl_divergence
		elif self.name == 'fcd_distance':
			from .chem_utils import fcd_distance
			self.evaluator_func = fcd_distance
		elif self.name == 'logp':
			from .chem_utils import penalized_logp
			self.evaluator_func = penalized_logp 
		elif self.name == 'qed':
			from .chem_utils import qed
			self.evaluator_func = qed  
		elif self.name == 'drd2':
			from .chem_utils import drd2
			self.evaluator_func = drd2 
		elif self.name == 'sa':
			from .chem_utils import SA
			self.evaluator_func = SA 
		elif self.name == 'gsk3b':
			from .chem_utils import gsk3b
			oracle_object = gsk3b
			self.evaluator_func = oracle_object
		elif self.name == 'jnk3':
			from .chem_utils import jnk3
			oracle_object = jnk3()
			self.evaluator_func = oracle_object
		elif self.name == 'celecoxib_rediscovery':
			from .chem_utils import celecoxib_rediscovery
			self.evaluator_func = celecoxib_rediscovery
		elif self.name == 'troglitazone_rediscovery':
			from .chem_utils import troglitazone_rediscovery
			self.evaluator_func = troglitazone_rediscovery
		elif self.name == 'thiothixene_rediscovery':
			from .chem_utils import thiothixene_rediscovery
			self.evaluator_func = thiothixene_rediscovery
		elif self.name == 'aripiprazole_similarity':
			from .chem_utils import aripiprazole_similarity
			self.evaluator_func = aripiprazole_similarity
		elif self.name == 'albuterol_similarity':
			from .chem_utils import albuterol_similarity
			self.evaluator_func = albuterol_similarity
		elif self.name == 'mestranol_similarity':
			from .chem_utils import mestranol_similarity
			self.evaluator_func = mestranol_similarity
		elif self.name == 'median1':
			from .chem_utils import median1
			self.evaluator_func = median1
		elif self.name == 'median2':
			from .chem_utils import median2
			self.evaluator_func = median2
		elif self.name == 'osimertinib_mpo':
			from .chem_utils import osimertinib_mpo
			self.evaluator_func = osimertinib_mpo
		elif self.name == 'fexofenadine_mpo':
			from .chem_utils import fexofenadine_mpo
			self.evaluator_func = fexofenadine_mpo
		elif self.name == 'ranolazine_mpo':
			from .chem_utils import ranolazine_mpo
			self.evaluator_func = ranolazine_mpo
		elif self.name == 'perindopril_mpo':
			from .chem_utils import perindopril_mpo
			self.evaluator_func = perindopril_mpo
		elif self.name == 'amlodipine_mpo':
			from .chem_utils import amlodipine_mpo
			self.evaluator_func = amlodipine_mpo
		elif self.name == 'sitagliptin_mpo':
			from .chem_utils import sitagliptin_mpo
			self.evaluator_func = sitagliptin_mpo
		elif self.name == 'zaleplon_mpo':
			from .chem_utils import zaleplon_mpo
			self.evaluator_func = zaleplon_mpo
		elif self.name == 'valsartan_smarts':
			from .chem_utils import valsartan_smarts
			self.evaluator_func = valsartan_smarts
		elif self.name == 'deco_hop':
			from .chem_utils import deco_hop
			self.evaluator_func = deco_hop
		elif self.name == 'scaffold_hop':
			from .chem_utils import scaffold_hop
			self.evaluator_func = scaffold_hop
		elif self.name == 'isomers_c7h8n2o2':
			from .chem_utils import isomers_c7h8n2o2
			self.evaluator_func = isomers_c7h8n2o2
		elif self.name == 'isomers_c9h10n2o2pf2cl':
			from .chem_utils import isomers_c9h10n2o2pf2cl
			self.evaluator_func = isomers_c9h10n2o2pf2cl  
		elif self.name == 'askcos':  		#### synthetic analysis 
			from .chem_utils import askcos
			self.evaluator_func = askcos
		elif self.name == 'ibm_rxn':
			from .chem_utils import ibm_rxn
			self.evaluator_func = ibm_rxn
		else:
			return 

	# ### old version without args and kwargs 
	# def __call__(self, smiles, temp = None):
	# 	if temp is None:
	# 		if type(smiles)==list:
	# 			if self.name in molecule_evaluator_name: 
	# 				#### evaluator for distribution learning, e.g., diversity, validity
	# 				#### the input of __call__ is list of smiles
	# 				return self.evaluator_func(smiles) 
	# 			else:
	# 				#### evaluator for single molecule, 
	# 				#### the input of __call__ is a single smiles OR list of smiles
	# 				return list(map(self.evaluator_func, smiles))
	# 		else: ### type(smiles)==str:
	# 			return self.evaluator_func(smiles)
	# 	else:
	# 		# novelty
	# 		return self.evaluator_func(smiles, temp)


	def __call__(self, *args, **kwargs):
		smiles_lst = args[0]
		if type(smiles_lst) == list:
			if self.name in molecule_evaluator_name:
				#### evaluator for distribution learning, e.g., diversity, validity
				#### the input of __call__ is list of smiles
				return self.evaluator_func(*args, **kwargs)
			else:
				#### evaluator for single molecule, 
				#### the input of __call__ is a single smiles OR list of smiles
				results_lst = []
				for smiles in smiles_lst:
					results_lst.append(self.evaluator_func(smiles, *(args[1:]), **kwargs))
				return results_lst
		else:	
			## a single smiles
			return self.evaluator_func(*args, **kwargs)




