# -*- coding: utf-8 -*-
"""
@authors: Ethan Sean Chan, Andrew Philip Freiburger
"""
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium import webdriver

from scipy.constants import minute, hour, milli, nano, micro
from pprint import pprint
from chardet import detect
from glob import glob
from math import floor
import datetime
import pandas
import numpy
import warnings, json, time, re, os


def isnumber(string):
    try:
        num = float(string)
        return num
    except:
        try:
            num = int(string)
            return num
        except:
            return False
        
    
def average(num_1, num_2 = None):
    if isnumber(num_1): 
        if isnumber(num_2):
            numbers = [isnumber(num_1), isnumber(num_2)]
            return sum(numbers) / len(numbers)
        else:
            return num_1
    elif type(num_1) is list:
        summation = total = 0
        for num in num_1:
            if num is not None:
                summation += num
                total += 1
        if total > 0:
            return summation/total
        return None # raise ValueError(f'The arguments {num_1} & {num_2} must be numbers or a list of numbers')
    elif isnumber(num_2):
        return num_2
    else:
        return None # raise ValueError(f'The arguments {num_1} & {num_2} must be numbers or a list of numbers')
    
    
    

# encoding the final JSON
class NumpyEncoder(json.JSONEncoder):     # sourced from https://github.com/hmallen/numpyencoder
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
                            numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
                            numpy.uint16, numpy.uint32, numpy.uint64)):

            return int(obj)

        elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32, numpy.float64)):
            return float(obj)

        elif isinstance(obj, (numpy.complex_, numpy.complex64, numpy.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (numpy.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (numpy.bool_)):
            return bool(obj)

        elif isinstance(obj, (numpy.void)): 
            return None

        return json.JSONEncoder.default(self, obj)
    
    
# allows case insensitive dictionary searches
class CaseInsensitiveDict(dict):        # sourced from https://stackoverflow.com/questions/2082152/case-insensitive-dictionary
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()
        
    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
    
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
        
    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
    
    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
    
    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
    
    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
    
    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
    
    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
    
    def update(self, E=None, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))
        
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


class SABIO_scraping():
#     __slots__ = (str(x) for x in [progress_file_prefix, xls_download_prefix, is_scraped_prefix, is_scraped_entryids_prefix, sel_raw_data, processed_csv, entry_json, scraped_model, bigg_model_name_suffix, output_directory, progress_path, raw_data, is_scraped, is_scraped_entryids_path, xls_csv_file_path, entryids_json_file_path, model_kinetics_path, bigg_model, step_number, cwd])
    
    def __init__(self,
                 bigg_model_path: str,        # the JSON version of the BiGG model
                 bigg_model_name: str = None,  # the name of the BiGG model
                 export_model_content: bool = False,
                 verbose: bool = False,
                 printing: bool = True
                 ):
        self.export_model_content = export_model_content 
        self.verbose = verbose
        self.printing = printing
        self.step_number = 1
        self.count = 0
        self.paths = {}
        
        # initial parameters and variables
        self.parameters = {}
        self.parameters['general_delay'] = 2
        
        self.variables = {}
        self.variables['is_scraped'] = {}
        self.variables['is_scraped_entryids'] = {}
        self.variables['entryids'] = {}
        
        # load BiGG dictionary content 
        self.paths['bigg_model_path'] = bigg_model_path
        self.paths['root_path'] = os.path.dirname(__file__)
        self.bigg_to_sabio_metabolites = json.load(open(os.path.join(self.paths['root_path'],'BiGG_metabolites, parsed.json')))
        self.sabio_to_bigg_metabolites = json.load(open(os.path.join(self.paths['root_path'],'BiGG_metabolite_names, parsed.json')))
        self.sabio_insensitive = CaseInsensitiveDict(self.sabio_to_bigg_metabolites)
        self.bigg_insensitive = CaseInsensitiveDict(self.bigg_to_sabio_metabolites)
        self.bigg_reactions = json.load(open(os.path.join(self.paths['root_path'],'BiGG_reactions, parsed.json')))
        
        # load the BiGG model content
        if os.path.exists(self.paths['bigg_model_path']):
            self.model = json.load(open(self.paths['bigg_model_path']))
        else:
            raise ValueError('The BiGG model file does not exist')
            
        self.bigg_model_name = bigg_model_name 
        if bigg_model_name is None:
            self.bigg_model_name = re.search("([\w+\.?\s?]+)(?=\.json)", self.paths['bigg_model_path']).group()
            
        # define folder paths
        self.paths['cwd'] = os.path.dirname(os.path.realpath(self.paths['bigg_model_path']))  
        self.paths['output_directory'] = os.path.join(self.paths['cwd'],f"scraping-{self.bigg_model_name}")    
        self.paths['raw_data'] = os.path.join(self.paths['output_directory'], 'downloaded')    
        if not os.path.isdir(self.paths['output_directory']):        
            os.mkdir(self.paths['output_directory'])
        if not os.path.isdir(self.paths['raw_data']):
            os.mkdir(self.paths['raw_data'])
        
        # define file paths
        self.paths['progress_path'] = os.path.join(self.paths['output_directory'], "current_progress.txt")
        self.paths['model_kinetics_path'] = os.path.join(self.paths['output_directory'], "model_kinetics.json")
        self.paths['concatenated_data'] = os.path.join(self.paths['raw_data'], "concatenated_data.csv")
        self.paths['is_scraped'] = os.path.join(self.paths['raw_data'], "is_scraped.json")
        self.paths['is_scraped_entryids'] = os.path.join(self.paths['raw_data'], "is_scraped_entryids.json")
        self.paths['entryids_path'] = os.path.join(self.paths['raw_data'], "entryids.json")
        self.paths['model_contents'] = os.path.join(self.paths['raw_data'], f'processed_{self.bigg_model_name}_model.json')
        
        # parse the model contents 
        self._progress_update(self.step_number)
        self.model_contents = {}        
        for enzyme in self.model['reactions']:
            annotations = enzyme['annotation']
            enzyme_id = enzyme['id']
            enzyme_name = enzyme['name']
            
            og_reaction_string = self.bigg_reactions[enzyme_id]['reaction_string']
            reaction_string, sabio_chemicals, bigg_compounds = self._split_reaction(og_reaction_string)
            self.model_contents[enzyme_name] = {
                'reaction': {
                    'original': og_reaction_string,
                    'substituted': reaction_string,
                },
                'bigg_chemicals': bigg_compounds,
                'sabio_chemicals': sabio_chemicals,
                'annotations': annotations
            }
            
            
    # ==================== HELPER FUNCTIONS =======================

    #Clicks a HTML element with selenium by id
    def _click_element_id(self,n_id):
        element = self.driver.find_element_by_id(n_id)
        element.click()
        time.sleep(self.parameters['general_delay'])
        
    def _wait_for_id(self,n_id):
        while True:
            try:
                element = self.driver.find_element_by_id(n_id)   #!!! what is the purpose of this catch?
                break
            except:
                time.sleep(self.parameters['general_delay'])
        

    #Selects a choice from a HTML dropdown element with selenium by id
    def _select_dropdown_id(self,n_id, n_choice):
        element = Select(self.driver.find_element_by_id(n_id))
        element.select_by_visible_text(n_choice)
        time.sleep(self.parameters['general_delay'])
        
        
    def _progress_update(self, step):
        if not re.search('[0-5]', str(step)):
            print(f'--> ERROR: The {step} step is not acceptable.')
        f = open(self.paths['progress_path'], "w")
        f.write(str(step))
        f.close()


    def _previous_scrape(self):
        if os.path.exists(self.paths['progress_path']):
            with open(self.paths['progress_path'], "r") as f:
                self.step_number = int(f.read(1))
                if not re.search('[1-5]',str(self.step_number)):
                    raise ImportError(f"Progress file malformed. Create a < current_progress.txt > file with a < 1-5 > digit to signify the current scrapping progress.")
                print(f'Continuing Step {self.step_number}')

        # define file paths and import content from an interupted scrapping       
        if os.path.exists(self.paths['is_scraped']):
            with open(self.paths['is_scraped'], 'r') as f:
                self.variables['is_scraped'] = json.load(f)

        if os.path.exists(self.paths['is_scraped_entryids']):
            with open(self.paths['is_scraped_entryids'], 'r') as f:
                try:
                    self.variables['is_scraped_entryids'] = json.load(f)
                except:
                    raise ImportError('The < entryids.json > file is corrupted or empty.')
        
        if os.path.exists(self.paths['entryids_path']):
            with open(self.paths['entryids_path'], 'r') as f:
                try:
                    self.variables['entryids'] = json.load(f)
                except:
                    raise ImportError('The < entryids.json > file is corrupted or empty.')
                
    def _open_driver(self,):
        self.options = Options()
        self.options.headless = True
        self.fp = webdriver.FirefoxProfile(os.path.join(self.paths['root_path'],"l2pnahxq.scraper"))
        self.fp.set_preference("browser.download.folderList", 2)
        self.fp.set_preference("browser.download.manager.showWhenStarting", False)
        self.fp.set_preference("browser.download.dir", self.paths["raw_data"])
        self.fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        self.driver = webdriver.Firefox(firefox_profile=self.fp, executable_path=os.path.join(self.paths['root_path'],"geckodriver.exe"))
        self.driver.get("http://sabiork.h-its.org/newSearch/index")
            
            
    def complete(self,):
        self._previous_scrape()
        while True:
            if self.step_number == 1:
                self.scrape_bigg_xls()
            elif self.step_number == 2:
                self.to_fba()
                break
        print("Execution complete.")
        # os.remove(self.paths['progress_path'])
        
    """
    ---------------------------------------------------------------------------------------------------------
        STEP 1: SCRAPE SABIO WEBSITE BY DOWNLOAD XLS FOR GIVEN REACTIONS IN BIGG MODEL
    ---------------------------------------------------------------------------------------------------------    
    """

    def _scrape_csv(self,reaction_identifier, search_option):
        quantity_of_xls_files = len([file for file in glob(os.path.join(self.paths['raw_data'], '*.xls'))])
        
        self.driver.get("http://sabiork.h-its.org/newSearch/index")
       
        time.sleep(self.parameters['general_delay'])

        self._click_element_id("resetbtn")        
        
        time.sleep(self.parameters['general_delay']*2)
        
        self._click_element_id("option")
        self._select_dropdown_id("searchterms", search_option)
        text_area = self.driver.find_element_by_id("searchtermField")
        text_area.send_keys(reaction_identifier)  
        
        time.sleep(self.parameters['general_delay']) 
        
        self._click_element_id("addsearch")
        
        time.sleep(self.parameters['general_delay'])

        result_num = ""
        try: 
            result_num_ele = self.driver.find_element_by_id("numberofKinLaw")
            for char in result_num_ele.text:
                if re.search('[0-9]', char):
                    result_num += char
            result_num = int(result_num)
        except:
            #self.driver.close()
            self.driver.get("http://sabiork.h-its.org/newSearch/index")
            return False

        time.sleep(self.parameters['general_delay'])

        self._select_dropdown_id("max", "100")
        element = Select(self.driver.find_element_by_id("max"))
        element.select_by_visible_text("100")

        time.sleep(self.parameters['general_delay'])

        if result_num > 0 and result_num <= 100:
            self._click_element_id("allCheckbox")
            time.sleep(self.parameters['general_delay'])
        elif result_num > 100:
            loops = floor(result_num/100)
            if result_num % 100 == 0:
                loops -= 1
            
            self._click_element_id("allCheckbox")
            for i in range(loops):
                element = self.driver.find_element_by_xpath("//*[@class = 'nextLink']")
                element.click()
                time.sleep(self.parameters['general_delay'])
                self._click_element_id("allCheckbox")
                time.sleep(self.parameters['general_delay'])
        else:
            #self.driver.close()
            self.driver.get("http://sabiork.h-its.org/newSearch/index")
            return False

        self.driver.get("http://sabiork.h-its.org/newSearch/spreadsheetExport")
        
        time.sleep(self.parameters['general_delay']*7.5)
        
        element = self.driver.find_element_by_xpath("//*[text()[contains(., 'Add all')]]")
        element.click()
        
        time.sleep(self.parameters['general_delay']*2.5)
        
        self._click_element_id("excelExport")
        
        time.sleep(self.parameters['general_delay']*2.5)
        
        new_quantity_of_xls_files = len([file for file in glob(os.path.join(self.paths['raw_data'], '*.xls'))])
        loop = 0
        while new_quantity_of_xls_files != quantity_of_xls_files+1:
            if loop == 0:
                print(f'The search result for {reaction_identifier} has not downloaded. We will wait until it downloads.')
            new_quantity_of_xls_files = len([file for file in glob(os.path.join(self.paths['raw_data'], '*.xls'))])
            time.sleep(self.parameters['general_delay'])
            loop += 1
        if loop > 0:
            time.sleep(self.parameters['general_delay']*30)
            if self.verbose:
                string = 'The search result for {} downloaded after {} seconds.'.format(reaction_identifier, self.parameters['general_delay']*loop)
                print(string)

        return True
    
#    def _expand_shadow_element(self, element):      
#        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
#        return shadow_root
    
    def _split_reaction(self, 
                        reaction_string, # the sabio or bigg reaction string
                        sabio = False   # specifies how the reaction string will be split
                        ):
        def __parse_stoich(met):
            stoich = ''
            ch_number = 0
            denom = False
            numerator = denominator = 0
            while re.search('[0-9\./]', met[ch_number]): 
                stoich += met[ch_number]
                if met[ch_number] == '/':
                    numerator = stoich
                    denom = True
                if denom:
                    denominator += met[ch_number]
                ch_number += 1
                
            if denom:
                stoich = f'{numerator}/{denominator}'
            return stoich
        
        def __met_parsing(met):
    #         print(met)
            met = met.strip()
            met = re.sub('_\w$', '', met)
            if re.search('(\d\s\w|\d\.\d\s|\d/\d\s)', met):
                coefficient = __parse_stoich(met)
                coefficient = '{} '.format(coefficient)
            else:
                coefficient = ''
            met = re.sub(coefficient, '', met)
    #         print(met, coefficient)
            return met, coefficient   
    
        def __reformat_met_name(met_name, sabio = False):
            met_name = re.sub(' - ', '-', met_name)
#            if not sabio:
#                met_name = re.sub(' ', '_', met_name)
            return met_name
        
        def __name_refinement(met_name):
            if met_name == 'NAD\+':
                met_name = 'Nicotinamide adenine dinucleotide'
            elif met_name == 'NADH':
                met_name = 'Nicotinamide adenine dinucleotide - reduced'
                
            return met_name
        
        def __check_existence(met, coefficient, bigg_chemicals, sabio = False):
            original_length = len(bigg_chemicals)
            if met in self.sabio_insensitive:
                if 'bigg_name' in self.sabio_insensitive.get(met):
                    bigg_chemicals.append(coefficient + __reformat_met_name(self.sabio_insensitive.get(met)['bigg_name']))
                else:
                    bigg_chemicals.append(coefficient + __reformat_met_name(met))
            elif met in self.bigg_insensitive:
                if 'bigg_name' in self.bigg_insensitive.get(met):
                    bigg_chemicals.append(coefficient + __reformat_met_name(self.bigg_insensitive.get(met)['bigg_name']))
                else:
                    bigg_chemicals.append(coefficient + __reformat_met_name(met))
            else:
                print(f'-->ERROR: The {met} metabolite in is not recognized by BiGG.')        
                
            final_length = len(bigg_chemicals)
            if original_length == final_length:
                return bigg_chemicals, False
            else:
                return bigg_chemicals, True
        
        def parsing_chemical_list(chemical_list, sabio):            
            bigg_chemicals = []
            sabio_chemicals = []
            for met in chemical_list:
                if not re.search('[A-Za-z]', met):
                    continue
                met, coefficient = __met_parsing(met)
                met = __name_refinement(met)
                
                # assign the proper chemical names
                if not sabio:
                    sabio_chemicals.append(coefficient + __reformat_met_name(self.bigg_to_sabio_metabolites[met]['name'], True))     
                else:
                    sabio_chemicals.append(coefficient + __reformat_met_name(met, True))    
                match = __check_existence(met, coefficient, bigg_chemicals, True)
                if not match:
                    if re.search('D-', met):
                        met = re.sub('D-', '', met)
                        bigg_chemicals, match = __check_existence(met, coefficient, bigg_chemicals, sabio)
                    elif not re.search('D-', met) and not match:
                        met = 'D-' + met
                        bigg_chemicals, match = __check_existence(met, coefficient, bigg_chemicals, sabio)
#                        elif not re.search('D-', met) and not match:
#                            met = 'D-' + met
            
            return bigg_chemicals, sabio_chemicals
        
            
        # parse the reactants and products for the specified reaction string
        if not sabio:
            reaction_split = reaction_string.split(' <-> ')
        else:
            reaction_split = reaction_string.split(' = ')
            
        reactants_list = reaction_split[0].split(' + ')
        products_list = reaction_split[1].split(' + ')
        
        # parse the reactants and products
        bigg_reactants, sabio_reactants = parsing_chemical_list(reactants_list, sabio)
        bigg_products, sabio_products = parsing_chemical_list(products_list, sabio)
        
        # assemble the chemicals list and reaction string
        bigg_compounds = bigg_reactants + bigg_products
        sabio_chemicals = sabio_reactants + sabio_products
        reactant_string = ' + '.join(bigg_reactants)
        product_string = ' + '.join(bigg_products)
        reaction_string = ' <-> '.join([reactant_string, product_string])
#        if sabio:
#            reaction_string = ' = '.join([reactant_string, product_string])        
        
        return reaction_string, sabio_chemicals, bigg_compounds
    
    def _refine_scraped_file(self, enzyme_name, ID):     
        # open the most recent file
        xls_files = glob(os.path.join(self.paths['raw_data'], '*.xls'))
        most_recent = max(xls_files, key = os.path.getctime)
        with open(most_recent) as xls:
            df = pandas.read_excel(xls.name)
            
        # apply the enzyme name information with the BiGG name, and save as the 
        df['Enzymename'] = [enzyme_name for name in range(len(df['Enzymename']))]
        sabio_ids = df["SabioReactionID"].unique().tolist()
        
        # export the XLS with a unique name
        count = -1
        file_extension = ''
        df_path = os.path.join(self.paths['raw_data'], enzyme_name+'.csv')
        while os.path.exists(df_path):
            count += 1
            if re.search('(\.[a-zA-Z]+$)', df_path):
                file_extension = re.search('(\.[a-zA-Z]+$)', df_path).group()
                df_path = re.sub(file_extension, '', df_path)
            if not re.search('(-[0-9]+$)', df_path):
                df_path += f'-{count}'   
            else:
                df_path = re.sub('([0-9]+)$', str(count), df_path)
            df_path += file_extension
        
        os.remove(most_recent)
        dir = os.path.dirname(df_path)
        if not os.path.exists(dir):
            print(f'missing directory {dir} has been created.')
            os.mkdir(dir)
        df.to_csv(df_path)
        
        # store the matched content for future access during parsing
        self.id_bigg_matches[enzyme_name] = sabio_ids
        self.id_bigg_matches[ID] = enzyme_name
        
    def _glob_csv(self,):
#         scraped_sans_parentheses_enzymes = glob('./{}/*.xls'.format(self.paths['raw_data']))
        total_dataframes = []
        
        original_csvs = glob(os.path.join(self.paths['raw_data'], '*.csv')) 
        for path in original_csvs:
            size = os.path.getsize(path)
            if size > 0:
                with open(path, 'rb') as file:
                    encoding = detect(file.read())['encoding']
                    if encoding is None:
                        encoding = 'utf-8'
            dfn = pandas.read_csv(path)
            total_dataframes.append(dfn)
            
        remaining_xls = glob(os.path.join(self.paths['raw_data'], '*.xls')) 
        for path in remaining_xls:
            size = os.path.getsize(path)
            if size > 0:
                with open(path, 'rb') as file:
                    encoding = detect(file.read())['encoding']
                    if encoding is None:
                        encoding = 'utf-8'
            dfn = pandas.read_excel(path)
            total_dataframes.append(dfn)

        # All scraped dataframes are combined and duplicate rows are removed
        combined_df = pandas.DataFrame()
        combined_df = pandas.concat(total_dataframes)
        combined_df = combined_df.fillna('')
        combined_df = combined_df.drop_duplicates()

        # remove the individual dataframes
        total_files = original_csvs+remaining_xls
        for file in total_files:
            os.remove(file)
        
        # export the concatenated dataframe
        combined_df.to_csv(self.paths['concatenated_data'])
        print(f'SABIO data has been concatenated.')
        

    def _scrape_entry_id(self,entry_id):
        entry_id = str(entry_id)  
        self.driver.get("http://sabiork.h-its.org/newSearch/index")
        
        time.sleep(self.parameters['general_delay'])
        
        self._wait_for_id("resetbtn")
        
        time.sleep(self.parameters['general_delay'])
        
        self._click_element_id("resetbtn")
        
        time.sleep(self.parameters['general_delay']*2)

        self._click_element_id("option")
        self._select_dropdown_id("searchterms", "EntryID")
        text_area = self.driver.find_element_by_id("searchtermField")
        
        time.sleep(self.parameters['general_delay'])
        
        text_area.send_keys(entry_id)
        
        time.sleep(self.parameters['general_delay'])
        
        self._click_element_id("addsearch")
        
        # wait for the information expansion to open 
        for delay in range(60):
            try:
                self._click_element_id(entry_id + "img")              
                break
            except:
                if delay == 59:
                    return {'content':None}
                time.sleep(self.parameters['general_delay'])
        
        time.sleep(self.parameters['general_delay'])
        
        # wait for the table to load
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[@name='iframe_" + entry_id + "']"))
        for delay in range(60):
            try:
                element = self.driver.find_element_by_xpath("//table")                
                break
            except:
                if delay == 59:
                    return {'content':None}
                time.sleep(self.parameters['general_delay'])

        element = self.driver.find_element_by_xpath("//table")
        html_source = element.get_attribute('innerHTML')
        table_df = pandas.read_html(html_source)
        reaction_parameters_df = pandas.DataFrame()
        counter = 0
        parameters_json = {}
        for df in table_df:
            try:
                if df[0][0] == "Parameter":
                    reaction_parameters_df = table_df[counter]
            except:
                self.driver.get("http://sabiork.h-its.org/newSearch/index")
                return parameters_json
            counter += 1
            
        for row in range(2, len(reaction_parameters_df[0])):
            parameter_name = str(reaction_parameters_df[0][row])
            inner_parameters_json = {}
            for col in range(1, len(reaction_parameters_df.columns)):
                parameter_type = str(reaction_parameters_df[col][1])
                inner_parameters_json[parameter_type] = reaction_parameters_df[col][row]

            parameters_json[parameter_name] = inner_parameters_json
        return parameters_json

    def _scrape_entryids(self,):
        self._open_driver()
        self.sabio_df = pandas.read_csv(self.paths['concatenated_data'])
        self._previous_scrape()
        entryids = self.sabio_df["EntryID"].unique().tolist()
        remaining_entryids = set(entryids) - set(self.variables['is_scraped_entryids'])
        
        # estimate the time to scrape the the entryids
        seconds_per_enzyme = 1*minute
        scraping_time = seconds_per_enzyme * len(remaining_entryids)
        estimated_completion = datetime.datetime.now() + datetime.timedelta(seconds = scraping_time)          # approximately 1 minute per enzyme for Step 1
        print(f'Estimated completion of scraping the XLS data for {self.bigg_model_name}: {estimated_completion}, in {scraping_time/hour} hours')
        
        for entryid in remaining_entryids:
            entryid = str(entryid)
            # only entries that possess calculable units will be processed and accepted
            self.variables['is_scraped_entryids'][entryid] = "erroneous"
            parameters = self._scrape_entry_id(entryid)
            if parameters is not None:
                for param in parameters:
                    if not 'unit' in parameters[param]:
                        self.variables['is_scraped_entryids'][entryid] = "missing_unit"
                    elif parameters[param]['unit'] == '-':
                        self.variables['is_scraped_entryids'][entryid] = "missing_unit"
                    elif parameters[param]['start val.'] == '-' and parameters[param]['end val.'] == '-':
                        self.variables['is_scraped_entryids'][entryid] = "missing_values"   
                    else:
                        self.variables['is_scraped_entryids'][entryid] = "acceptable"
                    
            if self.variables['is_scraped_entryids'][entryid] == 'acceptable':
                self.variables['entryids'][entryid] = parameters
                                
                with open(self.paths["is_scraped_entryids"], 'w') as outfile:
                    json.dump(self.variables['is_scraped_entryids'], outfile, indent = 4)   
                    outfile.close()
                with open(self.paths["entryids_path"], 'w') as f:
                    json.dump(self.variables['entryids'], f, indent = 4)        
                    f.close()    
            else:
                if self.verbose:
                    print(entryid, self.variables['is_scraped_entryids'][entryid])
                    pprint(parameters)
                    
            print(f'\rScraped entryID {entryids.index(int(entryid))}/{len(entryids)}\t{datetime.datetime.now()}', end='')
        
        # update the step counter
        print(f'The parameter specifications for each entryid have been scraped.')
        

    def scrape_bigg_xls(self,):        
        self._open_driver()
        # estimate the time to scrape the XLS files
        minutes_per_enzyme = 0.016*minute
        scraping_time = minutes_per_enzyme * len(self.model['reactions'])
        estimated_completion = datetime.datetime.now() + datetime.timedelta(seconds = scraping_time)     
        print(f'Estimated completion of scraping the XLS data for {self.bigg_model_name}: {estimated_completion}, in {scraping_time/hour} hours')
        
        # scrape SABIO data based upon various search parameters
        self.count = len(self.variables["is_scraped"])
        annotation_search_pairs = {
                "sabiork":"SabioReactionID", 
                "metanetx.reaction":"MetaNetXReactionID",
                "ec-code":"ECNumber", 
                "kegg.reaction":"KeggReactionID",
                "rhea":"RheaReactionID"
                }
        self.bigg_sabio_enzymes = {}
        self.id_bigg_matches = {}
        for enzyme in self.model['reactions']:            
            # search SABIO for reaction kinetics
#            enzyme_name = enzyme['name'].replace("\"", "")
            enzyme_name = enzyme['name']
            if not enzyme_name in self.variables['is_scraped']:
                self.variables['is_scraped'][enzyme_name] = {}
                annotation_search_pairs.update({
                        enzyme_name:"Enzymename"
                        })
                for database in annotation_search_pairs:
                    if database in self.model_contents[enzyme_name]['annotations']:
                        for ID in self.model_contents[enzyme_name]['annotations'][database]:
                            self.variables['is_scraped'][enzyme_name][ID] = False
                            scraped = self._scrape_csv(ID, annotation_search_pairs[database])
                            if scraped:
                                self.variables['is_scraped'][enzyme_name][ID] = True
                                try:                               
                                    self._refine_scraped_file(enzyme_name, ID)
                                except:
                                    warnings.warn(f'The downloaded XLS file for {enzyme_name} and the {ID} ID could not be opened.')
#                                self._change_enzyme_name(enzyme_name)
                    
                self.count += 1
                print(f"\rCompleted reaction: {self.count+1}/{len(self.model['reactions'])}\t{datetime.datetime.now()}", end='')
            else:
                print(f'< {enzyme_name} > was either already scraped, or is duplicated in the model.')

            # tracks scraping progress
            with open(self.paths['is_scraped'], 'w') as outfile:
                json.dump(self.variables['is_scraped'], outfile, indent = 4)   
                outfile.close()
                
        if self.export_model_content:
            with open(self.paths['model_contents'], 'w') as out:
                json.dump(self.model_contents, out, indent = 3)
                
        # process the data
        print(f'SABIO data has been downloaded.')
        self._glob_csv()
        self._scrape_entryids()
        self.step_number = 2
        self._progress_update(self.step_number)

    """
    --------------------------------------------------------------------
        STEP 2: COMBINE XLS AND ENTRYID DATA INTO A dFBA INPUT JSON FILE
    --------------------------------------------------------------------
    """   
    
    def _determine_parameter_value(self, unit, original_value):
        # parse the unit
        numerator = ''
        denominator = ''
        term = ''
        skips = 0
        next_denominator = False
        for index in range(len(unit)):
            if skips > 0:
                skips -= 1 
                continue
                
            ch = unit[index]
            term += ch
            # parse the unit characters
            if index == len(unit)-1:
                if next_denominator:
                    denominator += term
                else:
                    numerator += term
                term = ''
            elif index+1 == len(unit)-1:
                if next_denominator:
                    denominator += term
                else:
                    numerator += term
                term = ''
            elif unit[index+1] == '^':
                if unit[index+2:index+6] == '(-1)':
                    denominator += term 
                    skips = 5
                    term = ''
                else:
                    print(unit, term)
            elif unit[index+1] == '/':
                numerator += term
                term = ''
                skips += 1
                next_denominator = True
                
        if term != '':
            print(unit, term)
        unit_dic = {
            'numerator':numerator,
            'denominator': denominator
        }
        
        # determine the mathematically equivalent value in base units
#        print('original_value', original_value)
        if original_value is None or original_value in ['None']:
            return original_value, unit_dic
        value = float(original_value)
        for group in unit_dic:
            term = unit_dic[group]
            if re.search('min', unit_dic[group]):
                if group == 'numerator':
                    value *= minute
                    unit_dic[group] = re.sub('min', 's', unit_dic[group])
                else:
                    value /= minute  
                    unit_dic[group] = re.sub('min', 's', unit_dic[group])
            if re.search('mg|mM|mmol', unit_dic[group]):
                if group == 'numerator':
                    value *= milli
                    unit_dic[group] = re.sub('m', '', unit_dic[group], count = 1)
                else:
                    value /= milli    
                    unit_dic[group] = re.sub('m', '', unit_dic[group])
            if re.search('ng|nM|nmol', unit_dic[group]):
                if group == 'numerator':
                    value *= nano
                    unit_dic[group] = re.sub('n', '', unit_dic[group])
                else:
                    value /= nano   
                    unit_dic[group] = re.sub('n', '', unit_dic[group])
            if re.search('µ|u00b5|U\+00B5', unit_dic[group]):
                if group == 'numerator':
                    value *= micro
                    unit_dic[group] = re.sub('µ|u00b5g|U\+00B5', '', unit_dic[group])
                else:
                    value /= micro 
                    unit_dic[group] = re.sub('µ|u00b5g|U\+00B5', '', unit_dic[group])
                                    
        return value, unit_dic
    
    def _parameter_value(self, var, parameter_info):
        # determine the average parameter value
        end_value = start_value = None
        for start in ["start val.","start value", ]:
            if start in parameter_info[var]:
                start_value = parameter_info[var][start]
                break
        for end in ["end val.","end value", ]:    
            if end in parameter_info[var]:
                end_value = parameter_info[var][end]                                
                break
            
        return average(start_value, end_value)

    def to_fba(self,):
        # import previously content
        self.sabio_df = pandas.read_csv(self.paths['concatenated_data'])
        with open(self.paths['entryids_path']) as json_file: 
            entry_id_data_file = json.load(json_file)

        # combine the scraped data into a programmable JSON  
        enzyme_dict = {}
        missing_entry_ids = []
        enzymes = self.sabio_df["Enzymename"].unique().tolist()
        incorrect_enzymes = []
        undefined_names = set()
        for enzyme in enzymes:
            if enzyme not in self.model_contents:
                incorrect_enzymes.append(enzyme)
                undefined_names.add(enzyme)
                continue
            
            enzyme_df = self.sabio_df.loc[self.sabio_df["Enzymename"] == enzyme]
            reactions = enzyme_df["Reaction"].unique().tolist()
            bigg_reaction_string = self.model_contents[enzyme]['reaction']['original']
            for reaction_string in reactions:                
                # ensure that the reaction chemicals match before accepting kinetic data
                print('\n\nSABIO reaction:', reaction_string)
                bigg_rxn_string, sabio_chemicals, expected_bigg_chemicals = self._split_reaction(reaction_string, sabio = True) 
                bigg_chemicals = self.model_contents[enzyme]['bigg_chemicals']
                extra_bigg = set(bigg_chemicals) - set(expected_bigg_chemicals) 
                extra_bigg = list(set(re.sub('(H\+|H2O|NAD\+|NADH)', '', chem) for chem in extra_bigg))   
                
                loop = 0
                missed_reaction = None
                while len(extra_bigg) <= 1:
                    if re.search('NADP', ' '.join(extra_bigg)) and loop == 0:
                        extra_bigg = [re.sub('NADP.?', '', chem) for chem in extra_bigg]                        
                        loop += 1
                    else:
                        print(extra_bigg)
                        missed_reaction = f'The || {bigg_rxn_string} || reaction with {expected_bigg_chemicals} chemicals does not match the BiGG reaction of {bigg_chemicals} chemicals.'
                        if self.verbose:
                            print(missed_reaction)
                        break                
                if missed_reaction:
                    continue 
                    
                # parse and filter each entryid of the matching reaction
                enzyme_reactions_df = enzyme_df.loc[enzyme_df["Reaction"] == reaction_string]
                entryids = enzyme_reactions_df["EntryID"].unique().tolist()
                for entryid in entryids:  # !!! The following catches should be relocated to parse_data(), where they can prevent mismatches instead of retrospectively catching them. This will be essential for full BiGG models.
                    entryid = str(entryid)
                    entry_id_row = enzyme_reactions_df.loc[enzyme_reactions_df["EntryID"] == int(entryid)]
                    if len(entry_id_row.index) == 0:
                        print(f'{entryid} has no content')
                        continue
                    
                    # assign the rate law for an entryid
                    head_of_df = entry_id_row.head(1).squeeze()
                    rate_law = head_of_df["Rate Equation"]
                    if rate_law == [] or rate_law in ['unknown', '-']:
                        print(f'The {entryid} entryid has an unexpected rate_law {rate_law}.')
                        continue
                    
                    # define the parameters for extant entryids
                    if entryid not in entry_id_data_file:  
                        print(f'The {entryid} entryid is missing from the datafile.')
                        missing_entry_ids.append(entryid)
                        continue
                    
                    corrupted_entries = {}
                    enzyme_dict[enzyme] = {}
                    enzyme_dict[enzyme][entryid] = {}
                    enzyme_dict[enzyme][entryid]["RateLaw"] = rate_law

                    # add annotations and metadata to the assembled dictionary
                    annotations = {}
                    metadata = {}
                    metadata.update({'reaction_string':bigg_rxn_string})
                    for annotation in ["SabioReactionID", "PubMedID", 'ECNumber', 'KeggReactionID']:
                        annotations[annotation] = head_of_df[annotation]
                    metadata.update({'annotations':annotations})
                    for field in ["Buffer", "Product", "Publication", "pH", "Temperature", "Enzyme Variant", "KineticMechanismType", "Organism", "Pathway", ]:  
                        metadata[field] = head_of_df[field]
                    enzyme_dict[enzyme][entryid]['metadata'] = metadata
                        
                    # substitute quantities into the rate law 
                    stripped_string = re.sub('[0-9]', '', rate_law)
                    variables = set(re.split("[\^\*\+\-\/\(\)]", stripped_string))
                    
                    substituted_parameters = {}
                    variable_molar = {}
                    variable_name = {}
                    initial_concentrations = {}
                    parameter_value = True
                    substituted_rate_law = rate_law
                    while parameter_value:
                        for var in variables:
                            # the acceptable variables are filtered for those that possess data and those that are substrates
                            if var in entry_id_data_file[entryid]:
                                variable_name[var] = entry_id_data_file[entryid][var]['species']  #!!! Change the species name to match the BiGG name of the metabolite that is present in the bigg_rxn_string
                                parameter_value = self._parameter_value(var, entry_id_data_file[entryid])                                                                       
                                unit = entry_id_data_file[entryid][var]['unit']
                                parameter_value, unit_dict = self._determine_parameter_value(unit, str(parameter_value))
                                parameter_value = str(parameter_value)
                                if len(var) != 1 or var in ['h', 'n']:
                                    if not parameter_value or parameter_value in ['unknown', '-', 'None', None]:
                                        print(f'The {var} parameter has an unaccepted value {parameter_value}.')
                                        parameter_value = False
                                        break
                                    
                                    variable_molar[var] = parameter_value
                                    substituted_rate_law = substituted_rate_law.replace(var, parameter_value)
                                    substituted_parameters[var] = entry_id_data_file[entryid][var]
                                else:
                                    if isnumber(parameter_value):
                                        initial_concentrations[var] = float(parameter_value)

                        # define the final JSON with the desired content and organization
                        substituted_rate_law = re.sub('\^', '**', substituted_rate_law)
                        if parameter_value:
                            enzyme_dict[enzyme][entryid]["substituted_rate_law"] = substituted_rate_law
                            enzyme_dict[enzyme][entryid]["substituted_parameters"] = substituted_parameters
                            enzyme_dict[enzyme][entryid]["variables_molar"] = variable_molar
                            enzyme_dict[enzyme][entryid]["variables_name"] = variable_name
                            enzyme_dict[enzyme][entryid]['initial_concentrations_M'] = initial_concentrations
                            
                            if substituted_parameters != entry_id_data_file[entryid]:
                                warnings.warn(f'---> ERROR: The rate rate {rate_law} does not reflect {substituted_parameters} in the defined entry variables and parameters.')                            
                        parameter_value = False
                    
                    # remove entryids whose rate laws could not be completely substituted, and thus are not calculable
                    if not "substituted_rate_law" in enzyme_dict[enzyme][entryid]:
                        enzyme_dict[enzyme].pop(entryid)
                        
            if enzyme in enzyme_dict:
                if bigg_reaction_string in enzyme_dict[enzyme]:
                    if enzyme_dict[enzyme] == {}:
                        enzyme_dict.pop(enzyme)

        with open(self.paths["model_kinetics_path"], 'w', encoding="utf-8") as f:
            json.dump(enzyme_dict, f, indent=4, sort_keys=True, cls=NumpyEncoder)
            
        # update the step counter
        print('\n\n\n', 'undescribed enzymes', set(list(self.model_contents.keys())) - set(list(enzyme_dict.keys())))
        print('\n\n\n', 'un-renamed enzymes', undefined_names)
        print('\n\n\n', 'content', list(enzyme_dict.keys()))
        print(f'The dFBA data file have been generated.')
        self._progress_update(self.step_number)