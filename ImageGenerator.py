class ImageGenerator:
  def __init__(self,startIndex,endIndex):
    self.start_index = startIndex
    self.end_index = endIndex
  
  def run(self):
    return self.process_csv_list(self.start_index,self.end_index)

  def process_csv_list(self,start_index,end_index):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import gc
    import ast
    import os
    import warnings
    warnings.filterwarnings("ignore")
    csv_file_list = ['basket.csv','basketball.csv','bat.csv','bear.csv','bed.csv','bee.csv','bicycle.csv','bird.csv','book.csv','bowtie.csv','bracelet.csv','bread.csv','bridge.csv']
    csv_file_list = csv_file_list[start_index:end_index]
    print("csv to process:{}".format(csv_file_list))
    for id,file in enumerate(csv_file_list):
      if file.endswith('.csv'):
        print("Processing File ",file,".... ")
        imageName = file.split('.')[0]
        fields = ["countrycode","drawing","word"]
        data = pd.read_csv('/content/drive/Shared drives/AIGroup/FromGCP/train_simplified/{}'.format(file),skipinitialspace=True,usecols=fields)
        data = pd.DataFrame(data)
        # data = data.head(1000)

        raw_images = []

        for i in data['drawing']:
          image =  ast.literal_eval(i)
          raw_images.append(image)
        
        for index, raw_drawing in enumerate(raw_images, 0):
          print("File{} of {} Files -- {}/{}".format(id,len(csv_file_list),index,len(raw_images)))    
          _=plt.figure(figsize=(6,3))
          dest = '/content/drive/Shared drives/AIGroup/Points_to_Images/{}-{}.png'.format(imageName,index)
          if os.path.exists(dest):
            continue
          for x,y in raw_drawing:
              plt.subplot(1,2,2)
              plt.plot(x, y)
              plt.axis('off')
              plt.gca().invert_yaxis()
              plt.axis('equal')
              _=plt.savefig(dest)
              _=gc.collect()
    return 0