from pathlib import Path
import random
from imgaug import augmenters as iaa
import cv2
from random import randint
from tqdm import tqdm


def aug_strategy(strategy):
    '''


    Parameters
    ----------
    strategy : str
        采用数据增强的策略.
        策略介绍：
        1. aug_1: 随机左右或上下翻转，角度变换或仿射变换，随机加噪音，随机裁剪区域
        2. aug_2: 随机左右或上下翻转，颜色变换或对比度变换，随机加噪音，随机裁剪区域
        3. aug_3: 随机左右或上下翻转，颜色变换或其它颜色空间变换，随机加噪音，随机裁剪区域
        4. aug_4: 随机左右或上下翻转，颜色变换或对比度变换，角度变换或仿射变换，随机加噪音，随机裁剪区域（变化最多最全）
        5. aug_5: 随机左右或上下翻转，对比度变换，随机加噪音，随机裁剪区域（相比aug_2，去掉了颜色变换，因为可能引起图片变色过度）
        6. aug_6: 随机左右或上下翻转，对比度变换，随机加噪音（针对大部分场景）
        7. aug_7: 随机对比度变换或颜色变换，随机加噪音（针对一些不可以进行水平和上下翻转的物体）
        8. aug_8: 随机左右或上下翻转，角度变换或仿射变换，随机加噪音，随机裁剪区域（全部都是外形角度变换）
        9. aug_9: 随机左右或上下翻转，角度变换或仿射变换，随机加噪音
        10. aug_10: 随机左右翻转，角度变换，对比度变换，随机加噪音（针对大部分场景）
        11. aug_11: 角度变换，对比度变化，随机加噪音（针对一些不可以进行水平和上下翻转的物体）
        12. aug_12: 特殊算子，用来重写，以便模拟某些特殊情况（包括后面可能产生的aug_13, aug_14...）
        13. aug_13: 为立式机采集的图片放到台式机上使用做变换（降低亮度和对比度）
        14. aug_14: 进行模仿抖动而采取的运动模糊、高斯模糊、平均模糊、中值模糊策略
        15. aug_x: 随机挑选策略中的任意一个（从aug_1到aug_11中任选一个）

    Returns
    -------
    aug: none, 进行数据增强的策略

    '''
    aug_1 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-20, 20)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1)),
            iaa.PiecewiseAffine(scale=(0.01, 0.15)),
            iaa.PerspectiveTransform(scale=(0.01, 0.025))
        ]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])
    ])  # 随机裁切1-3块，每块占比整个图片大小的10%

    aug_2 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.WithBrightnessChannels(iaa.Add((-10, 10)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        # iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.1), add=(-30, 30)),
        # iaa.AddToBrightness((-30, 30)),
        # iaa.MultiplySaturation((0.5, 1.1)),
        # iaa.MultiplyHue((0.5, 1.1)),
        # iaa.MultiplyHueAndSaturation((0.5, 1.1))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_3 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.WithBrightnessChannels(iaa.Add((-10, 10)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6)),
            iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.1), add=(-30, 30)),
            iaa.AddToBrightness((-30, 30)),
            iaa.MultiplySaturation((0.5, 1.1)),
            iaa.MultiplyHue((0.5, 1.1)),
            iaa.MultiplyHueAndSaturation((0.5, 1.1))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_4 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.WithBrightnessChannels(iaa.Add((-10, 10)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-30, 30)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1)),
            iaa.PiecewiseAffine(scale=(0.01, 0.15)),
            iaa.PerspectiveTransform(scale=(0.01, 0.15))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_5 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_6 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_7 = iaa.Sequential([
        iaa.OneOf([
            iaa.WithBrightnessChannels(iaa.Add((-10, 10)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_8 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-30, 30)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1)),
            iaa.PiecewiseAffine(scale=(0.01, 0.15)),
            iaa.PerspectiveTransform(scale=(0.01, 0.15))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.5,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_9 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-30, 30)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1)),
            iaa.PiecewiseAffine(scale=(0.01, 0.15)),
            iaa.PerspectiveTransform(scale=(0.01, 0.15))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_10 = iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.OneOf([
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-30, 30)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_11 = iaa.Sequential([
        iaa.OneOf([
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.OneOf([
            iaa.Affine(shear=(-5, 5)),
            iaa.Affine(rotate=(-30, 30)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_12 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        # iaa.MultiplyBrightness((0.8, 1.1)),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.Sometimes(0.5, iaa.Affine(rotate=(-10, 10))),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_13 = iaa.Sequential([
        iaa.OneOf([
            iaa.Sometimes(0.9, iaa.MultiplyBrightness((0.7, 0.9))),
            iaa.Sometimes(0.9, iaa.GammaContrast((0.5, 1.2))),
            # iaa.Sometimes(0.9, iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6))),
            iaa.Sometimes(0.9, iaa.LogContrast(gain=(0.6, 1.0))),
            iaa.Sometimes(0.9, iaa.LinearContrast((0.4, 1.0)))]),

        iaa.Sometimes(0.1, iaa.Affine(rotate=(-30, 30))),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))]),
        iaa.OneOf([
            iaa.Sometimes(0.4,
                          iaa.Cutout(fill_mode="constant", cval=(0, 255), fill_per_channel=0.5)),
            iaa.Sometimes(0.4,
                          iaa.Cutout(fill_mode="gaussian", fill_per_channel=True)),
            iaa.Sometimes(0.4,
                          iaa.Cutout(nb_iterations=(1, 3), size=0.1, squared=False))])])

    aug_14 = iaa.Sequential([
        iaa.Sometimes(0.8, iaa.OneOf([
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))])),
        # iaa.ChangeColorTemperature((1100, 10000))]),
        iaa.Sometimes(0.5, iaa.OneOf([
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1))])),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_15 = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.Sometimes(0.6, iaa.OneOf([
            iaa.LinearContrast((0.6, 1.4)),
            iaa.ScaleX((0.9, 1.1)),
            iaa.ScaleY((0.9, 1.1)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.Affine(rotate=(-5, 5)),
            iaa.TranslateY(percent=(-0.1, 0.1))])),
        iaa.OneOf([
            iaa.Sometimes(0.1,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.1,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.1,
                          iaa.AdditivePoissonNoise(0, 1))])])

    aug_demo = iaa.Sequential([
        iaa.OneOf([
            iaa.Fliplr(0.5),
            iaa.Flipud(0.5)]),
        iaa.OneOf([
            iaa.Affine(rotate=(-20, 20)),
            iaa.TranslateX(percent=(-0.1, 0.1)),
            iaa.TranslateY(percent=(-0.1, 0.1))]),
        iaa.OneOf([
            iaa.WithBrightnessChannels(iaa.Add((-10, 10)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),
            iaa.GammaContrast((0.5, 2.0)),
            iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
            iaa.LogContrast(gain=(0.6, 1.4)),
            iaa.LinearContrast((0.4, 1.6))]),
        iaa.OneOf([
            iaa.Sometimes(0.2,
                          iaa.AdditiveGaussianNoise(scale=(0, 0.1 * 255))),
            iaa.Sometimes(0.2,
                          iaa.AdditiveLaplaceNoise(scale=0.1 * 255)),
            iaa.Sometimes(0.2,
                          iaa.AdditivePoissonNoise(0, 1))])])

    if strategy == '1':
        return aug_1

    elif strategy == '2':
        return aug_2

    elif strategy == '3':
        return aug_3

    elif strategy == '4':
        return aug_4

    elif strategy == '5':
        return aug_5

    elif strategy == '6':
        return aug_6

    elif strategy == '7':
        return aug_7

    elif strategy == '8':
        return aug_8

    elif strategy == '9':
        return aug_9

    elif strategy == '10':
        return aug_10

    elif strategy == '11':
        return aug_11

    elif strategy == '12':
        return aug_12

    elif strategy == '13':
        return aug_13

    elif strategy == '14':
        return aug_14

    elif strategy == '15':
        return aug_15

    elif strategy == 'x':
        return random.sample([aug_1, aug_2, aug_3, aug_4, aug_5,
                              aug_6, aug_7, aug_8, aug_9, aug_10,
                              aug_11, aug_12, aug_13, aug_14, aug_15], 1)[0]

    elif strategy == 'demo':
        return aug_demo


def increase(dir,num=1000):
    dir = Path(dir)
    aug = aug_strategy("6")
    if not dir.joinpath("image_enhancement").exists():
        dir.joinpath("image_enhancement").mkdir()
    total = 0
    while True:
        if total==num:
            break
        for i in tqdm(list(dir.glob("*.jpg"))):
            rn = randint(1, 100)
            img = cv2.imread(i.__str__())
            new_img = aug.augment_image(img)
            new_img_name = dir.joinpath("image_enhancement",i.name[:-4]+f"_new{rn}.jpg")
            cv2.imwrite(new_img_name.__str__(),new_img)
            total+=1
            if total==num:
                break


if __name__ == '__main__':
    increase(r"C:\VOC2007\Capture",1000)