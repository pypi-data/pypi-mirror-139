def selectRegion(strList):
    cc = []
    for i in range(np.shape(strList)[0]):
        tmp = [convert(strList[i][1]),convert(strList[i][0])]
        cc.append(tmp)
    return(cc)