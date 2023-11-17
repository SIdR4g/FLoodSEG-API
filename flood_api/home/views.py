import cv2
import os

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from .serializers import *
from .models import *


PATH = 'media/'



def SegmentationTask(filename):
    from roboflow import Roboflow

    rf = Roboflow(api_key="wkWk6oLO2S99wPV1bMuj")

    project = rf.workspace().project("flood-1sljl")   
    model = project.version(2).model 

    image_folder = os.path.join(PATH,'image/'+filename)
    mask_folder = os.path.join(PATH,'mask/predicted_'+filename)


    prediction = model.predict(image_folder, confidence=98)
    result = prediction.json()
    s = prediction.save(mask_folder)

    return image_folder,mask_folder,result






class PatchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self,request):
        try:
            flood_patch = FloodedImagePatch.objects.filter(user = request.user)

            if request.GET.get("search"):
                search = request.GET.get("search")
                flood_patch = flood_patch.filter(patch_code=search).order_by('image_id')
                print(len(flood_patch))

                if request.GET.get("merge") and request.GET.get("patch_dimension"):
                    merge = request.GET.get("merge")
                    patch_dimension = request.GET.get("patch_dimension").split('x')

                    
                    if merge == "original":
                        
                        img = [cv2.imread(os.path.normpath(flood_patch[idx].captured_image.name)) for idx in range(int(patch_dimension[1]))]
                        vertical = cv2.hconcat(img)
                    
                        for i in range(int(patch_dimension[1]),len(flood_patch),int(patch_dimension[1])):
                            img = [cv2.imread(os.path.normpath(flood_patch[idx].captured_image.name)) for idx in range(i,i+int(patch_dimension[1]))]
                            horizontal = cv2.hconcat(img)
                            vertical = cv2.vconcat([vertical,horizontal])


                    elif merge == "segment":
                        img = [cv2.imread(os.path.normpath(flood_patch[idx].segmented_image.name)) for idx in range(int(patch_dimension[1]))]
                        vertical = cv2.hconcat(img)
                    
                        for i in range(int(patch_dimension[1]),len(flood_patch),int(patch_dimension[1])):
                            img = [cv2.imread(os.path.normpath(flood_patch[idx].segmented_image.name)) for idx in range(i,i+int(patch_dimension[1]))]
                            horizontal = cv2.hconcat(img)
                            vertical = cv2.vconcat([vertical,horizontal])
                    else:
                        return Response({
                            'data': {},
                            'message': 'something went wrong',   
                        }, status  = status.HTTP_400_BAD_REQUEST)

                    cv2.imwrite('stitched.jpg', vertical) 
                    
                    return Response({
                        'data' : 'stitched.jpg',
                        'message' : 'patches merged successfully'
                    }, status = status.HTTP_200_OK)

                else:
                    return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)


        
            serializer = FloodedImagePatchSerializer(flood_patch, many = True)
            
            return Response({
                'data' : serializer.data,
                'message' : 'blogs fetched successfully'
            }, status = status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            data = request.data
            files = request.FILES
            data['user'] = request.user.id
            print(data)

            dummy = FloodedImagePatch(captured_image = files['captured_image'])
            serializer = FloodedImagePatchSerializer(dummy, data = data)
            
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            

            image_folder,mask_folder,prediction_json = SegmentationTask(files['captured_image'].name)


            f_img = FloodedImagePatch(user = dummy.user, patch_code = dummy.patch_code, 
                                image_id = dummy.image_id, captured_image = image_folder, 
                                prediction_data = prediction_json, segmented_image = mask_folder)
 
            dummy.delete()
 
            f_img.save()
            serializer = FloodedImagePatchSerializer(f_img)

            return Response({
                'data' : serializer.data,
                'messsage': 'image uploaded successfully',
            }, status = status.HTTP_201_CREATED)

            
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request):
        try:
            data = request.data
            flood = FloodedImagePatch.objects.filter(uid = data.get('uid'))

            if not flood.exists():
                return Response({
                    'data':{},
                    'message':'invalid flood uid'
                },status  = status.HTTP_400_BAD_REQUEST)

            if request.user != flood[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status  = status.HTTP_400_BAD_REQUEST)
            
            serializer = FloodedImagePatchSerializer(flood[0], data=data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data' : serializer.data,
                'messsage': 'updated successfully',
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            data = request.data
            flood = FloodedImagePatch.objects.filter(uid = data.get('uid'))

            if not flood.exists():
                return Response({
                    'data':{},
                    'message':'invalid flood uid'
                },status  = status.HTTP_400_BAD_REQUEST)

            if request.user != flood[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status  = status.HTTP_400_BAD_REQUEST)
            
            
            flood[0].delete()

            return Response({
                'data' : {},
                'messsage': 'deleted successfully',
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)










class DroneView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self,request):
        try:
            images = FloodedImage.objects.filter(user = request.user)

            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(Q(uid=search)|Q(title=search))
        
            serializer = FloodedImageSerializer(images, many = True)
            
            return Response({
                'data' : serializer.data,
                'message' : 'blogs fetched successfully'
            }, status = status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        


    def post(self, request):
        try:
            data = request.data
            files = request.FILES
            data['user'] = request.user.id

            dummy = FloodedImage(captured_image = files['captured_image'])
            serializer = FloodedImageSerializer(dummy, data = data)
            
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            
            import os

            rf = Roboflow(api_key="wkWk6oLO2S99wPV1bMuj")

            project = rf.workspace().project("flood-1sljl")   
            model = project.version(2).model 

            image_folder = os.path.join(PATH,'image/'+files['captured_image'].name)
            mask_folder = os.path.join(PATH,'mask/predicted_'+files['captured_image'].name)


            prediction = model.predict(image_folder, confidence=98)
            result = prediction.json()
            s = prediction.save(mask_folder)



            f_img = FloodedImage(title = dummy.title, captured_image = image_folder, 
                                 prediction_data = result, user = dummy.user, segmented_image = mask_folder)

            z = FloodedImage.objects.get(uid = dummy.uid)
            z.delete()

            f_img.save()

            serializer = FloodedImageSerializer(f_img)
            

            return Response({
                'data' : serializer.data,
                'messsage': 'image uploaded successfully',
            }, status = status.HTTP_201_CREATED)

            
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        try:
            data = request.data
            flood = FloodedImage.objects.filter(uid = data.get('uid'))

            if not flood.exists():
                return Response({
                    'data':{},
                    'message':'invalid flood uid'
                },status  = status.HTTP_400_BAD_REQUEST)

            if request.user != flood[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status  = status.HTTP_400_BAD_REQUEST)
            
            serializer = FloodedImageSerializer(flood[0], data=data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data' : serializer.data,
                'messsage': 'updated successfully',
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            data = request.data
            flood = FloodedImage.objects.filter(uid = data.get('uid'))

            if not flood.exists():
                return Response({
                    'data':{},
                    'message':'invalid flood uid'
                },status  = status.HTTP_400_BAD_REQUEST)

            if request.user != flood[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status  = status.HTTP_400_BAD_REQUEST)
            
            
            flood[0].delete()

            return Response({
                'data' : {},
                'messsage': 'deleted successfully',
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'something went wrong',   
                }, status  = status.HTTP_400_BAD_REQUEST)
        