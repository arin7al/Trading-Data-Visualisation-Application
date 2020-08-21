from RandomDealData import RandomDealData

randomData = RandomDealData()
instrumentList = randomData.createInstrumentList()
for i in range(10):
    print(randomData.createRandomData(instrumentList))