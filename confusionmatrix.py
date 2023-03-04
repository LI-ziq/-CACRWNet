# 输出混淆矩阵
# matplotlib.use('TkAgg')
import torch
import config
import config as cfg
import time
from PIL import Image
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

batch_size = 8
num_classes = config.NUM_CLASSES
valid_directory = config.VALID_DATASET_DIR
test_valid_transforms = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406],
                                  [0.229, 0.224, 0.225])
])
valid_datasets = datasets.ImageFolder(valid_directory,transform=test_valid_transforms)
valid_data_size = len(valid_datasets)
valid_data = torch.utils.data.DataLoader(valid_datasets, batch_size=batch_size, shuffle=True)
from sklearn.metrics import confusion_matrix

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import time
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.size'] = 30
# 更新混淆矩阵


def confusion_matrix(preds, labels, conf_matrix):
    for p, t in zip(preds, labels):
        conf_matrix[p, t] += 1
    return conf_matrix


# 绘制混淆矩阵
def plot_confusion_matrix(cm, labels):
    from sklearn.metrics import confusion_matrix
    # cmap = plt.cm.binary
    # cmap = plt.cm.paired
    # camp = plt.cm.get_cmap('Accent')
    cm = cm
    print(cm)
    tick_marks = np.array(range(len(labels))) + 0.5
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float64') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(32, 27), dpi=400)
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)
    intFlag = 0  # 标记在图片中对文字是整数型还是浮点型
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        #

        if (intFlag):
            c = cm[y_val][x_val]
            plt.text(x_val, y_val, "%d" % (c,), color='white',
                     fontsize=22, va='center', ha='center')

        else:
            c = cm_normalized[y_val][x_val]
            if (c > 0.001):
                if (y_val == x_val):
                    plt.text(x_val, y_val, "%0.2f" % (c,), color='white',
                             fontsize=22, va='center', ha='center')
                else:
                    plt.text(x_val, y_val, "%0.2f" % (c,), color='black',
                             fontsize=22, va='center', ha='center')
            else:
                plt.text(x_val, y_val, "%d" % (0,), color='black',
                         fontsize=22, va='center', ha='center')
    if (intFlag):
        plt.imshow(cm, interpolation='nearest', cmap="Blues")
    else:
        plt.imshow(cm_normalized, interpolation='nearest', cmap="Blues")
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.title('')
    plt.colorbar()
    xlocations = np.array(range(len(labels)))

    # p = range(0,21,1)
    # xlocations = p

    plt.xticks(xlocations, labels, rotation=90, fontsize=40)
    # plt.xticks(xlocations, labels, fontsize=10)
    plt.yticks(xlocations, labels, fontsize=40)
    plt.ylabel('True Classes', fontsize=40)
    plt.xlabel('Predict Classes', fontsize=40)
    # plt.savefig('confusion_UCM.png',
    #             dpi=400, bbox_inches='tight')
    plt.savefig('confusion_AID28.png',
                dpi=500, bbox_inches='tight')
    plt.show()


# 创建一个空矩阵存储混淆矩阵
conf_matrix = torch.zeros(cfg.NUM_CLASSES, cfg.NUM_CLASSES)
for batch_images, batch_labels in valid_data:
        # print(batch_labels)
    with torch.no_grad():
        if torch.cuda.is_available():
                batch_images, batch_labels = batch_images.cuda(), batch_labels.cuda()
    model = torch.load('./2_model.pth')
    out = model(batch_images)
    prediction = torch.max(out, 1)[1]
    conf_matrix = confusion_matrix(
    prediction, labels=batch_labels, conf_matrix=conf_matrix)

    # conf_matrix需要是numpy格式
    # attack_types是分类实验的类别，eg：attack_types = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
# attack_types = ['agricultural', 'airplane', 'baseballdiamond', 'beach', 'buildings', 'chaparral',
#         'denseresidential', 'forest', 'freeway', 'golfcourse', 'harbor',
#                     'intersection', 'mediumresidential', 'mobilehomepark', 'overpass', 'parkinglot',
#                             'river', 'runway', 'sparseresidential', 'storagetanks', 'tenniscourt']
    attack_types = ['Airport', 'BareLand', 'BaseballField', 'Beach', 'Bridge', 'Center', 'Church', 'Commercial',
                    'DenseResidential', 'Desert', 'Farmland', 'Forest', 'Industrial', 'Meadow',
    'MediumResidential', 'Mountain', 'Park', 'Parking', 'Playground', 'Pond', 'Port', 'RailwayStation',
                    'Resort', 'River', 'School', 'SparseResidential', 'Square', 'Stadium', 'StorageTanks', 'Viaduct']
# attack_types = ['airplane', 'airport', 'baseball_diamond', 'basketball_court', 'beach', 'bridge', 'chaparral',
# 'church', 'circular_farmland', 'cloud', 'commercial_area',
#                     'dense_residential', 'desert', 'forest', 'freeway', 'golf_course', 'ground_track_field',
#                     'harbor', 'industrial_area', 'intersection', 'island', 'lake',
#                     'meadow', 'medium_residential', 'mobile_home_park', 'mountain', 'overpass', 'palace',
#                     'parking_lot', 'railway', 'railway_station', 'rectangular_farmland',
#                     'river', 'roundabout', 'runway', 'sea_ice', 'ship', 'snowberg', 'sparse_residential',
#                     'stadium', 'storage_tank', 'tennis_court', 'terrace', 'thermal_power_station', 'wetland']
plot_confusion_matrix(conf_matrix.numpy(), attack_types)
