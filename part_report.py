import cv2 as cv


img = cv.imread(r"D:\corneal_pachymetry\corneal_pachymetry\images\Pachymetry  report.jpeg")
img = cv.resize(img,(500,500))
cv.imshow("report",img)
# cv.waitKey(0)
# cv.destroyAllWindows()

crop_pc_od = img[120:280, 30:135]
crop_pc_od = cv.resize(crop_pc_od,(250,250))
cv.imshow("crop_pc_od",crop_pc_od)
#cv.waitKey(0)
#cv.destroyAllWindows()



#crop_pc_os = img[125:280, 170:275]
crop_pc_os = img[120:280, 173:275]
crop_pc_os = cv.resize(crop_pc_os,(250,250))
cv.imshow("rcrop_pc_os",crop_pc_os)
#cv.waitKey(0)
#cv.destroyAllWindows()


crop_epithial_od =img[315:480, 25:134]
crop_epithial_od = cv.resize(crop_epithial_od,(250,250))
cv.imshow("crop_epithial_od",crop_epithial_od)
#cv.waitKey(0)
#cv.destroyAllWindows()


crop_epithial_os =img[317:480, 170:278]
crop_epithial_os = cv.resize(crop_epithial_os,(250,250))
cv.imshow("crop_epithial_os",crop_epithial_os)
cv.waitKey(0)
cv.destroyAllWindows()




# import cv2 as cv


# img = cv.imread(r"D:\corneal_pachymetry\corneal_pachymetry\images\Pachymetry  report.jpeg")
# #cv.imshow("report",img)
# # cv.waitKey(0)
# # cv.destroyAllWindows()

# crop_pc_od = img[215:435, 75:325]
# #crop_pc_od = cv.resize(crop_pc_od,(250,250))
# #cv.imshow("crop_pc_od",crop_pc_od)
# #cv.waitKey(0)
# #cv.destroyAllWindows()


# crop_pc_os =img[215:435, 410:670]
# crop_pc_os = cv.resize(crop_pc_os,(250,250))
# #cv.imshow("rcrop_pc_os",crop_pc_os)
# #cv.waitKey(0)
# #cv.destroyAllWindows()


# crop_epithial_od =img[510:770, 75:325]
# crop_epithial_od = cv.resize(crop_epithial_od,(250,250))
# cv.imshow("crop_epithial_od",crop_epithial_od)
# cv.waitKey(0)
# cv.destroyAllWindows()


# crop_epithial_os =img[510:770, 410:670]
# crop_epithial_os = cv.resize(crop_epithial_os,(250,250))
# cv.imshow("crop_epithial_os",crop_epithial_os)
# cv.waitKey(0)
# cv.destroyAllWindows()


