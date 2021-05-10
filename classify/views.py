from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
import pickle
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.compat.v1 import Session
from tensorflow import Graph
from store.models.customer import Customer
from store.models.farmer import Farmer
from django.contrib.sessions.models import Session as SS


model_graph = Graph()

with model_graph.as_default():
	tf_session = Session()
	with tf_session.as_default():




		#with open('cnn_model.pkl', 'rb') as f:
    	 #model = pickle.load(f)
		model = load_model("classify/AlexNetModel.hdf5")
		# Please use the below link to download model from drive because it is of large size so
		# i cannot use it here. 
		#model = "https://drive.google.com/file/d/1uoa7_WWQXaahpnAB6JbqNZV6Kr9RKm2Z/view?usp=sharing"

IMG_WIDTH = 224
IMG_HEIGHT = 224

'''labels = {0: "Corn Gray leaf spot", 
1: "Common rust Corn Maize", 
2: "Northern Leaf Blight Corn Maize", 
3: "Healthy Maize Corn", 
4: "Early blight Potato leaf", 
5: "Late blight Potato Leaf", 
6: "healthy Potato Leaf", 
7: "Bacterial spot of Tomato", 
8: "Leaf Mold of Tomato", 
9: "Yellow Leaf Curl Virus Tomato", 
10: "Mosaic virus leaf Tomato", 
11: "Healthy Tomato Leaf"}

print(labels[0])'''

labels = {0: 'Apple___Apple_scab',
 1: 'Apple___Black_rot',
 2: 'Apple___Cedar_apple_rust',
 3: 'Apple___healthy',
 4: 'Blueberry___healthy',
 5: 'Cherry_(including_sour)___Powdery_mildew',
 6: 'Cherry_(including_sour)___healthy',
 7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 8: 'Corn_(maize)___Common_rust_',
 9: 'Corn_(maize)___Northern_Leaf_Blight',
 10: 'Corn_(maize)___healthy',
 11: 'Grape___Black_rot',
 12: 'Grape___Esca_(Black_Measles)',
 13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 14: 'Grape___healthy',
 15: 'Orange___Haunglongbing_(Citrus_greening)',
 16: 'Peach___Bacterial_spot',
 17: 'Peach___healthy',
 18: 'Pepper,_bell___Bacterial_spot',
 19: 'Pepper,_bell___healthy',
 20: 'Potato___Early_blight',
 21: 'Potato___Late_blight',
 22: 'Potato___healthy',
 23: 'Raspberry___healthy',
 24: 'Soybean___healthy',
 25: 'Squash___Powdery_mildew',
 26: 'Strawberry___Leaf_scorch',
 27: 'Strawberry___healthy',
 28: 'Tomato___Bacterial_spot',
 29: 'Tomato___Early_blight',
 30: 'Tomato___Late_blight',
 31: 'Tomato___Leaf_Mold',
 32: 'Tomato___Septoria_leaf_spot',
 33: 'Tomato___Spider_mites Two-spotted_spider_mite',
 34: 'Tomato___Target_Spot',
 35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 36: 'Tomato___Tomato_mosaic_virus',
 37: 'Tomato___healthy'}


def index_1(request):
	session = SS.objects.get(session_key=request.session.session_key)
	session_data = session.get_decoded()
	groups = session_data.keys()
	list_group = []
	for grp in groups:
		list_group.append(grp)
	
	if list_group[0] == 'farmer':
		entry = Farmer.objects.get(id=session_data['farmer'])
		firstname = entry.first_name
		lastname = entry.last_name
		email = entry.email
		phone = entry.phone
	
	if list_group[0] == 'customer':
		entry = Customer.objects.get(id=session_data['customer'])
		firstname = entry.first_name
		lastname = entry.last_name
		email = entry.email
		phone = entry.phone
	

	return render(request, "index_1.html",{'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})




def predictImage(request):
	#print(request.POST.dict())
	fileObj = request.FILES["document"]
	fs=FileSystemStorage()
	filePathName = fs.save(fileObj.name,fileObj)
	test_image_1 = "./uploads/products/" + filePathName
	filePathName = fs.url(filePathName)
	#print(filePathName)
	#test_image = "."+filePathName

	img = image.load_img(test_image_1,target_size=(IMG_WIDTH,IMG_HEIGHT,3))
	img = image.img_to_array(img)
	img = img/255
	x = img.reshape(1,IMG_WIDTH,IMG_HEIGHT,3)
	with model_graph.as_default():
		with tf_session.as_default():
			proba = model.predict(x)
			top_3 = np.argsort(proba[0])[:-4:-1]
	max_proba = np.max(proba)
	if max_proba>0.5:
		for i in range(1):
			label_pred = labels[(top_3[i])]
			acc_pred = proba[0][top_3[i]]*100
	else:
		message = "This image is not of leaf please try other one."
	#print(np.max(proba))
	#print(label_pred)
	#print(acc_pred)
	session = SS.objects.get(session_key=request.session.session_key)
	session_data = session.get_decoded()
	groups = session_data.keys()
	list_group = []
	for grp in groups:
		list_group.append(grp)
	
	if list_group[0] == 'farmer':
		entry = Farmer.objects.get(id=session_data['farmer'])
		firstname = entry.first_name
		lastname = entry.last_name
		email = entry.email
		phone = entry.phone
	
	if list_group[0] == 'customer':
		entry = Customer.objects.get(id=session_data['customer'])
		firstname = entry.first_name
		lastname = entry.last_name
		email = entry.email
		phone = entry.phone
	



	# prediction = labels[str(np.argmax(proba[0]))]
	 #Getting currently logged-in user maintaining Session





	context={
	"filePathName":filePathName,
	"prediction":label_pred,
	"Accuracy" : acc_pred,
	"firstname":firstname, 
	"lastname":lastname, 
	"email":email, 
	"phone":phone
	}
	return render(request,"test_1.html",context)

