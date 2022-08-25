import gzip
import ijson
import pandas as pd

def parse_tic_toc(file_path):
    
    ###### Do a first pass collecting Reporting Entity and Type
    if file_path.endswith('.json.gz'):
        toc_file = gzip.open(file_path, 'rb')
    elif file_path.endswith('.json'):
        toc_file = open(file_path)
    else:
        raise ValueError("Expecting a .json or .json.gz file...")

    parser = ijson.parse(toc_file)
    for prefix, event, value in parser:
        if prefix == 'reporting_entity_name':
            reporting_entity_name = value
        if prefix == 'reporting_entity_type':
            reporting_entity_type = value
    
    toc_file.close()
    
    ###### Next, collect Reporting Plans
    if file_path.endswith('.json.gz'):
        toc_file = gzip.open(file_path, 'rb')
    elif file_path.endswith('.json'):
        toc_file = open(file_path)
    else:
        raise ValueError("Expecting a .json or .json.gz file...")

    reporting_plans = ijson.items(toc_file, 'reporting_structure.item.reporting_plans')
    rps = pd.DataFrame()
    for (struct_num, rep_plan) in enumerate(reporting_plans):
        plan_details = pd.DataFrame([plan for plan in rep_plan])
        plan_details['reporting_structure_number'] = struct_num
        rps = rps.append(plan_details, ignore_index=True)
        
    rps['reporting_entity_name'] = reporting_entity_name
    rps['reporting_entity_type'] = reporting_entity_type
    
    toc_file.close()
    
    ###### Next, collect In-Network File Location Objects
    if file_path.endswith('.json.gz'):
        toc_file = gzip.open(file_path, 'rb')
    elif file_path.endswith('.json'):
        toc_file = open(file_path)
    else:
        raise ValueError("Expecting a .json or .json.gz file...")
        
    in_network_files = ijson.items(toc_file, 'reporting_structure.item.in_network_files')
    infs = pd.DataFrame()
    for (struct_num, in_netw_f) in enumerate(in_network_files):
        in_net_f_detail = pd.DataFrame([inf for inf in in_netw_f])
        in_net_f_detail['reporting_structure_number'] = struct_num
        infs = infs.append(in_net_f_detail, ignore_index=True)
        
    infs['reporting_entity_name'] = reporting_entity_name
    infs['reporting_entity_type'] = reporting_entity_type
    
    toc_file.close()
    
    ###### Finally, collect Allowed Amount File Location Objects
    if file_path.endswith('.json.gz'):
        toc_file = gzip.open(file_path, 'rb')
    elif file_path.endswith('.json'):
        toc_file = open(file_path)
    else:
        raise ValueError("Expecting a .json or .json.gz file...")
        
    allowed_amt_file = ijson.items(toc_file, 'reporting_structure.item.allowed_amount_file')
    aafs = pd.DataFrame([aaf for aaf in allowed_amt_file])    
    aafs['reporting_structure_number'] = aafs.index
    
    aafs['reporting_entity_name'] = reporting_entity_name
    aafs['reporting_entity_type'] = reporting_entity_type
    
    return rps, infs, aafs