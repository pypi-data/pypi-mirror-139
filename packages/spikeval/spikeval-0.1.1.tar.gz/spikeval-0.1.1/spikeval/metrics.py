import numpy as np
import pandas as pd

def classification_summary(
        dataframe: pd.DataFrame, 
        target_col: str="target",
        pred_col: str='pred', 
        query: str=None, 
        full: bool=False, 
        step: float=0.01,
        custom_metrics: dict=None,
    ) -> pd.DataFrame:
    """
    Computes multiple summary stats over the input dataframe
    containing the resuling predictions and targets of a
    classification task.

    Parameters
    ----------
    dataframe: pandas.DataFrame
        Table containing the predictions and targets
    target_col: string
        Name of the target column (binary)
    pred_col: string
        Name of the predition column (probability)
    query: string 
        String to filter the dataframe previous to compute
        the summary stats.
    full: bool
        If True, compute the stats for each percentiles
        from 0 to 1.
    step: float
        If full=True, this is the step size for the percentiles
        between 0 and 1.
    custom_metrics: dict
        Dictionary containing the pairs metric_name:metric_function
        for metrics to be computed on the dataframe. The signature of
        the metric_function is:
            metric_function(dataframe_full, dataframe_filtered)
        were dataframe_full is the same as the input dataframe
        and dataframe_filtered the dataframe filtered by the
        corresponding percentiles.

    Returns
    -------
    pd.DataFrame
        Table containing the resuting stats at each percentile.
    """

    if query is not None:
        dataframe_ = dataframe.query(query).copy()
    else:
        dataframe_ = dataframe.copy()

    results = list()
    prev_thresh = 1
    
    if not full:
        frac_iter = [.01, .02, .03, .04, .05] + [.05+.05*n for n in range(1, 20)]
    else:
        frac_iter = np.arange(step, 1.01, step)

    for frac in frac_iter:

        thresh = dataframe_[pred_col].quantile(1-frac)
        dataframe_['top'] = dataframe_[pred_col] > thresh
        dataframe_['group'] = (dataframe_[pred_col] > thresh) & (
            dataframe_[pred_col] <= prev_thresh)

        # computes cumulative stats
        cum_resp_rate = dataframe_.query('top')[target_col].mean()
        cum_lift = cum_resp_rate / dataframe_[target_col].mean()
        cum_capture_rate = dataframe_.query('top')[target_col].sum() / dataframe_[target_col].sum()

        # computes group stats
        resp_rate = dataframe_.query('group')[target_col].mean()
        lift = resp_rate / dataframe_[target_col].mean()
        capture_rate = dataframe_.query('group')[target_col].sum() / dataframe_[target_col].sum()

        results.append({
            'cumulative_data_fraction': frac,
            'cumulative_data_pct': int(frac*100),
            'lower_threshold': thresh,
            'lift': lift,
            'cumulative_lift': cum_lift,
            'response_rate': resp_rate,
            'cumulative_response_rate': cum_resp_rate,
            'cumulative_response_pct': int(cum_resp_rate*100),
            'capture_rate': capture_rate,
            'cumulative_capture_rate': cum_capture_rate,
            'cumulative_capture_pct': int(cum_capture_rate*100),
        })

        if custom_metrics is not None:
            for metric_name,metric_func in custom_metrics.items():
                results[-1][f"{metric_name}"] = metric_func(dataframe_, dataframe_.query('group'))
                results[-1][f"cumulative_{metric_name}"] = metric_func(dataframe_, dataframe_.query('top'))
        
        prev_thresh = thresh

    return pd.DataFrame(results)
