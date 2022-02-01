import numpy as np
from scipy.stats import norm

from src.AnalysisTools import experimentalparams as ep
from src.AnalysisTools.datautils import create3dlist

USEDTREATMENTS = ep.USEDTREATMENTS
USEDWEEKS = ep.USEDWEEKS
TREATMENT_TYPES = ep.TREATMENT_TYPES
WS = ep.WS


def removeoutliers3dlist(alldata, m: float = 2):
    """
    removes outliers outside of m standard deviations for 3D lists

    :param alldata: values in 2d list of weeks and treatments.
    :param m: number of standard deviations included. Data outside this is considered outlier data.
    :return: data with outliers removed
    """
    newdata = create3dlist(USEDTREATMENTS, USEDWEEKS)
    for t, treatment in enumerate(TREATMENT_TYPES):
        for w, weekno in enumerate(WS[:USEDWEEKS]):
            wtdata = alldata[t][w]
            wtarr = np.asarray(wtdata)
            # wtarrp = wtarr[wtarr < 2000]
            wtarrp = removeoutliers(wtarr, m)
            newdata[t][w] = list(wtarrp)
            # a = wtarr[wtarr >= 5000]
            #             print(len(wtdata), len(newdata[t][w]), type(wtdata),type(newdata[t][w]))
    return newdata


def removeoutliers(data1darray, m: float = 2):
    """
    removes outliers outside of m standard deviations for 1d arrays
    :param data1darray: 1d array
    :param m:  number of standard deviations included. Data outside this is considered outlier data.
    :return: data with outliers removed
    """
    newdata = data1darray[abs(data1darray - np.mean(data1darray)) < m * np.std(data1darray)]
    return newdata


# def rmoutliers(alldata, m=2):
#     newdata = create3dlist(usedtreatments, usedweeks)
#     for t, treatment in enumerate(treatment_type):
#         for w, weekno in enumerate(ws[:usedweeks]):
#             wtdata = alldata[t][w]
#             wtarr = np.asarray(wtdata)
#             #             wtarrp = wtarr[wtarr<2000]
#             wtarrp = wtarr[abs(wtarr - np.mean(wtarr)) < m * np.std(
#                 wtarr)]  # Note the abs value --> for both ends
#             newdata[t][w] = list(wtarrp)
#     #             a = wtarr[wtarr>=5000]
#     #             print(len(wtdata), len(newdata[t][w]), type(wtdata),type(newdata[t][w]))
#
#     return (newdata)


def perctosd(percentile: float = 95.452):
    """
    calculate standard deviation based on percent point function.

    :param percentile: percentile
    :return: number of standard deviations
    """
    percentile = percentile / 100
    tail = percentile + (1 - percentile) / 2
    z_crit = norm.ppf(tail)
    return z_crit


def removestackoutliers(stackdata: np.ndarray, abstraction: int = 0, m: float = 2, fixeddims=6):
    """
    expected dimensions of stackdata: ((usedtreatments, usedweeks, usedchannels, usedwells, totalFs, maxnocells, maxorganellepercell))
    :param stackdata:
    :param m:
    :return:
    """
    dims = stackdata.ndim
    axes = (0, 1, 2, 3, 4, 5, 6)[:dims]# to account for cell vs organelle dimensions
    # exit()
    if abstraction:
        abstraction = abstraction + dims - fixeddims  # to account for cell vs organelle dimensions
        stackdata = np.nanmean(stackdata, axis=axes[dims-abstraction:dims])
        # print("Abstraction axes", axes[dims - abstraction:dims], stackdata.shape, dims, abstraction)
    nstackdata = stackdata.copy()

    s = stackdata.shape
    for treatment in range(s[0]):
        for week in range(s[1]):
            selectedarray = stackdata[treatment, week].copy()
            stdev = np.nanstd(selectedarray)
            mean = np.nanmean(selectedarray)
            condition = np.abs(selectedarray - mean) < m * stdev

            # nooutlierarray = selectedarray.copy()
            selectedarray[~condition] = np.nan
            nstackdata[treatment, week] = selectedarray
            # print(mean, mean1, stdev, stdev1, np.count_nonzero(selectedarray[~np.isnan(selectedarray)]))
            # print(treatment, week, nstackdata.shape, nstackdata[treatment, week].shape, selectedarray.shape)
    #
    # if 3 < dims < 8:
    #     if dims != 7:
    #         for i in range(7 - dims):
    #             stackdata = np.expand_dims(stackdata, axis=-1)
    #
    # assert (stackdata.ndim == 7)

    return nstackdata


# def reportoutliervalues(vol):
#     if vol > 10000:
#         print(vol, ">10k")

if __name__ == "__main__":
    n1, n2, n3, n4, n5 = 5, 6, 1, 12, 234
    exshape = (n1, n2, n3, n4, n5)
    selectedarray = np.random.random(n1 * n2 * n3 * n4 * n5).reshape(exshape)
    mean = np.mean(selectedarray)
    stdev = np.std(selectedarray)
    # nonoutliers = np.any(abs(selectedarray.flatten() - np.mean(selectedarray.flatten())) < 2 * np.std(selectedarray.flatten()))

    condition = np.abs(selectedarray - mean) < 1 * stdev
    newarray = selectedarray.copy()
    newarray[~condition] = np.nan
    print(condition.shape, mean, stdev, np.min(selectedarray), np.max(selectedarray))
    print(False in condition)
    print(selectedarray[condition].shape, selectedarray[~condition].shape)
    # print((selectedarray).shape, newarray.shape, selectedarray == newarray)
    print(newarray)
