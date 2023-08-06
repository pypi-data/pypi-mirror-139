import pandas as pd

@staticmethod
def dfGroup(dfSource,by=None,columnsList=None,groupbyColumns=None,floatFormatter='{:.2f}',aggDict=None,adjustNames=True):    
    if by != 'agg':
        if columnsList!= None:
            dataFrame = dfSource[columnsList]
            if by == 'mean':
                dataFrame = dataFrame.groupby(groupbyColumns).mean()
            elif by == 'min':
                dataFrame = dataFrame.groupby(groupbyColumns).min()
            elif by == 'max':
                dataFrame = dataFrame.groupby(groupbyColumns).max()
            elif by == 'std':
                dataFrame = dataFrame.groupby(groupbyColumns).std()
            elif by == 'var':
                dataFrame = dataFrame.groupby(groupbyColumns).var()
            elif by == 'count':
                dataFrame = dataFrame.groupby(groupbyColumns).count()
            dataFrame = dataFrame.groupby(groupbyColumns).mean()
            dataFrame = dataFrame.reset_index()
            if adjustNames != False:
                for t in dataFrame.columns:
                    if t in groupbyColumns:
                        pass
                    else:
                        dataFrame = dataFrame.rename({t:f'{t}_{by} '},axis=1)
            for i in (dataFrame.columns):
                if dataFrame[i].dtypes == 'float64':
                    dataFrame.loc[:, i] = dataFrame[i].map(floatFormatter.format)
        else:
            dataFrame = dfSource
            if by == 'mean':
                dataFrame = dataFrame.groupby(groupbyColumns).mean()
            elif by == 'min':
                dataFrame = dataFrame.groupby(groupbyColumns).min()
            elif by == 'max':
                dataFrame = dataFrame.groupby(groupbyColumns).max()
            elif by == 'std':
                dataFrame = dataFrame.groupby(groupbyColumns).std()
            elif by == 'var':
                dataFrame = dataFrame.groupby(groupbyColumns).var()
            elif by == 'count':
                dataFrame = dataFrame.groupby(groupbyColumns).count()
            dataFrame = dataFrame.reset_index()
            if adjustNames != False:
                for t in dataFrame.columns:
                    if t in groupbyColumns:
                        pass
                    else:
                        dataFrame = dataFrame.rename({t:f'{t}_mean '},axis=1)
            if floatFormatter != None:
                for i in (dataFrame.columns):
                    if dataFrame[i].dtypes == 'float64':
                        dataFrame.loc[:, i] = dataFrame[i].map(floatFormatter.format)
            else:
                pass
    elif by == 'agg':
        dataFrame = dfSource
        dataFrame = dataFrame.groupby(groupbyColumns).agg(aggDict)
        dataFrame = dataFrame.reset_index()
        dataFrame = dataFrame.rename({},axis=1)
        if adjustNames != False:
            for t in dataFrame.columns:
                if t in aggDict:
                    dataFrame = dataFrame.rename({t:f'{t}_{aggDict[t]}'},axis=1)
        else:
            pass
        if floatFormatter != None:
            for i in (dataFrame.columns):
                    if dataFrame[i].dtypes == 'float64':
                        dataFrame.loc[:, i] = dataFrame[i].map(floatFormatter.format)
        else:
            pass
    return dataFrame
