import os
import numpy as np
from tqdm import tqdm
import pickle

class ChunksizedGenerateFeatures():
  def __init__(self,chunksize=3000):
    from keras.applications.vgg16 import VGG16
    self.chunksize = chunksize
    self.ptoi_folder_path = '/content/drive/Shared drives/AIGroup/Points_to_Images'
    self.itof_folder_path = '/content/drive/Shared drives/AIGroup/Images_to_Features'
    self.__generate_chunks__()
    self.model = VGG16(weights='imagenet')
    

  def get_feature_from_image(self,img_path):
    # img_path = '/content/drive/Shared drives/AIGroup/Points_to_Images/The Eiffel Tower-0.png'
    from keras.applications.vgg16 import preprocess_input
    from keras.preprocessing import image
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    vgg16_feature = self.model.predict(img_data)
    return vgg16_feature

  def run(self,chunkID):
    png_files = self.chunks[chunkID]
    for f in tqdm(png_files):
      # num += 1
      rename = f.replace('.png','.feat')
      save_path = '{}/{}'.format(self.itof_folder_path,rename)
      if os.path.exists(save_path):
        continue
      img_path = '{}/{}'.format(self.ptoi_folder_path,f)
      feature = self.get_feature_from_image(img_path)
      rename = f.replace('.png','.feat')
      label = f.split('-')[0]
      with open(save_path,'wb') as fw:
        obj = {'label':label,'feature':feature}
        pickle.dump(obj,fw)

  def __chunks__(self,l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
      yield l[i:i + n]
  def __generate_chunks__(self):
    png_files = os.listdir(self.ptoi_folder_path)
    self.png_files = [p for p in png_files if p.endswith('.png')]
    self.chunks = list(self.__chunks__(png_files,self.chunksize))
    chunk_num = len(self.chunks)
    print("\n{} chunks are needed".format(chunk_num))


if __name__ == "__main__":
    chunkFG = ChunksizedGenerateFeatures()
    chunkFG.run(1)

