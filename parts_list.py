'''
Required pices: [620, 620, 510, 510, 390] (2650 total)
Accepted supplier lengths: [500, 1000, 1500, 2000]
Cut width: 3

length=2000, waste=244, pices=[620, 620, 510]
length=1000, waste=97, pices=[510, 390]
'''
sq60 = [
  620, 620, 510, 510, 390
]

'''
Required pices: [510, 510, 300, 300, 220, 510, 510, 300, 300, 220] (3680 total)
Accepted supplier lengths: [500, 1000, 1500, 2000]
Cut width: 3

length=2000, waste=68, pices=[300, 510, 510, 300, 300]
length=1500, waste=31, pices=[220, 220, 510, 510]
length=500, waste=200, pices=[300]
'''
sq40 = [
  510, 510, 300, 300, 220,
  510, 510, 300, 300, 220
]

'''
Required pices: [960, 960, 255, 255, 195, 195, 440, 440, 650, 650, 255, 255] (5510 total)
Accepted supplier lengths: [500, 1000, 1500, 2000]
Cut width: 3

length=2000, waste=77, pices=[960, 960]
length=1000, waste=31, pices=[255, 255, 255, 195]
length=2000, waste=8, pices=[255, 195, 440, 440, 650]
length=1000, waste=350, pices=[650]
'''
sq30 = [
  960, 960, 255, 255, 195, 195,
  440, 440,
  650, 650, 255, 255
]

def get_current_pices():
  return sq30