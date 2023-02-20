import re
import os
import mimetypes
from typing import Any, Dict, List, Union, Callable, Optional
from docassemble.base.util import (
    log,
    DADict,
    DAList,
    DAObject,
    DAFile,
    DAFileCollection,
    DAFileList,
    defined,
    pdf_concatenate,
    zip_file,
    DAOrderedDict,
    background_action,
    action_button_html,
    include_docx_template,
    user_logged_in,
    user_info,
    send_email,
    docx_concatenate,
    get_config,
    space_to_underscore,
    DAStaticFile,
    alpha,
    showifdef,
)

__all__ = [
  'DAScore'
]

from .lookup_values import get_score
from .custom_dtype import LookupVariable

class DAScore(DAObject):
  
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

        if not hasattr(self, 'name'):
          self.name = DAObject()

        if not hasattr(self, 'entry_type'):
          self.entry_type = 'score'

        self.datatype = 'LookupVariable'
        
    def get_score(self):
      if not hasattr(self, 'score'):
        return 'N/A'
      return self.score
    
    def get_percentile(self):
      if hasattr(self, 'score_to_qualifier'):
        self.percentile = 'N/A'
        return self.percentile
        
      if not hasattr(self, 'score'):
        return self.percentile
      
      self.percentile = get_score(value=self.score, tab_name=self.type)
      return self.percentile
    
    def get_qualifier(self):
      if hasattr(self, 'score_to_qualifier'):
        lookup_value = self.score
        lookup_column = 'score'
        tab_name = self.type
      elif self.entry_type == 'percentile':
        lookup_value = self.percentile
        lookup_column = 'percentile'
        tab_name = self.type
      else:
        lookup_value = self.percentile
        lookup_column = 'percent'
        tab_name = 'classification'
        
      self.qualifier = get_score(
        value=lookup_value, 
        tab_name=tab_name, 
        lookup_variable=lookup_column, 
        return_variable='classification'
       )
      return self.qualifier
    
    def validate_input(self):
      try:
        self.get_percentile()
        self.get_qualifier()
        return True
      except:
        return False
        
   #  self.percentile = get_score(value=self.score, tab_name=get_tab(self.name))
   #   self.qual = get_score(
   #     value=self.percentile, 
   #     tab_name='classification', 
   #     lookup_variable='percent', 
   #     return_variable='classification'
   #    )
       
     