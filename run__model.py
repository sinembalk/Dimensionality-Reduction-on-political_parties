
import sys
sys.path.append("..")
from config import Params
from model.model_generator import *
from model.model_generator import Model

model= Model(Params.country_out_scope, Params.conceptual_cols, Params.scale_7)
data= model.data_preperation()
feature_dict= model.get_concept_dimensions(data)
data_treated= model.null_treatment(data)
weight_dict = model.two_d_visual(data_treated, feature_dict)
sample_data=  model.feature_value_wieghts( data_treated, feature_dict, weight_dict )
