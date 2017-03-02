from EmoData.image_pipeline import FACE_pipeline 
import os
import numpy as np
from skimage.io import imread, imsave
pwd = os.path.dirname(os.path.abspath(__file__))

img = imread(pwd+'/data/images/test_07.jpg')

class testcase:

    def test_run_empty(self):
        pip = FACE_pipeline()
        out, pts = pip.run_pipeline(img)
        assert(img.shape==out.shape)
        assert(pts==None)

    def test_grayscale(self):
        pip = FACE_pipeline(
                grayscale=True
                )
        out, pts = pip.run_pipeline(img, preprocessing=True)
        assert(img.shape[:2]==out.shape[:2])
        assert(out.shape[-1]==1)
        assert(pts==None)

    def test_normalization(self):
        pip = FACE_pipeline(
                histogram_normalization=True
                )
        out, pts = pip.run_pipeline(img, preprocessing=True)
        assert(img.shape==out.shape)
        assert(out.max()<=1)
        assert(out.min()>=0)
        assert(pts==None)

    def test_preprocessing(self):
        pip = FACE_pipeline(
                histogram_normalization=True,
                grayscale=True
                )
        out, pts = pip.run_pipeline(img, preprocessing=True)
        assert(img.shape[:2]==out.shape[:2])
        assert(out.shape[-1]==1)
        assert(out.max()<=1)
        assert(out.min()>=0)
        assert(pts==None)

    def test_augmentation(self):

        pip = FACE_pipeline(
                histogram_normalization=True,
                grayscale=True,
                rotation_range = 10,
                width_shift_range = 0.05,
                height_shift_range = 0.05,
                zoom_range = 0.05,
                fill_mode = 'edge',
                random_flip = True,
                )


        out, pts = pip.run_pipeline(
                img, 
                preprocessing=False,
                augmentation=True
                )
        assert(pts==None)
        assert(img.shape==out.shape)


        out, pts = pip.run_pipeline(
                img, 
                preprocessing=True,
                augmentation=True
                )
        assert(pts==None)
        assert(out.shape[-1]==1)
        assert(img.shape[:2]==out.shape[:2])

    def test_face_detection(self):
        pip = FACE_pipeline(
                output_size = [160,240],
                face_size = 160,
                )
        out, pts = pip.run_pipeline(img, face_detect=True)
        assert(out.shape==(240,160,3))
        assert(pts.shape==(68,2))

    def test_full_pipeline(self):
        pip = FACE_pipeline(
                output_size = [160,240],
                face_size = 160,
                histogram_normalization=True,
                grayscale=True,
                rotation_range = 10,
                width_shift_range = 0.05,
                height_shift_range = 0.05,
                zoom_range = 0.05,
                fill_mode = 'edge',
                random_flip = True,
                )
        out, pts = pip.run_pipeline(img, face_detect=True, preprocessing=True, augmentation=True)
        assert(out.shape==(240,160,1))
        assert(pts.shape==(68,2))
        # save output
        # out = out-out.min()
        # out = out/out.max()
        # imsave('test.jpg',out[:,:,0])





if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
