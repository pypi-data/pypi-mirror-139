from typing import Any

from pydantic import BaseModel


class FilterVariable(BaseModel):
    data_column: str  # The column in the remote cohort df to get data from
    filter_column: str  # The column in the remote cohort df to check against
    filter_value: Any  # the value to match against
