import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

elastixImageFilter = sitk.ElastixImageFilter()
im1 = sitk.ReadImage("images/K0006-11_1_Frame13.jpg", sitk.sitkUInt8)
im2 = sitk.ReadImage("images/K0006-11_1_Frame14.jpg", sitk.sitkUInt8)
elastixImageFilter.SetFixedImage(im1)
elastixImageFilter.SetMovingImage(im2)
# elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("affine"))
parameterMapVector = sitk.VectorOfParameterMap()
parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))
parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))
elastixImageFilter.SetParameterMap(parameterMapVector)

elastixImageFilter.LogToFileOn()
elastixImageFilter.SetOutputDirectory("./")
elastixImageFilter.Execute()

res = sitk.GetArrayFromImage(elastixImageFilter.GetResultImage())
diff = sitk.GetArrayFromImage(im1) - res
plt.imsave('origin_subtract_aligned.jpg', diff, cmap='gray')
plt.imsave('angio_aligned.jpg', res, cmap=plt.gray())

param = elastixImageFilter.GetTransformParameterMap()


print("----Finished-----")
# sitk.PrintParameterMap(elastixImageFilter.GetTransformParameterMap()[0])

print("---Applying to segmented image---")
elastixImageFilter = sitk.ElastixImageFilter()
im3 = sitk.ReadImage("images/K0006-11_1_Frame13_prediction.png", sitk.sitkUInt8)
# res = sitk.Transformix(im3, param)
# plt.imshow(sitk.GetArrayFromImage(res), cmap='gray')
# plt.show()
im4 =  sitk.ReadImage("images/K0006-11_1_Frame14_prediction.png", sitk.sitkUInt8)
elastixImageFilter.SetInitialTransformParameterFileName('TransformParameters.0.txt')
elastixImageFilter.SetFixedImage(im3)
elastixImageFilter.SetMovingImage(im4)
elastixImageFilter.Execute()

# transform = sitk.TransformixImageFilter()
# # params = sitk.ReadParameterFile("TransformParameters.0.txt")
# # transform.SetTransformParameterMap(params)
# transform.SetTransformParameterMap(param)
# sitk.PrintParameterMap(transform.GetTransformParameterMap())
# transform.SetMovingImage(im3)
# transform.Execute()

res = sitk.GetArrayFromImage(elastixImageFilter.GetResultImage())
print(res)
plt.imsave('seg_aligned.jpg', res, cmap=plt.gray())

exit()
res = sitk.GetArrayFromImage(transform.GetResultImage())
plt.imshow(res, cmap='gray')
plt.show()
# plt.imshow(sitk.GetArrayFromImage(im3), cmap='gray')
# plt.show()
# transformed = sitk.Transformix(im3, trans_matrix)


# sitk.WriteImage(elastixImageFilter.GetResultImage(), 'result.png')
# array = sitk.GetArrayFromImage(elastixImageFilter.GetResultImage())
# plt.imshow(array, cmap='gray')
# plt.show()

