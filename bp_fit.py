import numpy as np,pandas as pd,os
np.random.seed(1337)  # for reproducibility
 #3 建立一个简单BP神经网络模型
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD
def getdate():
    image_path0 = '股票数据\\训练数据\\0\\'
    image_path1 = '股票数据\\训练数据\\1\\'
    image_path='股票数据\\待判断\\'
    f0=os.listdir(image_path0)
    f1=os.listdir(image_path1)
    f2=os.listdir(image_path)
    xq=[]
    yq=[]
    for k in f0:
        ww=pd.read_csv(image_path0+k,header=0)
        ww=np.array(ww)
        ww=ww[np.newaxis,:,:]
        xq.append(ww)
        yq.append(0)
    for k in f1:
        ww=pd.read_csv(image_path1+k,header=0)
        ww=np.array(ww)
        ww=ww[np.newaxis,:,:]
        xq.append(ww)
        yq.append(1)
    for k in range(xq.__len__()):
        if k==0:
            x=xq[0]
        else:
            x=np.append(x,xq[k],axis=0)
    y=np.array(yq)
    #BP专用
    xx=list(x)
    x=[]
    for k in xx:
        k=k.ravel()
        x.append(k)
    x=np.array(x)

#读取待判断数据
    xq=[]
    for k in f2:
        ww=pd.read_csv(image_path+k,header=0)
        ww=np.array(ww)
        ww=ww[np.newaxis,:,:]
        xq.append(ww)
    for k in range(xq.__len__()):
        if k==0:
            xp=xq[0]
        else:
            xp=np.append(xp,xq[k],axis=0)
    #BP专用
    xxp=list(xp)
    xp=[]
    for k in xxp:
        k=k.ravel()
        xp.append(k)
    xp=np.array(xp)

    return x,y,xp,f2
def get_model():
    model=Sequential(
        [
            Dense(64,input_dim=506),
            Activation("relu"),
            Dense(16),
            Activation("relu"),
            Dense(2),
            Activation("sigmoid"),#激活函数为sigmoid函数
        ]
    )
    sgd=SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True) #lr因子，步长，实质因子
    model.compile(optimizer=sgd, loss="sparse_categorical_crossentropy")  # 损失函数为cross
    return model
x, y,xp,m = getdate()#获取数据
model=get_model()#获取初始化的模型
model.fit(x,y,nb_epoch=300,batch_size=20) #训练300轮，每次取20个数字
cc=model.predict_classes(xp)#预测
