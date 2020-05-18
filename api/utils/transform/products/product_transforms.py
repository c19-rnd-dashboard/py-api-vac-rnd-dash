import pandas as pd
import numpy as np
import logging


logger = logging.getLogger(__name__)

def renumber_id(data: pd.DataFrame, id_col='ID') -> pd.DataFrame:
    logger.info(f"Starting id renumber on {id_col}")
    id_list = []
    id = 1
    for i, _ in enumerate(range(len(data))):
        id_list.append(id)
        if i%2 != 0:
            id += 1

    data['ID'] = id_list
    return data